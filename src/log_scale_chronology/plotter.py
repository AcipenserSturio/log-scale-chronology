import csv
import re
from pathlib import Path

from PIL import Image, ImageDraw
import tomli

from .date import Date
from .stratigraphy import Tree, Span
from .taxonomy import Taxonomy, Taxon
from .plot_utils import textbox_size
from .config import (
    FONT,
    BACKGROUND_COLOR, COLOR,
    SEMI_TRANSPARENT, SEMI_TRANSPARENT_COLORED,
    BIG_BANG,
    LEVELS_TO_IDS, BLOCK_SIZE,
)

CHILD_EXTEND = 10
MIN_BLOCK = 20

class Plotter:
    def __init__(self, profile: Path):
        with open(profile, "rb") as f:
            self.settings = tomli.load(f)

        self.im = Image.new("RGBA", (self.settings["width"], self.settings["height"]), BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.im)

        self.plot()


    def draw_tack(self, text: str, y: int, x_offset: int = 0):
        self.draw.line(
            ((0 + x_offset, y), (5 + x_offset, y)),
            fill=COLOR,
        )
        self.draw.text(
            (10 + x_offset, y),
            text,
            fill=COLOR,
            font=FONT,
            anchor="lm",
        )

    def draw_tacks(self,
                   tacks: list[tuple[Date, str]],
                   x_offset: int):
        self.draw.line(
            ((x_offset, 0), (x_offset, self.settings["height"])),
            fill=COLOR,
        )
        for date, description in tacks:
            self.draw_tack(description, self.y(date), x_offset=x_offset)

    def draw_csv(self,
                 offset: int,
                 filepath: Path,
                 ) -> Image:

        im_over = Image.new("RGBA", (self.settings["width"], self.settings["height"]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im_over)

        with open(filepath) as f:
            data = csv.reader(f)
            unit, _ = next(data)
            prev_date, prev_temp = next(data)
            for date, temp in data:
                draw.line(
                    ((offset + float(prev_temp) * self.settings["temps"]["magnifier"],
                    self.y(Date(f"{prev_date} {unit}"))),
                    (offset + float(temp) * self.settings["temps"]["magnifier"],
                    self.y(Date(f"{date} {unit}")))),
                    fill=SEMI_TRANSPARENT,
                )
                prev_date, prev_temp = date, temp
        self.im.alpha_composite(im_over)

    def draw_temp_scale(self,
                        offset: int,
                        ) -> Image:

        im_over = Image.new("RGBA", (self.settings["width"], self.settings["height"]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im_over)

        for temp in range(-10, 25):
            draw.line(
                ((offset + temp * self.settings["temps"]["magnifier"], self.y(Date("120 mya")),
                (offset + temp * self.settings["temps"]["magnifier"], self.settings["height"]))),
                fill=(SEMI_TRANSPARENT_COLORED
                    if temp % 5 else SEMI_TRANSPARENT),
            )
        self.im.alpha_composite(im_over)

    def draw_taxon(self,
                   taxon: Taxon,
                   offset: int):

        taxon_mid = self.settings["taxonomy"]["offset"] + round(taxon.x * MIN_BLOCK)
        if taxon.children:
            if len(taxon.children) > 1:
                self.draw_branch_text(taxon.name, taxon_mid, self.y(taxon.date))
            else:
                self.draw.line(
                    ((taxon_mid - 2, self.y(taxon.date)), (taxon_mid + 2, self.y(taxon.date))),
                    fill=COLOR,
                )
            for child in taxon.branches:
                # draw child
                child_mid = self.settings["taxonomy"]["offset"] + round(child.x * MIN_BLOCK)

                if child.size == 1:
                    self.draw.line(
                        ((taxon_mid, self.y(taxon.date)),
                        (child_mid, self.y(taxon.date))),
                        fill=COLOR,
                    )
                    self.draw.line(
                        ((child_mid, self.y(taxon.date)),
                        (child_mid, self.y(taxon.date) + CHILD_EXTEND)),
                        fill=COLOR,
                    )
                    self.draw_leaf_text(child.leaf.name, child_mid, self.y(taxon.date) + CHILD_EXTEND)
                else:
                    self.draw.line(
                        ((taxon_mid, self.y(taxon.date)),
                        (child_mid, self.y(taxon.date))),
                        fill=COLOR,
                    )
                    self.draw.line(
                        ((child_mid, self.y(taxon.date)),
                        (child_mid, self.y(child.date))),
                        fill=COLOR,
                    )
                    self.draw_taxon(child, offset)
                offset += child.size * MIN_BLOCK
        else:
            raise ValueError("Somehow, a leaf is being rendered - it should be handled elsewhere")
            # self.draw_leaf_text(taxon.name, taxon_mid, taxon.date.y)
            # self.draw_tack(taxon.name, taxon.date.y, taxon_mid)



    def draw_leaf_text(self,
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
        self.im.alpha_composite(img_text, (x - height // 2 + 5, y + 5))


    def draw_branch_text(self,
                         message: str,
                         # offset: tuple[int, int],
                         # size: tuple[int, int]):
                         x: int,
                         y: int):
        # Ignore branch names that are digits, i.e. unnamed
        if message.isdigit():
            return
        # Ignore digits in branch names, i.e. identically named branches
        message = re.sub(r"\(\d*\)", "", message)

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
        self.im.alpha_composite(img_text, (x - height // 2 + 5, y - width - 5))


    def y(self, date: Date) -> int:
        """
        Returns value in the form of [0, HEIGHT],
        where Big Bang = 0,
        one year ago = HEIGHT.
        """
        return round(date.percentile * self.settings["height"])
        # Non logarithmic option:
        # return round((1 - self.value / BIG_BANG) * HEIGHT)


    def rectangle(self, span: Span):
        y1, y2 = self.y(span.start), self.y(span.end)
        y_mid = (y1 + y2) / 2
        x1 = LEVELS_TO_IDS[span.level] * BLOCK_SIZE
        x2 = x1 + BLOCK_SIZE
        if not span._child:
            # x2 = BLOCK_SIZE*5
            x2 = self.settings["width"]

        self.draw.rectangle(
            ((x1, y1), (x2, y2)),
            fill=span.color,
        )
        if y2 - y1 > 15:
            self.draw.text(
                (10 + x1, y_mid),
                span.name,
                fill=span.text_color,
                font=FONT,
                anchor="lm",
            )

    def plot(self):

        # draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
        # draw_node(im, draw, 0, 0)

        if "stratigraphy" in self.settings:
            print("Loading stratigraphic data")
            with open(self.settings["stratigraphy"]["source"], "rb") as f:
                strat = Tree(tomli.load(f))

            print("Drawing eons")
            for span in strat.eons:
                self.rectangle(span)

            print("Drawing eras")
            for span in strat.eras:
                self.rectangle(span)

            print("Drawing periods")
            for span in strat.periods:
                self.rectangle(span)

            print("Drawing epochs")
            for span in strat.epochs:
                self.rectangle(span)

            print("Drawing ages")
            for span in strat.ages:
                self.rectangle(span)

        if "timescale" in self.settings:
            overlay = Image.new("RGBA",
                (self.settings["width"] - self.settings["timescale"]["offset"],
                self.settings["height"]),
                (255, 255, 255, 200),
            )
            self.im.alpha_composite(overlay, (self.settings["timescale"]["offset"], 0))

            print("Drawing time scale tacks")
            for date in self.settings["timescale"]["tacks"]:
                date = Date(date)
                self.draw_tacks([(date, date.string)], self.settings["timescale"]["offset"])

        if "temps" in self.settings:
            print("Drawing temperature scale")
            self.draw_temp_scale(self.settings["temps"]["offset"])
            for filepath in Path("assets/paleotemps").glob("*.csv"):
                print(f"Drawing {filepath.stem}")
                self.draw_csv(self.settings["temps"]["offset"], filepath)

        if "taxonomy" in self.settings:
            print("Drawing taxonomy")
            taxonomy = Taxonomy(self.settings["taxonomy"]["root"])
            for filepath in sorted(Path(self.settings["taxonomy"]["source"]).glob("*.csv"), reverse=True):
                taxonomy.register(filepath)
            taxonomy.root.set_leaf_x(0)
            self.draw_taxon(taxonomy.root, self.settings["taxonomy"]["offset"])

        if "events" in self.settings:
            print("Loading events")
            with open(self.settings["events"]["source"], "rb") as f:
                events = tomli.load(f)

            print("Drawing events")
            self.draw_tacks(
                [(Date(date), desc) for date, desc in events.items()],
                self.settings["events"]["offset"]
            )

        print("Postprocessing image")
        self.im = self.im.crop((
            0,
            self.y(Date(self.settings["earliest"])),
            self.settings["width"],
            self.y(Date(self.settings["latest"])),
        ))
        if self.settings["rotate"]:
            self.im = self.im.rotate(90, expand=True)
        self.im.save(self.settings["out"])

        print("Exiting")
