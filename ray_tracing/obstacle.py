from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Iterable
import math

# from random import uniform

from PIL import Image, ImageDraw

from .ray import Ray
from .point import Point

if TYPE_CHECKING:
    from .model import Model


class Obstacle(ABC):
    _model: Model

    @property
    def model(self) -> Model:
        try:
            return self._model
        except:
            return None

    @model.setter
    def model(self, model: Model) -> None:
        self._model = model

    @abstractmethod
    def reflect(self, ray: Ray) -> list[Ray]:
        pass

    @abstractmethod
    def run_length(self, ray: Ray) -> float | None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class CircleObstacle(Obstacle):
    BR_DECAY: ClassVar[float] = 0.7
    BR_MIN: ClassVar[float] = 0.01
    RAYS_CNT: ClassVar[int] = 6
    ANGLE_DIFF: ClassVar[float] = 0.1

    center: Point
    radius: float

    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius

    def reflect(self, ray: Ray) -> list[Ray]:
        t = self.run_length(ray)
        assert t is not None

        result = list[Ray]()

        collision = ray.start + t * ray.direction
        ray.end = collision
        radius = collision - self.center
        dir = ray.direction

        for i in range(self.RAYS_CNT):
            dang = (
                self.ANGLE_DIFF * 2 * (i / (self.RAYS_CNT - 1) - 0.5) if self.RAYS_CNT != 1 else 0
            )
            newdir = Point.from_angle((-dir).angle() + 2 * (-dir).angle_to(radius) + dang)
            if newdir @ radius < 0:
                newdir = -newdir
                assert newdir @ radius > 0

            newray = Ray(collision, newdir, ray.brightness * self.BR_DECAY)

            if newray.brightness >= self.BR_MIN:
                result.append(newray)
        return result

    def run_length(self, ray: Ray) -> float | None:
        dist = (self.center - ray.start).abs() * math.sin(
            ray.direction.angle_to(self.center - ray.start),
        )

        px, py = ray.direction
        x0, y0 = ray.start
        xc, yc = self.center
        r = self.radius

        t1 = (
            px ** 2 * (-x0 + xc)
            + px * py * (-y0 + yc)
            + (
                px ** 2
                * (
                    py ** 2 * (r + x0 - xc) * (r - x0 + xc)
                    + 2 * px * py * (x0 - xc) * (y0 - yc)
                    + px ** 2 * (r + y0 - yc) * (r - y0 + yc)
                )
            )
            ** 0.5
        ) / (px * (px ** 2 + py ** 2))

        t2 = (
            px ** 2 * (-x0 + xc)
            + px * py * (-y0 + yc)
            - (
                px ** 2
                * (
                    py ** 2 * (r + x0 - xc) * (r - x0 + xc)
                    + 2 * px * py * (x0 - xc) * (y0 - yc)
                    + px ** 2 * (r + y0 - yc) * (r - y0 + yc)
                )
            )
            ** 0.5
        ) / (px * (px ** 2 + py ** 2))

        s: Iterable = {t1, t2}

        s = filter(lambda x: isinstance(x, float), s)
        s = filter(lambda x: x >= 0.00001, s)
        s = set(s)

        if not s:
            return None

        return min(s)

    def draw(self) -> None:
        self.model.draw.draw_circle(self.center, self.radius, outline=(255, 0, 0))


class LineObstacle(Obstacle):
    BR_DECAY: ClassVar[float] = 0.7
    BR_MIN: ClassVar[float] = 0.01
    RAYS_CNT: ClassVar[int] = 6
    ANGLE_DIFF: ClassVar[float] = 0.1

    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def reflect(self, ray: Ray) -> list[Ray]:
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = ray.start
        x3, y3 = ray.start + ray.direction
        t = (x3 * (y0 - y2) + x0 * (y2 - y3) + x2 * (-y0 + y3)) / (
            -((x2 - x3) * (y0 - y1)) + (x0 - x1) * (y2 - y3) + 0.000001
        )

        collision = self.p1 + (self.p2 - self.p1) * t
        ray.end = collision

        dir = ray.direction

        result = list[Ray]()
        for i in range(self.RAYS_CNT):
            dang = (
                self.ANGLE_DIFF * 2 * (i / (self.RAYS_CNT - 1) - 0.5) if self.RAYS_CNT != 1 else 0
            )
            newdir = -Point.from_angle(
                (-dir).angle() + 2 * (-dir).angle_to(self.p1 - self.p2) + dang
            )
            # newdir = Point.from_angle(uniform(0, 6.28))
            newray = Ray(collision, newdir, ray.brightness * self.BR_DECAY)
            if ray.brightness > self.BR_MIN:
                result.append(newray)

        # print('reflection', ray, self, uniform(0, 1))
        # print(newray)
        return result

    def run_length(self, ray: Ray) -> float | None:
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = ray.start
        x3, y3 = ray.start + ray.direction
        t = (x3 * (y0 - y2) + x0 * (y2 - y3) + x2 * (-y0 + y3)) / (
            -((x2 - x3) * (y0 - y1)) + (x0 - x1) * (y2 - y3) + 0.000001
        )
        t2 = (x2 * (y0 - y1) + x0 * (y1 - y2) + x1 * (-y0 + y2)) / (
            (x2 - x3) * (y0 - y1) - (x0 - x1) * (y2 - y3) + 0.000001
        )
        if t2 < 0.01:
            return None

        if t < 0.01:
            return None

        if t >= 0.99:
            return None

        return t2

    def draw(self) -> None:
        self.model.draw.draw_line(self.p1, self.p2, color=(255, 0, 0))
