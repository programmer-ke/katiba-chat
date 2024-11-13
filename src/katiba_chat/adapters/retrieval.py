"""Retrieval adapters"""

import dataclasses
import json
import logging
import pathlib

import numpy
from whoosh import fields as F
from whoosh import index as whoosh_index
from whoosh import qparser

from .. import core

log = logging.getLogger(__name__)

DEFAULT_ST_MODELNAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
FileSystemPath = str | pathlib.Path


class SentenceTransformersIndex(core.AbstractIndex):
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        data_path: FileSystemPath,
        index_dirname: FileSystemPath,
        model_name: str = DEFAULT_ST_MODELNAME,
    ):

        # importing on demand because load time can be quite slow
        # pylint: disable=import-outside-toplevel
        from sentence_transformers import SentenceTransformer, util

        self._semantic_search = util.semantic_search

        self._emb_filename = "article_embeddings.npy"
        self._index_data_filename = "articles.json"
        self.model = SentenceTransformer(model_name)
        index_dir = pathlib.Path(index_dirname)
        data_path = pathlib.Path(data_path)
        _ensure_exists(index_dir)
        self._create_index_if_missing(data_path, index_dir)
        self._index_emb = numpy.load(index_dir / self._emb_filename)
        with open(index_dir / self._index_data_filename, "rt") as f:
            self._index_data = json.load(f)

    def search(self, query, num_results):
        query_embeddings = self.model.encode(str(query))
        results = self._semantic_search(
            query_embeddings, self._index_emb, top_k=num_results
        )
        article_indices = [r["corpus_id"] for r in results[0]]
        matching_articles = [
            core.Article(**self._index_data[idx]) for idx in article_indices
        ]
        return matching_articles

    def _create_index_if_missing(
        self, data_path: pathlib.Path, destination: pathlib.Path
    ):
        is_empty = len(list(destination.iterdir())) == 0
        if not is_empty:
            return
        log.info("Creating index at: %s", destination)
        with open(data_path, "rt") as f:
            data = json.load(f)

        articles = [core.Article(**d) for d in data]
        articles_text = [str(a) for a in articles]

        article_embeddings = self.model.encode(articles_text)
        numpy.save(destination / self._emb_filename, article_embeddings)

        article_dicts = [dataclasses.asdict(a) for a in articles]
        with open(destination / self._index_data_filename, "wt") as f:
            json.dump(article_dicts, f)


class WhooshIndex(
    core.AbstractIndex
):  # pylint: disable=too-few-public-methods
    """Lexical Search indexing with Whoosh"""

    schema = F.Schema(
        title=F.TEXT(stored=True),
        clauses=F.TEXT(stored=True),
        chapter=F.TEXT(stored=True),
        part=F.TEXT(stored=True),
        number=F.STORED,
    )

    def __init__(
        self, data_pathname: FileSystemPath, index_dirname: FileSystemPath
    ):
        """Initialize the index, creating it if necessary"""

        index_dir = pathlib.Path(index_dirname)
        data_path = pathlib.Path(data_pathname)
        _ensure_exists(index_dir)
        self._create_index_if_missing(data_path, index_dir)
        self._index = whoosh_index.open_dir(index_dirname)
        self._search_fields = ["title", "clauses", "chapter", "part"]

    def _create_index_if_missing(
        self, data_path: pathlib.Path, destination: pathlib.Path
    ):
        is_empty = len(list(destination.iterdir())) == 0
        if is_empty:
            log.info("Creating index at: %s", destination)
            with open(data_path, "rt") as f:
                data = json.load(f)

            data_index = whoosh_index.create_in(str(destination), self.schema)
            writer = data_index.writer()
            for doc in data:
                writer.add_document(**doc)
            writer.commit()

    def search(self, query, num_results):
        with self._index.searcher() as searcher:
            parser = qparser.MultifieldParser(
                self._search_fields, schema=self.schema, group=qparser.OrGroup
            )
            query = parser.parse(str(query))
            results = searcher.search(query, limit=num_results)
            results = [core.Article(**dict(r)) for r in results]
        return results


class HybridIndex(core.AbstractIndex):
    # pylint: disable=too-few-public-methods

    LEXICAL_INDEX_CLS = WhooshIndex
    SEMANTIC_INDEX_CLS = SentenceTransformersIndex

    @classmethod
    def from_index_locations(
        cls,
        lexical_index_dirname: FileSystemPath,
        semantic_index_dirname: FileSystemPath,
        data_location: FileSystemPath,
    ):
        """Creates a hybrid index from the given filesystem locations"""

        lexical_index = cls.LEXICAL_INDEX_CLS(
            data_location, lexical_index_dirname
        )
        semantic_index = cls.SEMANTIC_INDEX_CLS(
            data_location, semantic_index_dirname
        )
        return cls(lexical_index, semantic_index)

    def __init__(self, lexical_search_index, semantic_search_index):
        self._lexical_index = lexical_search_index
        self._semantic_index = semantic_search_index

    def search(self, query, num_results):
        lexical_search_results = self._lexical_index.search(query, num_results)
        semantic_search_results = self._semantic_index.search(
            query, num_results
        )
        ranked_results = self._rank_results(
            lexical_search_results, semantic_search_results
        )
        return ranked_results[:num_results]

    @classmethod
    def _rank_results(cls, *result_sets):
        scores: dict[int, float] = {}
        all_articles = {}
        for results in result_sets:
            for i, article in enumerate(results):
                all_articles[article.number] = article
                scores[article.number] = scores.get(
                    article.number, 0
                ) + cls.rrf_score(i + 1)

        sorted_scores = sorted(
            scores.items(), key=lambda num_score: num_score[1], reverse=True
        )
        return [all_articles[number] for number, _ in sorted_scores]

    @staticmethod
    def rrf_score(rank, k=60):
        return 1 / (k + rank)


def _ensure_exists(path: pathlib.Path):
    """Ensure that the given destination exists on the file system"""
    if not path.exists():
        path.mkdir(parents=True)
