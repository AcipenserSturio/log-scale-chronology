from PIL import ImageFont


FONTSIZE = 20
FONT = ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Bold.ttf", FONTSIZE)

WIDTH, HEIGHT = 1100, 6000
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
