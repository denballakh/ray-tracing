from __future__ import annotations
from typing import Iterator

import math

from rangers.std.mixin import PrintableMixin

from .point import Point

class Ray(PrintableMixin):
    brightness: float
    start: Point
    end: Point | None
    _direction: Point

    def __init__(
        self,
        start: Point,
        direction: Point,
        brightness: float,
    ) -> None:
        self.brightness = brightness
        self.start = start
        self.direction = direction
        self.end = None

    @property
    def direction(self) -> Point:
        return self._direction

    @direction.setter
    def direction(self, other: Point) -> None:
        self._direction = other.norm()

