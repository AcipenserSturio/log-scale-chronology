import csv
from pathlib import Path

from PIL import Image, ImageDraw
import tomli

from .date import Date
from .stratigraphy import Tree
from .config import (
    FONT, WIDTH, HEIGHT,
    BACKGROUND_COLOR, COLOR, SEMI_TRANSPARENT,
    YEAR_TACKS,
)
YEAR_TACKS = list(map(Date, YEAR_TACKS))


def draw_tack(draw: ImageDraw.Draw, text: str, y: int, x_offset: int = 0):
    draw.line(
        ((0 + x_offset, y), (5 + x_offset, y)),
        fill=COLOR,
    )
    draw.text(
        (10 + x_offset, y),
        text,
        fill=COLOR,
        font=FONT,
        anchor="lm",
    )

def draw_text(draw: ImageDraw.Draw, text: str, x: int, y: int):
    draw.text(
        (x, y),
        text,
        fill=COLOR,
        font=FONT,
        anchor="lm",
    )

def draw_tacks(draw: ImageDraw.Draw,
               tacks: list[tuple[Date, str]],
               x_offset: int):
    draw.line(
        ((x_offset, 0), (x_offset, HEIGHT)),
        fill=COLOR,
    )
    for date, description in tacks:
        draw_tack(draw, description, date.y, x_offset=x_offset)


MAGNIFIER = 10
def draw_csv(im: Image,
             offset: int,
             filepath: Path,
             ) -> Image:

    im_over = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im_over)

    with open(filepath) as f:
        data = csv.reader(f)
        unit, _ = next(data)
        prev_date, prev_temp = next(data)
        for date, temp in data:
            draw.line(
                ((offset + float(prev_temp) * MAGNIFIER,
                  Date(f"{prev_date} {unit}").y),
                 (offset + float(temp) * MAGNIFIER,
                  Date(f"{date} {unit}").y)),
                fill=SEMI_TRANSPARENT,
            )
            prev_date, prev_temp = date, temp
    im.alpha_composite(im_over)


def plot():
    im = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    # draw_node(im, draw, 0, 0)

    with open("assets/stratigraphy.toml", "rb") as f:
        strat = Tree(tomli.load(f))

    for span in strat.eons:
        draw.rectangle(
            ((0, span.start.y),
            (200, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                10,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.eras:
        draw.rectangle(
            ((200, span.start.y),
            (400, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                210,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.periods:
        draw.rectangle(
            ((400, span.start.y),
            (600, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                410,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.epochs:
        draw.rectangle(
            ((600, span.start.y),
            (800, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                610,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.ages:
        draw.rectangle(
            ((800, span.start.y),
            (1000, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                810,
                (span.start.y + span.end.y) / 2,
            )

    draw_tacks(
        draw,
        [(date, date.string) for date in YEAR_TACKS],
        1000
    )

    for filepath in Path("assets/paleotemps").glob("*.csv"):
        draw_csv(im, 1200, filepath)

    with open("assets/events.toml", "rb") as f:
        events = tomli.load(f)

    draw_tacks(
        draw,
        [(Date(date), desc) for date, desc in events.items()],
        1450
    )

    im.save("out.png")


if __name__ == "__main__":
    plot()
