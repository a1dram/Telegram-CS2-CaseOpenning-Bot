import subprocess
import random
import os

import sqlite3

from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

# from rembg import remove


# def raw():
#     image = Image.open('s.jpg')
#     output = remove(image)
#     output.save('asd.png')

def download_skin_photo(img, color):
    ffmpeg_cmd = f'ffmpeg -i static/image_adds/background.jpg -vf scale=1920:1361 new_background.jpg'
    subprocess.run(ffmpeg_cmd, check=True)

    # im = Image.open('image.png')
    # (width, height) = im.size
    # print(width, height)

    width, height = 1920, 1361

    img_ex = img[img.find(" ") + 1:]
    print(img_ex)

    img = img[img.find('wiki_') + 5:]
    img = 'wiki_' + img[:img.find('_')]
    print(img)

    link = f"https://s-wiki.cs.money/{img}_large_preview.png"

    ffmpeg_cmd = f'ffmpeg -i {link} -vf scale={width / 1.3}:-1 image.png'
    subprocess.run(ffmpeg_cmd, check=True)

    ffmpeg_cmd = f'ffmpeg -i new_background.jpg -i image.png -filter_complex "overlay=225:100" output.jpg'
    subprocess.run(ffmpeg_cmd, check=True)

    ffmpeg_cmd = f'ffmpeg -i static/colors/{color}.png -s {width}x130 color_line.png'
    subprocess.run(ffmpeg_cmd, check=True)

    ffmpeg_cmd = (f'ffmpeg -i output.jpg -i color_line.png -filter_complex '
                  f'"overlay=0:{height - 130}" static/CaseBase/"Dreams & Nightmares"/{color}/{img_ex}.jpg')
    subprocess.run(ffmpeg_cmd, check=True)


while True:
    try:
        skin_title = input()

        download_skin_photo(skin_title, 'blue')

    except subprocess.CalledProcessError:
        pass

    finally:
        for i in ['new_background.jpg', 'image.png', 'color_line.png', 'output.jpg']:
            os.remove(i)
