"""Tests for generation adapters"""

from katiba_chat.adapters import generation


def test_can_create_openai_request_args():

    request_args = generation.OpenAICompatibleLLM.format_completions_request(
        model_name="foo", prompt="bar"
    )

    assert request_args == {
        "model": "foo",
        "messages": [{"role": "user", "content": "bar"}],
    }
