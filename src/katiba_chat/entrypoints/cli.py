"""CLI Interface"""

import sys

from .. import core
from ..adapters import generation, retrieval
from . import common

st_index_dirname = common.user_data_dir("sentence_transformers_index")
whoosh_index_dirname = common.user_data_dir("whoosh_index")

hybrid_index = retrieval.HybridIndex.from_index_locations(
    whoosh_index_dirname, st_index_dirname, data_location=common.ARTICLES_PATH
)


def entrypoint(question: str):

    query = core.Query(question)

    retrieval_results = core.search(hybrid_index, query)
    prompt = core.Prompt(common.PROMPT_TEMPLATE, query, retrieval_results)
    llm = generation.OpenAICompatibleLLM(
        common.LLM_MODEL_NAME, common.LLM_API_KEY, common.LLM_BASE_URL
    )
    response = core.generate(llm, prompt)
    print(response, file=sys.stdout)
