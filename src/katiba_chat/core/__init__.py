"""Entity and Use Case Layer"""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol
    

@dataclass
class Query:
    text: str


@dataclass
class Article:
    title: str
    clauses: str
    chapter: str
    number: int
    part: str | None = None



class AbstractIndex(Protocol):
    def search(self, query: Query, num_results: int) -> Iterable[Article]:
        ...


def search(index: AbstractIndex, query: Query, num_results: int = 5) -> Iterable[Article]:
    return index.search(query, num_results)
