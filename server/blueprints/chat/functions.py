from io import BytesIO
from PIL import Image


# TODO(medium)(SpeedFox198): usel pillow
def get_display_dimensions(picture: bytes):
    """ Generates the height and width to display picture """

    image = Image.open(BytesIO(picture))
    width = image.width
    height = image.height
    print(f"\n\nwidth: {width}, height: {height}\n\n")

    ratio = height / width
    if ratio > 1:
        width = 300
    else:
        width = 400

    height = round(width*ratio, 3)

    if height > 440:
        height = 440
    elif height < 100:
        height = 100

    return height, width
