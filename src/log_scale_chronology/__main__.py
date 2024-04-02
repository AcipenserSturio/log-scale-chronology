import math
import re

from PIL import Image, ImageDraw, ImageFont

FONTSIZE = 20
FONT = ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Bold.ttf", FONTSIZE)

WIDTH, HEIGHT = 200, 4000
BACKGROUND_COLOR = (255, 255, 255, 255)
COLOR = (0, 0, 0, 255)

BP_EPOCH = 1950
PRESENT = 2024
BIG_BANG = (13.787 * 10**9 # Before Present
            - BP_EPOCH + PRESENT) # -> Current day
YEAR_TACKS = [
    "10 bya", "5 bya", "2 bya", "1 bya",
    "500 mya", "200 mya", "100 mya", "50 mya", "20 mya", "10 mya", "5 mya", "2 mya", "1 mya",
    "500 kya", "200 kya", "100 kya", "50 kya", "20 kya", "10 kya",
    "3000 BC", "1000 BC", "200 AD", "1000 AD", "1500 AD", "1800 AD",
    "1900 AD", "1950 AD", "1980 AD", "2000 AD", "2010 AD", "2016 AD", "2020 AD", "2022 AD",
]


def str_to_year(string) -> int | float:
    number, unit = re.match(r"(?P<number>\d+(\.\d+)?) (?P<year>bya|mya|kya|BC|AD)", string).group("number", "year")
    number = float(number)
    if (unit == "bya"):
        number = number * 10**9 - BP_EPOCH + PRESENT
    elif (unit == "mya"):
        number = number * 10**6 - BP_EPOCH + PRESENT
    elif (unit == "kya"):
        number = number * 10**3 - BP_EPOCH + PRESENT
    elif (unit == "BC"):
        number += PRESENT
    elif (unit == "AD"):
        number = PRESENT - number
    else:
        raise ValueError(f"Unsupported year unit: {unit}")
    return number


def year_to_percentile(year: int | float) -> float:
    return 1 - math.log(year) / math.log(BIG_BANG)


def draw_text(draw: ImageDraw.Draw, text: str, year: int | float):
    y = round(year_to_percentile(year) * HEIGHT)
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


def draw_year(draw: ImageDraw.Draw, year: str):
    draw_text(draw, year, str_to_year(year))


def plot():
    im = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(im)

    # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    # draw_node(im, draw, 0, 0)
    for year in YEAR_TACKS:
        draw_year(draw, year)

    im.save("out.png")


if __name__ == "__main__":
    print("Plotting...")
    plot()
