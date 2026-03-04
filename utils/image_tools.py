from PIL import Image
import os


def create_thumbnail(filename, upload_folder, thumb_folder):

    path = os.path.join(upload_folder, filename)
    thumb = os.path.join(thumb_folder, filename)

    try:
        img = Image.open(path)
        img.thumbnail((400, 400))
        img.save(thumb)

    except:
        pass