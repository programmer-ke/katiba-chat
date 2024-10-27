"""Retrieval adapters"""

import json
import logging
import pathlib

from whoosh import fields as F
from whoosh import index as whoosh_index
from whoosh import qparser

from .. import core

log = logging.getLogger(__name__)


class WhooshIndex(core.AbstractIndex):
    """Lexical Search indexing with Whoosh"""

    schema = F.Schema(
        title=F.TEXT(stored=True),
        clauses=F.TEXT(stored=True),
        chapter=F.TEXT(stored=True),
        part=F.TEXT(stored=True),
        number=F.STORED,
    )

    def __init__(self, data_pathname: str, index_dirname: str | pathlib.Path):
        """Initialize the index, creating it if necessary"""

        index_dir = pathlib.Path(index_dirname)
        data_path = pathlib.Path(data_pathname)
        self._ensure_exists(index_dir)
        self._create_index_if_missing(data_path, index_dir)
        self._index = whoosh_index.open_dir(index_dirname)
        self._search_fields = ["title", "clauses", "chapter", "part"]

    def _create_index_if_missing(
        self, data_path: pathlib.Path, destination: pathlib.Path
    ):
        is_empty = len(list(destination.iterdir())) == 0
        if is_empty:
            log.info(f"Creating index at {destination}")
            with open(data_path, "rt") as f:
                data = json.load(f)

            data_index = whoosh_index.create_in(str(destination), self.schema)
            writer = data_index.writer()
            for doc in data:
                writer.add_document(**doc)
            writer.commit()

    def _ensure_exists(self, path: pathlib.Path):
        if not path.exists():
            path.mkdir(parents=True)

    def search(self, query, num_results):
        with self._index.searcher() as searcher:
            parser = qparser.MultifieldParser(
                self._search_fields, schema=self.schema, group=qparser.OrGroup
            )
            query = parser.parse(str(query))
            results = searcher.search(query, limit=num_results)
            results = [core.Article(**dict(r)) for r in results]
        return results
