from katiba_chat import core


NUM_ARTICLES = 264


class FakeIndex(core.AbstractIndex):
    def __init__(self):
        self._index = [core.Article('foo', 'bar', 'quux', i+1, 'baz') for i in range(264)]
        
    def search(self, query, num_results=5):
        return self._index[:num_results]
        

def test_returns_default_results_num():
    query = core.Query("Who holds sovereign power?")
    index = FakeIndex()
    num_results = 3
    results = core.search(index, query, num_results)
    assert len(list(results)) == num_results
    assert all([isinstance(r, core.Article) for r in results])


def test_stringified_query():
    text = "who holds sovereign power?"
    q = core.Query(text=text)
    assert str(q) == text

def test_stringified_article():
    article = core.Article(
        title="title",
        clauses="clause a b c",
        chapter="Chapter 1: foobar",
        number=23,
        part="quux"
    )

    text = str(article)
    assert all([attr in text for attr in (article.title, article.clauses, article.chapter, article.part, str(article.number))])
