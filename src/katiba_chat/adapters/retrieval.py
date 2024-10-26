"""Retrieval adapters"""
import pathlib

from whoosh import fields as F
from whoosh import index as whoosh_index
from whoosh import qparser


from .. import core


class WhooshIndex(core.AbstractIndex):
    """Lexical Search indexing with Whoosh"""

    schema = F.Schema(
        title=F.TEXT(stored=True),
        clauses=F.TEXT(stored=True),
        chapter=F.TEXT(stored=True),
        part=F.TEXT(stored=True),
        number=F.STORED,
    )

    def __init__(self, data: list[dict], index_dirname: str | pathlib.Path):
        """Initialize the index, creating it if necessary"""

        path = pathlib.Path(index_dirname)
        if not path.exists():
            path.mkdir(parents=True)

        is_empty = len(list(path.iterdir())) == 0
        if is_empty:
            # create index
            data_index = whoosh_index.create_in(index_dirname, self.schema)
            writer = data_index.writer()
            for doc in data:
                writer.add_document(**doc)
            writer.commit()

        self._index = whoosh_index.open_dir(index_dirname)
        self._search_fields = ['title', 'clauses', 'chapter', 'part']
        
    def search(self, query, num_results):
        with self._index.searcher() as searcher:
            parser = qparser.MultifieldParser(self._search_fields, schema=self.schema, group=qparser.OrGroup)
            query = parser.parse(str(query))
            results = searcher.search(query, limit=num_results)
            results = [dict(r) for r in results]            
        return results
