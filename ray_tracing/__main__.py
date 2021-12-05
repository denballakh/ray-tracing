from __future__ import annotations

import os
import sys

from pprint import pprint

from rangers.std.decorator import profile

from ray_tracing.point import Point
from ray_tracing.ray import Ray
from ray_tracing.obstacle import Obstacle, CircleObstacle, LineObstacle
from ray_tracing.model import Model

import ray_tracing


@profile(filename='build/rt.log')
def main():
    source: Point = Point(0.5, 0.5)
    obstacles: list[Obstacle] = [
        LineObstacle(Point(0.0, 0.0), Point(0.0, 0.2)),
        LineObstacle(Point(0.0, 0.0), Point(0.2, 0.0)),
        CircleObstacle(Point(0.0, 0.4), 0.2),
        CircleObstacle(Point(0.0, 0.8), 0.2),
        CircleObstacle(Point(0.2, 1.0), 0.2),
        CircleObstacle(Point(0.6, 1.0), 0.2),
        CircleObstacle(Point(1.0, 1.0), 0.2),
        CircleObstacle(Point(1.0, 0.6), 0.2),
        CircleObstacle(Point(1.0, 0.2), 0.2),
        CircleObstacle(Point(0.8, 0.0), 0.2),
        CircleObstacle(Point(0.4, 0.0), 0.2),
    ]
    obstacles = [
        LineObstacle(Point(0.2,0.2), Point(0.2,0.8)),
        # LineObstacle(Point(0.2,0.8), Point(0.2,0.2)),
        LineObstacle(Point(1,1), Point(0,1)),
        LineObstacle(Point(1,1), Point(1,0)),
        LineObstacle(Point(0,0), Point(1,0)),
        # LineObstacle(Point(0.2,0.3), Point(0.3,0.33)),
        CircleObstacle(Point(1,1), 0.01),
        CircleObstacle(Point(0,1), 0.01),
        CircleObstacle(Point(1,0), 0.01),
        CircleObstacle(Point(0,0), 0.01),
    ]
    model = Model(source, obstacles)
    model.process()

    img = model.draw_end()
    # img = model.draw.image
    img.show()


if __name__ == '__main__':
    main()
