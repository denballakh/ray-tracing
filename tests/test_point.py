from __future__ import annotations
from typing import TYPE_CHECKING

import time
import random
from itertools import repeat

from rangers.common import is_compiled, rand31pm
from rangers.std.time import AdaptiveTimeMeasurer

from ray_tracing.geometry.point import Point, point

COMPILED = is_compiled(Point)
assert COMPILED != -1

def test_doc() -> None:
    """!
    >>> Point(0, 0)
    Point(0, 0)
    >>> print(Point(0, 0))
    <Point: x=0, y=0>
    >>> Point(1, 2) + Point(3, 4)
    Point(4, 6)
    >>> Point(0, 1).norm
    Point(0.0, 1.0)
    >>> Point(0, 1).abs
    1.0
    >>> Point(1, 0).angle
    0.0
    >>> Point(0, 0).norm
    Traceback (most recent call last):
      ...
    ValueError: norm of zero point is undefined
    >>> Point(1, 2) / 0
    Traceback (most recent call last):
      ...
    ZeroDivisionError: point cannot be divided by zero

    """


def test_speed() -> None:
    # make vars local to improve load speed
    from ray_tracing.geometry.point import Point, point

    with AdaptiveTimeMeasurer(
        target_time=0.3,
        config_file='benchmarks/point_compiled.json' if COMPILED else 'benchmarks/point.json',
    ) as atm:
        print(f'Compiled: {["no", "yes"][COMPILED]}')
        print()

        rndgen = rand31pm(random.randint(0, 2 ** 31 - 1))  # 4x times faster than random.randint

        T = atm('empty loop', extra=2)
        T.calibrate(0)
        with T as cnt:
            for _ in repeat(None, cnt):
                pass
        assert T.time is not None
        T.calibrate(T.time)

        with atm('calibrated empty loop') as cnt:
            for _ in repeat(None, cnt):
                pass

        with atm('next(rndgen)') as cnt:
            for _ in repeat(None, cnt):
                next(rndgen)

        print()

        with atm('Point(0, 0)') as cnt:
            for _ in repeat(None, cnt):
                Point(0, 0)

        with atm('Point(next(rndgen), next(rndgen))') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen))

        print()

        with atm('point(0, 0)') as cnt:
            for _ in repeat(None, cnt):
                point(0, 0)

        with atm('point(next(rndgen), next(rndgen))') as cnt:
            for _ in repeat(None, cnt):
                point(next(rndgen), next(rndgen))

        print()

        with atm('p1 + p2') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)) + Point(next(rndgen), next(rndgen))

        with atm('p1 - p2') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)) - Point(next(rndgen), next(rndgen))

        with atm('p1 @ p2') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)) @ Point(next(rndgen), next(rndgen))

        print()

        with atm('p.norm') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)).norm

        with atm('p.angle') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)).angle

        with atm('p.abs') as cnt:
            for _ in repeat(None, cnt):
                Point(next(rndgen), next(rndgen)).abs



if __name__ == '__main__':
    import doctest
    import os

    res = doctest.testmod()

    if res.failed == 0:
        test_speed()

    input('Press enter to exit...')
    os._exit(res.failed)
