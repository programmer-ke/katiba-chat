from katiba_chat import core
from katiba_chat.adapters import retrieval


def test_can_search_whoosh_index(temp_dir_name, constitution_articles):
    whoosh_index = retrieval.WhooshIndex(constitution_articles, temp_dir_name)
    query = core.Query("Who holds sovereign power")
    num_results = 3
    results = whoosh_index.search(query, num_results)
    assert len(results) == num_results