from __future__ import annotations

from PIL import Image, ImageDraw
from ray_tracing.point import Point


class Draw:
    draw: ImageDraw.ImageDraw

    def __init__(self, size: int) -> None:
        self.draw = ImageDraw.Draw(Image.new('RGB', (size, size), color=(0,0,0)))


    def show(self) -> None:
        self.image.show()

    @property
    def size(self) -> tuple[int, int]:
        return self.image.size

    @property
    def image(self) -> Image.Image:
        return self.draw._image  # type: ignore[attr-defined]

    def draw_point(
        self,
        point: Point,
        color=(255, 255, 255),
    ) -> None:
        self.draw.point(
            (
                round(point.x * (self.size[0]-1)),
                round(point.y * (self.size[1]-1)),
            ),
            fill=color,
        )

    def draw_line(
        self,
        start: Point,
        end: Point,
        color=(255, 255, 255),
    ) -> None:
        self.draw.line(
            (
                round(start.x * (self.size[0] - 1)),
                round(start.y * (self.size[1] - 1)),
                round(end.x * (self.size[0] - 1)),
                round(end.y * (self.size[1] - 1)),
            ),
            fill=color,
        )

    def draw_circle(self, center: Point, radius: float, outline=(255, 255, 255)) -> None:
        self.draw.ellipse(
            (
                round((center.x - radius) * (self.size[0]-1)),
                round((center.y - radius) * (self.size[1]-1)),
                round((center.x + radius) * (self.size[0]-1)),
                round((center.y + radius) * (self.size[1]-1)),
            ),
            outline=outline,
        )
