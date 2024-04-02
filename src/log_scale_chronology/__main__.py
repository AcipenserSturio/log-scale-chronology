from PIL import Image, ImageDraw
import tomli

from .date import Date
from .stratigraphy import Tree
from .config import (
    FONT, WIDTH, HEIGHT,
    BACKGROUND_COLOR, COLOR,
    YEAR_TACKS,
)
YEAR_TACKS = list(map(Date, YEAR_TACKS))


def draw_tack(draw: ImageDraw.Draw, text: str, y: int):
    draw.line(
        ((0, y), (5, y)),
        fill=COLOR,
    )
    draw.text(
        (10, y),
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


def plot():
    im = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    # draw_node(im, draw, 0, 0)

    with open("assets/stratigraphy.toml", "rb") as f:
        strat = Tree(tomli.load(f))

    for span in strat.eons:
        draw.rectangle(
            ((100, span.start.y),
            (300, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                110,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.eras:
        draw.rectangle(
            ((300, span.start.y),
            (500, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                310,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.periods:
        draw.rectangle(
            ((500, span.start.y),
            (700, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                510,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.epochs:
        draw.rectangle(
            ((700, span.start.y),
            (900, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                710,
                (span.start.y + span.end.y) / 2,
            )

    for span in strat.ages:
        draw.rectangle(
            ((900, span.start.y),
            (1100, span.end.y)),
            fill=span.color,
        )
        if span.end.y - span.start.y > 15:
            draw_text(
                draw,
                span.name,
                910,
                (span.start.y + span.end.y) / 2,
            )

    for date in YEAR_TACKS:
        draw_tack(draw, date.string, date.y)

    im.save("out.png")


if __name__ == "__main__":
    plot()
