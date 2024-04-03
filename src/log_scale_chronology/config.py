from PIL import ImageFont


FONTSIZE = 20
FONT = ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Bold.ttf", FONTSIZE)

WIDTH, HEIGHT = 2500, 7000
BACKGROUND_COLOR = (255, 255, 255, 255)
COLOR = (0, 0, 0, 255)
SEMI_TRANSPARENT = (0, 0, 0, 100)

BP_EPOCH = 1950
PRESENT = 2025
BIG_BANG = (13.787 * 10**9 # Before Present
            - BP_EPOCH + PRESENT) # -> Current day

YEAR_TACKS = [
    "10 bya",
    "6 bya", "4 bya", "2.5 bya", "1.5 bya", "1 bya",
    "600 mya", "400 mya", "250 mya", "150 mya", "100 mya",
    "60 mya", "40 mya", "25 mya", "15 mya", "10 mya",
    "6 mya", "4 mya", "2.5 mya", "1.5 mya", "1 mya",
    "600 kya", "400 kya", "250 kya", "150 kya", "100 kya",
    "60 kya", "40 kya", "25 kya", "15 kya", "10 kya",
    "3500 BC", "1500 BC", "1 AD", "700 AD", "1200 AD", "1500 AD", "1700 AD", "1820 AD", "1900 AD", "1940 AD", "1970 AD", "1990 AD", "2005 AD", "2015 AD", "2020 AD", "2022-02 AD", "2023-06 AD"

]

# YEAR_TACKS = [
#     "10 bya", "5 bya", "2 bya", "1 bya",
#     "500 mya", "200 mya", "100 mya", "50 mya", "20 mya", "10 mya", "5 mya", "2 mya", "1 mya",
#     "500 kya", "200 kya", "100 kya", "50 kya", "20 kya", "10 kya",
#     "3000 BC", "1000 BC", "200 AD", "1000 AD", "1500 AD", "1800 AD",
#     "1900 AD", "1950 AD", "1980 AD", "2000 AD", "2010 AD", "2016 AD", "2020 AD", "2022 AD",
# ]
