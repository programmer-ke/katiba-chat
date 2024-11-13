"""Gradio front-end"""

import time
from collections.abc import Iterable

import gradio as gr

from .. import core
from ..adapters import generation, retrieval
from . import common

st_index_dirname = common.user_data_dir("sentence_transformers_index")
whoosh_index_dirname = common.user_data_dir("whoosh_index")

hybrid_index = retrieval.HybridIndex.from_index_locations(
    whoosh_index_dirname, st_index_dirname, data_location=common.ARTICLES_PATH
)

RESPONSE_TEMPLATE = """
{llm_response}
<small>The above is AI-generated content. Please verify critical facts</small>

**Context**:
{context}
"""


def rag(question: str, history):  # pylint: disable=unused-argument

    if not question:
        yield "I cannot read your mind (yet 😎!). What would you like to know?"
        return

    query = core.Query(question)

    retrieval_results = core.search(hybrid_index, query)
    prompt = core.Prompt(common.PROMPT_TEMPLATE, query, retrieval_results)
    llm = generation.OpenAICompatibleLLM(
        common.LLM_MODEL_NAME, common.LLM_API_KEY, common.LLM_BASE_URL
    )
    response = core.generate(llm, prompt)
    llm_response_text = str(response)
    references_text = _format_references(retrieval_results)
    response_text = RESPONSE_TEMPLATE.format(
        llm_response=llm_response_text, context=references_text
    )
    chunk_size = 10
    for i in range(chunk_size, len(response_text) + chunk_size, chunk_size):
        yield response_text[:i]
        time.sleep(0.05)


def _format_references(retrieval_results: Iterable[core.Article]) -> str:
    return "\n".join([r.title for r in retrieval_results])


example_questions = [
    "Who holds sovereign power?",
    "What are the freedom of speech guarantees?",
    "What information must be promptly provided to an arrested person?",
    "What is the role of the Senate?",
    "How are public contracts for goods and services awarded?",
]


if __name__ == "__main__":
    gr.ChatInterface(
        rag,
        type="messages",
        examples=example_questions,
        title="katiba.KE",
        description=(
            "<p style='text-align:center'>"
            "Stay informed on the Kenyan 2010 Constitution</p>"
        ),
    ).launch()
