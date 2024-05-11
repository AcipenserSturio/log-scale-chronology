from PIL import Image, ImageDraw
from .config import (
    FONT,
)

def textbox_size(message: str) -> tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    _, _, width, height = draw.textbbox(
        (0, 0),
        message,
        font=FONT,
    )
    return width, height

