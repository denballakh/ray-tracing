from __future__ import annotations
from typing import ClassVar

import math

from PIL import Image, ImageDraw

from rangers.std.mixin import PrintableMixin

from .ray import Ray
from .obstacle import Obstacle
from .point import Point
from .queue import Queue
from .draw import Draw


class Model(PrintableMixin):
    RAYS_CNT: ClassVar[int] = 8
    MAX_LEN: ClassVar[int] = 100000

    source: Point
    obstacles: list[Obstacle]
    rays: list[Ray] | None
    draw: Draw

    def __init__(
        self,
        source: Point,
        obstacles: list[Obstacle],
    ) -> None:
        self.source = source
        self.obstacles = obstacles
        self.rays = None
        self.draw = Draw(size=850)

        for obs in self.obstacles:
            obs.model = self

    def process(self) -> None:
        queue = Queue[Ray]()

        for i in range(self.RAYS_CNT):
            queue.put(
                Ray(
                    self.source,
                    Point.from_angle(i / self.RAYS_CNT * math.pi * 2),
                    1.0,
                ),
            )

        for ray in queue:
            intersections = list[tuple[float, Obstacle]]()

            for obs in self.obstacles:
                rl = obs.run_length(ray)
                if rl is None:
                    continue
                intersections.append((rl, obs))

            if not intersections:
                continue

            intersections = sorted(intersections, key=lambda pr: pr[0])
            obs = intersections[0][1]

            rays = obs.reflect(ray)

            for r in rays:
                queue.put(r)

                if len(queue.data) > self.MAX_LEN:
                    break

            if len(queue.data) > self.MAX_LEN:
                break

        queue.reset()
        self.rays = list(queue)
        # print('rays:')
        # print(*queue, sep='\n')

    def draw_end(self) -> Image.Image:
        assert self.rays

        for ray in reversed(self.rays):
            if ray.end is None:
                continue
                ray.end = ray.start + ray.direction * 0.3

            c = round(ray.brightness * 255)
            color = c, c, c, 255 - c
            self.draw.draw_line(
                ray.start,
                ray.end,
                color=color,
            )

        for obs in self.obstacles:
            obs.draw()

        return self.draw.image
