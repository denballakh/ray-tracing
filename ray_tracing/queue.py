from __future__ import annotations
from typing import Any, Callable, Generic, Iterator, TypeVar

T = TypeVar('T')


class Queue(Generic[T]):
    data: list[T]
    pos: int

    def __init__(self) -> None:
        self.data = []
        self.pos = 0

    def put(self, obj: T) -> None:
        self.data.append(obj)

    def get(self) -> T:
        result = self.data[self.pos]
        self.pos += 1
        return result

    def __iter__(self) -> Iterator[T]:
        while self.pos < len(self.data):
            yield self.data[self.pos]
            self.pos += 1

    def reset(self) -> None:
        self.pos = 0

