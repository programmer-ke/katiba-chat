"""Test various helper utilities"""

from katiba_chat import core
from katiba_chat.adapters import retrieval


def test_rrf_score():
    # formula: 1 / (k + rank)
    k = 60
    expected_top_5 = [1 / (k + i + 1) for i in range(5)]
    rrf_func = retrieval.HybridIndex.rrf_score
    actual = [rrf_func(i + 1) for i in range(5)]
    assert expected_top_5 == actual


def test_hybrid_results_ranking():

    results_1 = [
        core.Article("foo", "bar", "quux", i + 1, "baz") for i in range(3)
    ]  # -> 1, 2, 3
    results_2 = results_1[1:]  # -> 2, 3

    # pylint: disable=protected-access
    ranking_func = retrieval.HybridIndex._rank_results
    ranked_results = ranking_func(results_1, results_2)
    expected_order = [2, 3, 1]

    assert len(ranked_results) == len(expected_order)
    for i, r in enumerate(ranked_results):
        assert r.number == expected_order[i]
