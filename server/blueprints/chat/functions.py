import os
from io import BytesIO
from PIL import Image
from utils import secure_save_file
from models import Media


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


async def save_file(attachments_path: str, file: bytes, filename: str, room_id: str, message_id: str, session):
    """ Save file securely I guess """

    destination_directory = os.path.join(attachments_path, room_id, message_id)
    os.makedirs(destination_directory)
    filename = await secure_save_file(destination_directory, filename, file)

    # TODO(high)(SpeedFox198): Check if file is image (check what kind of file)
    height, width = get_display_dimensions(file)

    media = Media(message_id, path=filename, height=height, width=width)
    async with session.begin():
        session.add(media)
