from io import BytesIO
# from PIL import Image

# img_file = BytesIO()

# # quality='keep' is a Pillow setting that maintains the quantization of the image.
# # Not having the same quantization can result in different sizes between the in-
# # memory image and the file size on disk.


# image_data = b""


# image = Image.open(BytesIO(image_data))

# width = image.width
# height = image.height
# print(f"width: {width}, height: {height}")


# TODO(medium)(SpeedFox198): usel pillow
def get_display_dimensions(picture: BytesIO):
    """ Generates the height and width to display picture """

    # .... get picture width n height ...
    height = 300
    width = 300
    # .... get picture width n height ...

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
