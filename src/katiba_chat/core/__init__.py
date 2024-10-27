"""Entity and Use Case Layer"""
from collections.abc import Iterable
from dataclasses import dataclass
import textwrap
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
    part: str | None = None

    def __str__(self):
        fmt = textwrap.dedent(f"""
        Chapter: {self.chapter}
        Part: {self.part}
        Title: {self.title}
        Number: {self.number}
        Clauses: {{}}
        """)
        return fmt.format(self.clauses).strip()


class AbstractIndex(Protocol):
    def search(self, query: Query, num_results: int) -> Iterable[Article]:
        ...


def search(index: AbstractIndex, query: Query, num_results: int = 5) -> Iterable[Article]:
    return index.search(query, num_results)
