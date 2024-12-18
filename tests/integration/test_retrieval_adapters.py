"""Retrieval adapters integration tests """

import os

from katiba_chat import core
from katiba_chat.adapters import retrieval


def test_can_search_whoosh_index(temp_dir_name, constitution_articles_path):
    whoosh_index = retrieval.WhooshIndex(
        constitution_articles_path, temp_dir_name
    )
    query = core.Query("Who holds sovereign power")
    num_results = 3
    results = whoosh_index.search(query, num_results)
    assert len(results) == num_results
    assert all(isinstance(r, core.Article) for r in results)


def test_can_search_sentence_transformers_index(
    temp_dir_name, constitution_articles_path
):
    st_transformers_index = retrieval.SentenceTransformersIndex(
        constitution_articles_path, temp_dir_name
    )
    query = core.Query("Who holds sovereign power")
    num_results = 3
    results = st_transformers_index.search(query, num_results)
    assert len(results) == num_results
    assert all(isinstance(r, core.Article) for r in results)


def test_can_search_hybrid_index(temp_dir_name, constitution_articles_path):
    whoosh_index = retrieval.WhooshIndex(
        constitution_articles_path, os.path.join(temp_dir_name, "whoosh")
    )
    st_transformers_index = retrieval.SentenceTransformersIndex(
        constitution_articles_path,
        os.path.join(temp_dir_name, "st_transformers"),
    )

    hybrid_index = retrieval.HybridIndex(whoosh_index, st_transformers_index)
    query = core.Query("Who holds sovereign power")
    num_results = 3
    results = hybrid_index.search(query, num_results)
    assert len(results) == num_results
    assert all(isinstance(r, core.Article) for r in results)
