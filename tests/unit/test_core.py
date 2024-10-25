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
