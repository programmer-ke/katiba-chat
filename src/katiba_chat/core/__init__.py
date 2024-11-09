"""Entity and Use Case Layer"""

import textwrap
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Query:
    text: str

    def __str__(self):
        return self.text


@dataclass
class Article:
    title: str
    clauses: str
    chapter: str
    number: int
    part: str

    def __str__(self):
        fmt = textwrap.dedent(
            f"""
        Chapter: {self.chapter}
        Part: {self.part}
        Title: {self.title}
        Number: {self.number}
        Clauses: {{}}
        """
        )
        return fmt.format(self.clauses).strip()


@dataclass
class Prompt:
    template: str
    query: Query
    context: Iterable[Article]

    def __str__(self):
        return self.template.format(
            query=str(self.query),
            context="\n\n".join([str(item) for item in self.context]),
        )


@dataclass
class LLMResponse:
    text: str

    def __str__(self):
        return self.text


class AbstractIndex(Protocol):  # pylint: disable=too-few-public-methods
    def search(self, query: Query, num_results: int) -> Iterable[Article]: ...


class AbstractLLM(Protocol):  # pylint: disable=too-few-public-methods
    def generate(self, prompt: Prompt) -> LLMResponse: ...


def search(
    index: AbstractIndex, query: Query, num_results: int = 5
) -> Iterable[Article]:
    return index.search(query, num_results)


def generate(
    llm: AbstractLLM,
    prompt: Prompt,
) -> LLMResponse:
    return llm.generate(prompt)
