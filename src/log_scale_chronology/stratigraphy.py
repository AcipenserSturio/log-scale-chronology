from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from PIL import ImageDraw

from .date import Date
from .config import (
    COLOR, FONT, WIDTH,
)

IDS_TO_LEVELS = [
    "eon",
    "era",
    "period",
    "epoch",
    "age",
]
LEVELS_TO_IDS = {k: v for v, k in enumerate(IDS_TO_LEVELS)}
BLOCK_SIZE = 200


class Tree:
    def __init__(self, spans: dict):
        self.spans = defaultdict(list)
        for level_name, level_details in spans.items():
            for span_name, span_details in level_details.items():
                self.spans[level_name].append(Span(
                    tree = self,
                    level = level_name,
                    name = span_name,
                    _color = span_details["color"],
                    _start = Date(span_details["start"]) if "start" in span_details else None,
                    _child = span_details["child"] if "child" in span_details else None,
                    _text_color = span_details["text_color"] if "text_color" in span_details else None,
                ))

    def get(self, level: str, span_name: Span) -> Span:
        for span in self.spans[level]:
            if span.name == span_name:
                return span
        raise ValueError(f"No {level} called {span_name}")

    def next_span(self, span: Span) -> Span | None:
        index = self.spans[span.level].index(span)
        if len(self.spans[span.level]) - 1 == index:
            return None
        return self.spans[span.level][index + 1]

    @property
    def eons(self) -> list[Span]:
        return self.spans["eon"]

    @property
    def eras(self) -> list[Span]:
        return self.spans["era"]

    @property
    def periods(self) -> list[Span]:
        return self.spans["period"]

    @property
    def epochs(self) -> list[Span]:
        return self.spans["epoch"]

    @property
    def ages(self) -> list[Span]:
        return self.spans["age"]


@dataclass
class Span:
    tree: Tree
    level: str
    name: str
    _color: str
    _start: Date | None
    _child: str | None
    _text_color: str | None

    def next_span(self) -> Span | None:
        return self.tree.next_span(self)

    @property
    def start(self) -> Date:
        if self._start:
            return self._start
        if not self._child:
            raise ValueError("Span exists without start or child")
        return self.tree.get(self.child_level, self._child).start

    @property
    def child_level(self) -> str:
        return IDS_TO_LEVELS[LEVELS_TO_IDS[self.level]+1]

    @property
    def end(self) -> Date:
        next_span = self.next_span()
        if not next_span:
            return Date("0 present")
        return next_span.start

    @property
    def color(self) -> Tuple[int, int, int]:
        return tuple(bytes.fromhex(self._color[1:]))

    @property
    def text_color(self) -> Tuple[int, int, int]:
        if self._text_color:
            return tuple(bytes.fromhex(self._text_color[1:]))
        return COLOR

    def rectangle(self, draw: ImageDraw):
        y1, y2 = self.start.y, self.end.y
        y_mid = (y1 + y2) / 2
        x1 = LEVELS_TO_IDS[self.level] * BLOCK_SIZE
        x2 = x1 + BLOCK_SIZE
        if not self._child:
            # x2 = BLOCK_SIZE*5
            x2 = WIDTH

        draw.rectangle(
            ((x1, y1), (x2, y2)),
            fill=self.color,
        )
        if y2 - y1 > 15:
            draw.text(
                (10 + x1, y_mid),
                self.name,
                fill=self.text_color,
                font=FONT,
                anchor="lm",
            )
