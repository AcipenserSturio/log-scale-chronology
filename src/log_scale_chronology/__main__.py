import csv
from pathlib import Path

from PIL import Image, ImageDraw
import tomli

from .date import Date
from .stratigraphy import Tree
from .taxonomy import Taxonomy, Taxon
from .config import (
    FONT, WIDTH, HEIGHT,
    BACKGROUND_COLOR, COLOR,
    SEMI_TRANSPARENT, SEMI_TRANSPARENT_COLORED,
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

def draw_temp_scale(im: Image,
                    offset: int,
                    ) -> Image:

    im_over = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im_over)

    for temp in range(-10, 25):
        draw.line(
            ((offset + temp * MAGNIFIER, Date("120 mya").y),
             (offset + temp * MAGNIFIER, HEIGHT)),
            fill=(SEMI_TRANSPARENT_COLORED
                  if temp % 5 else SEMI_TRANSPARENT),
        )
    im.alpha_composite(im_over)



MIN_BLOCK = 20
def draw_taxon(im: Image,
               draw: ImageDraw.Draw,
               taxon: Taxon,
               offset: int):

    # print(taxon.date, offset, taxon.size, taxon.name, sep="\t")
    taxon_mid = (offset + MIN_BLOCK * taxon.size // 2)
    if taxon.children:
        if len(taxon.children) > 1:
            draw.text(
                (taxon_mid + 3, taxon.date.y - 10),
                taxon.name,
                fill=COLOR,
                font=FONT,
                anchor="lm",
            )
        else:
            draw.line(
                ((taxon_mid - 2, taxon.date.y), (taxon_mid + 2, taxon.date.y)),
                fill=COLOR,
            )
        for child in taxon.branches:
            # draw child
            child_mid = offset + MIN_BLOCK * child.size // 2
            draw.line(
                ((taxon_mid, taxon.date.y),
                (child_mid, taxon.date.y)),
                fill=COLOR,
            )
            draw.line(
                ((child_mid, taxon.date.y),
                (child_mid, child.date.y)),
                fill=COLOR,
            )
            draw_taxon(im, draw, child, offset)
            offset += child.size * MIN_BLOCK
    else:
        draw_leaf_text(im, draw, taxon.name, taxon_mid, taxon.date.y)
        # draw_tack(draw, taxon.name, taxon.date.y, taxon_mid)


def textbox_size(message: str) -> tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    _, _, width, height = draw.textbbox(
        (0, 0),
        message,
        font=FONT,
    )
    return width, height


def draw_leaf_text(im: Image,
                   draw: ImageDraw.Draw,
                   message: str,
                   # offset: tuple[int, int],
                   # size: tuple[int, int]):
                   x: int,
                   y: int):
    # offset_x, offset_y = offset
    # size_x, size_y = size
    width, height = textbox_size(message)

    img_text = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(img_text)
    draw_text.text(
        (0, 0),
        text=message,
        fill=COLOR,
        font=FONT,
    )
    img_text = img_text.rotate(-90, expand=True)
    im.alpha_composite(img_text, (x - height // 2, y + 10))


def plot():
    im = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    # draw_node(im, draw, 0, 0)

    print("Loading stratigraphic data")
    with open("assets/stratigraphy.toml", "rb") as f:
        strat = Tree(tomli.load(f))

    print("Drawing eons")
    for span in strat.eons:
        span.rectangle(draw)

    print("Drawing eras")
    for span in strat.eras:
        span.rectangle(draw)

    print("Drawing periods")
    for span in strat.periods:
        span.rectangle(draw)

    print("Drawing epochs")
    for span in strat.epochs:
        span.rectangle(draw)

    print("Drawing ages")
    for span in strat.ages:
        span.rectangle(draw)

    overlay = Image.new("RGBA", (WIDTH - 1000, HEIGHT), (255, 255, 255, 200))
    im.alpha_composite(overlay, (1000, 0))

    print("Drawing time scale tacks")
    draw_tacks(
        draw,
        [(date, date.string) for date in YEAR_TACKS],
        1000
    )

    print("Drawing temperature scale")
    draw_temp_scale(im, 1200)
    for filepath in Path("assets/paleotemps").glob("*.csv"):
        print(f"Drawing {filepath.stem}")
        draw_csv(im, 1200, filepath)

    print("Drawing taxonomy")
    taxonomy = Taxonomy()
    for filepath in Path("assets/taxa").glob("*.csv"):
        taxonomy.register(filepath)
    draw_taxon(im, draw, taxonomy.taxa["cellular_organisms"], 1450)

    print("Loading events")
    events_path = (
        "assets/events-short.toml"
        if HEIGHT < 4000 else "assets/events.toml"
    )
    with open(events_path, "rb") as f:
        events = tomli.load(f)

    print("Drawing events")
    draw_tacks(
        draw,
        [(Date(date), desc) for date, desc in events.items()],
        2650
    )

    print("Saving image")
    im.save("out.png")

    print("Exiting")


if __name__ == "__main__":
    plot()
