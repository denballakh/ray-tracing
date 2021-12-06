cimport cython
from typing import Iterator

__all__ = ('Point',)

DEF PI = (3.141592653589793)
DEF PI2 = (6.283185307179586)

cdef extern from "math.h":
    cdef double sqrt(double)
    cdef double sin(double)
    cdef double cos(double)
    cdef double atan2(double, double)
    cdef int isnan(double)
    cdef double nan "NAN"

cdef inline double sqr(double x):
    return x * x


cdef class Point:
    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y
        self._abs = nan
        self._angle = nan
        self._norm = None

    @classmethod
    def from_angle(
        cls: type[Point],
        double angle,
        double magn = 1.0,
    ) -> Point:
        result = Point(
            cos(angle) * magn,
            sin(angle) * magn,
        )
        result._abs = magn
        result._angle = angle
        if magn == 1.0:
            result._norm = result

        return result

    @classmethod
    def from_tuple(cls: type[Point], tup: tuple[double, double]) -> Point:
        return Point(tup[0], tup[1])

    def __str__(self) -> str: return self.str()
    def __repr__(self) -> str: return self.repr()
    def __hash__(self) -> int: return self.hash()
    def __bool__(self) -> bool: return self.bool()
    def __eq__(self, object other) -> bool: return self.eq(other)
    def __ne__(self, object other) -> bool: return self.ne(other)
    def __abs__(self) -> double: return self.abs()
    def __neg__(self) -> Point: return self.neg()
    def __pos__(self) -> Point: return self
    def __add__(self, other: Point) -> Point: return self.add(other)
    def __sub__(self, other: Point) -> Point: return self.sub(other)
    def __mul__(self, other: double) -> Point: return self.mul(other)
    def __rmul__(self, other: double) -> Point: return self.mul(other)
    def __truediv__(self, other: double) -> Point: return self.div(other)
    def __matmul__(self, other: Point) -> double: return self.scalar(other)
    def __iter__(self) -> Iterator[double]:
        yield self.x
        yield self.y


    cpdef unicode str(self):
        return f'<Point: x={self.x!r}, y={self.y!r}>'

    cpdef unicode repr(self):
        return f'Point({self.x!r}, {self.y!r})'

    cpdef int hash(self):
        return (<int>self.x) ^ (<int>self.y)

    cpdef int bool(self):
        return self.x != 0 and self.y != 0

    cpdef int eq(self, object other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    cpdef int ne(self, object other):
        if isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    cpdef Point neg(self):
        return Point(-self.x, -self.y)

    cpdef Point add(self, Point other):
        return Point(self.x + other.x, self.y + other.y)

    cpdef Point sub(self, Point other):
        return Point(self.x - other.x, self.y - other.y)

    cpdef Point div(self, double factor):
        if factor == 0.0:
            raise ZeroDivisionError(f'point cannot be divided by zero')
        return Point(self.x / factor, self.y / factor)

    cpdef Point mul(self, double factor):
        return Point(self.x * factor, self.y * factor)

    cpdef double scalar(self, Point other):
        return self.x * other.x + self.y * other.y


    cpdef double abs(self):
        if isnan(self._abs):
            self._abs = sqrt(sqr(self.x) + sqr(self.y))
        return self._abs

    cpdef double angle(self):
        if isnan(self._angle):
            self._angle = atan2(self.y, self.x)
        return self._angle

    cpdef Point norm(self):
        if self._norm is None:
            if self.abs() == 0.0:
                raise ValueError(f'norm of zero point is undefined')

            norm = Point(
                self.x / self.abs(),
                self.y / self.abs(),
            )
            norm._norm = norm
            norm._abs = 1.0
            norm._angle = self._angle
            self._norm = norm

        return self._norm

    cpdef double angle_to(self, Point other):
        return other.rotate(-self.angle()).angle()

    cpdef Point rotate(self, double angle):
        return Point.from_angle(self.angle() + angle, self.abs())

    cpdef double dist(self, Point other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
