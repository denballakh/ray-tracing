from __future__ import annotations
from typing import Final, Iterator, final

from math import sin, cos, atan2
from functools import cache, cached_property, lru_cache

__all__ = (
    'Point',
    'point',
)

PI: Final[float] = 3.141592653589793
PI2: Final[float] = 2 * PI


@lru_cache(maxsize=2 ** 15)
def point(x: float, y: float) -> Point:
    """
    Cached constructor of Point
    Caches results to avoid re-constructing same points
    """
    return Point(x, y)


@final
class Point:
    """
    2D point represented as two float
    Immutable
    """

    __slots__ = (
        'x',
        'y',
        '_abs',
        '_angle',
        '_norm',
    )

    x: float
    y: float
    _abs: float | None
    ## may be not in (-pi,pi] or [0,2*pi) diapason
    _angle: float | None
    _norm: Point | None

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self._abs = None
        self._angle = None
        self._norm = None

    @classmethod
    def from_angle(
        cls,
        angle: float,
        magn: float = 1.0,
    ) -> Point:
        result = point(
            cos(angle) * magn,
            sin(angle) * magn,
        )
        result._abs = magn
        result._angle = angle
        if magn == 1.0:
            result._norm = result

        return result

    @classmethod
    def from_tuple(cls, tup: tuple[float, float]) -> Point:
        return point(tup[0], tup[1])

    def __str__(self) -> str:
        return f'<Point: x={self.x!r}, y={self.y!r}>'

    def __repr__(self) -> str:
        return f'Point({self.x!r}, {self.y!r})'

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __iter__(self) -> Iterator[float]:
        """!
        x, y = Point(1, 2)
        assert x == 1 and y == 2
        """
        yield self.x
        yield self.y

    def __abs__(self) -> float:
        return self.abs

    def __neg__(self) -> Point:
        return point(
            -self.x,
            -self.y,
        )

    def __pos__(self) -> Point:
        return self

    def __add__(self, other: Point) -> Point:
        return point(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Point) -> Point:
        return point(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, other: float) -> Point:
        return point(
            self.x * other,
            self.y * other,
        )

    def __rmul__(self, other: float) -> Point:
        return point(
            self.x * other,
            self.y * other,
        )

    def __truediv__(self, other: float) -> Point:
        return point(
            self.x / other,
            self.y / other,
        )

    def __matmul__(self, other: Point) -> float:
        return self.x * other.x + self.y * other.y

    @property
    def abs(self) -> float:
        if self._abs is None:
            self._abs = (self.x ** 2 + self.y ** 2) ** 0.5
        return self._abs

    @property
    def angle(self) -> float:
        if self._angle is None:
            self._angle = atan2(self.y, self.x)
        return self._angle

    @property
    def norm(self) -> Point:
        if self._norm is None:
            norm = self._norm = point(
                self.x / self.abs,
                self.y / self.abs,
            )
            norm._norm = norm
            norm._abs = 1.0
            norm._angle = self._angle

        return self._norm

    def angle_to(self, other: Point) -> float:
        return other.rotate(-self.angle).angle

    def rotate(self, angle: float) -> Point:
        return Point.from_angle(self.angle + angle, self.abs)
