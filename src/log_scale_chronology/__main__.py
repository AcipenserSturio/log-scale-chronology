from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 2000, 2000
BACKGROUND_COLOR = (255, 255, 255, 255)


def plot():
    im = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(im)

    draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    # draw_node(im, draw, 0, 0)

    im.save("out.png")


if __name__ == "__main__":
    print("Plotting...")
    plot()
