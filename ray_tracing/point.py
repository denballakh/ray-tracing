from __future__ import annotations
from typing import Iterator

import math

from rangers.std.mixin import PrintableMixin

class Point(PrintableMixin):
    __slots__ = ('x', 'y')

    x: float
    y: float

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_angle(
        cls,
        angle: float,
        magn: float = 1,
    ) -> Point:
        return Point(
            math.cos(angle) * magn,
            math.sin(angle) * magn,
        )

    @classmethod
    def from_tuple(cls, tup: tuple[float, float]) -> Point:
        return cls(tup[0], tup[1])

    def __add__(self, other: Point) -> Point:
        return Point(
            self.x + other.x,
            self.y + other.y,
        )

    def __mul__(self, other: float) -> Point:
        return Point(
            self.x * other,
            self.y * other,
        )

    def __neg__(self) -> Point:
        return self * (-1.0)

    def __pos__(self) -> Point:
        return self

    def __sub__(self, other: Point) -> Point:
        return self + (-other)

    def __rmul__(self, other: float) -> Point:
        return self * other

    def __truediv__(self, other: float) -> Point:
        return self * (1.0 / other)

    def __matmul__(self, other: Point) -> float:
        return self.x * other.x + self.y * other.y

    def abs(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __abs__(self) -> float:
        return self.abs()

    def angle_to(self, other: Point) -> float:
        return other.rotate(-self.angle()).angle() % (2 * math.pi)

    def angle(self) -> float:
        assert -math.pi <= math.atan2(self.y, self.x) <= math.pi
        return math.atan2(self.y, self.x) % (2 * math.pi)

    def norm(self) -> Point:
        return Point(
            self.x / self.abs(),
            self.y / self.abs(),
        )

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def rotate(self, angle: float) -> Point:
        return Point.from_angle(self.angle() + angle, self.abs())
