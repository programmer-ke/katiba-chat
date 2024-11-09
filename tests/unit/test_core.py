"""Test core package"""

from katiba_chat import core

NUM_ARTICLES = 264


def article_factory(number):
    return [
        core.Article("foo", "bar", "quux", i + 1, "baz") for i in range(number)
    ]


class FakeIndex(core.AbstractIndex):  # pylint: disable=too-few-public-methods
    def __init__(self):
        self._index = article_factory(264)

    def search(self, query, num_results=5):  # pylint: disable=unused-argument
        return self._index[:num_results]


class FakeLLM(core.AbstractLLM):  # pylint: disable=too-few-public-methods

    def generate(self, prompt):  # pylint: disable=unused-argument
        # simply returns the first item in the context
        context_item = prompt.context[0]
        return core.LLMResponse(str(context_item))


def test_returns_default_results_num():
    query = core.Query("Who holds sovereign power?")
    index = FakeIndex()
    num_results = 3
    results = core.search(index, query, num_results)
    assert len(list(results)) == num_results
    assert all(isinstance(r, core.Article) for r in results)


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
        part="quux",
    )

    text = str(article)
    assert all(
        attr in text
        for attr in (
            article.title,
            article.clauses,
            article.chapter,
            article.part,
            str(article.number),
        )
    )


def test_can_create_prompt():
    prompt_template = """
    some prompt
    {query}

    {context}
    """
    query = core.Query("foo")
    context = article_factory(3)
    prompt = core.Prompt(prompt_template, query, context)

    assert prompt.template == prompt_template
    assert prompt.query == query
    assert prompt.context == context

    prompt_text = str(prompt)
    assert "some prompt" in prompt_text
    assert "foo" in prompt_text
    article1, *_ = context
    assert article1.title in prompt_text
    assert str(article1.number) in prompt_text


def test_generation_from_prompt():
    prompt_template = """
    some prompt
    {query}

    {context}
    """
    query = core.Query("foo")
    context = article_factory(3)
    prompt = core.Prompt(prompt_template, query, context)
    llm = FakeLLM()
    response = core.generate(llm, prompt)
    assert response.text
