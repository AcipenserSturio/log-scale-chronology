from PIL import ImageFont


FONTSIZE = 20
FONT = ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Bold.ttf", FONTSIZE)

BACKGROUND_COLOR = (255, 255, 255, 255)
COLOR = (0, 0, 0, 255)
SEMI_TRANSPARENT = (0, 0, 0, 100)
SEMI_TRANSPARENT_COLORED = (0, 127, 255, 50)

BP_EPOCH = 1950
PRESENT = 2025
BIG_BANG = (13.787 * 10**9 # Before Present
            - BP_EPOCH + PRESENT) # -> Current day

IDS_TO_LEVELS = [
    "eon",
    "era",
    "period",
    "epoch",
    "age",
]
LEVELS_TO_IDS = {k: v for v, k in enumerate(IDS_TO_LEVELS)}
BLOCK_SIZE = 200
