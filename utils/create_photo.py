import subprocess
import random
import os

from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

from database.skin_base import *
from utils.parsing import get_skin_value


def download_skin_photo(user_name, skin_case):
    chances = [0, 79.92, 95.9, 99.1, 99.74, 100]
    chance = random.uniform(0, 100)

    case_use = eval(skin_case)

    if chances[0] < chance < chances[1]:
        color = 'blue'

    elif chances[1] < chance < chances[2]:
        color = 'purple'

    elif chances[2] < chance < chances[3]:
        color = 'pink'

    elif chances[3] < chance < chances[4]:
        color = 'red'

    else:
        color = 'yellow'

    skin = random.choice([i for i in case_use[color].keys()])
    skin_type = case_use[color][skin]
    skin_name = skin.replace('-', '—')
    real_skin_name = skin

    stattrack = False

    if 'stattrack' in skin_type:
        choose_stattrack = random.randint(1, 10)
        if choose_stattrack == 10:
            stattrack = True
            is_stattrack = 'stattrack'

            real_skin_name = 'StatTrak™ ' + real_skin_name
        else:
            is_stattrack = 'not_stattrack'
    else:
        is_stattrack = 'not_stattrack'

    real_skin_name = {'blue': '🟦 ',
                      'purple': '🟪 ',
                      'pink': '🎆 ',
                      'red': '🟥 ',
                      'yellow': '🟨 ★ '}[color] + real_skin_name

    rare = random.choice([ex for ex in skin_type[is_stattrack].keys()])
    rare_fullname = {'FN': 'Factory New', 'MW': 'Minimal Wear', 'FT': 'Field-Tested',
                     'WW': 'Well-worn', 'BS': 'Battle-Scarred'}[rare]

    skin_id = skin_type[is_stattrack][rare]

    if not 'doppler' in skin_name.lower():
        skin_cost = get_skin_value(skin_id)

    else:
        if 'gamma' in skin_name.lower():
            gamma_chance = random.uniform(0, 100)

            if gamma_chance <= 8.53:
                skin_name += ' | Emerald'
                real_skin_name += ' | Emd'
                skin_cost = round(get_skin_value(skin_id) * skin_type['phase_type'][rare]['emerald'], 2)

            else:
                phase = random.choice(['1', '2', '3', '4'])
                skin_name += f' | Phase {phase}'
                real_skin_name += f' | P{phase}'
                skin_cost = round(get_skin_value(skin_id) * skin_type['phase_type'][rare][phase], 2)

    if type(skin_type['float_limit'][rare]) is not str:
        skin_float = round(random.uniform(*skin_type['float_limit'][rare]), 8)
    else:
        skin_float = 0
        rare_fullname = skin_type['float_limit'][rare]

    try:
        skin_pattern = random.randint(1, 999)

        if skin_pattern in [56, 200, 700]:
            skin_pattern = 56

            image = Image.open(
                f"static/CaseBase/{skin_case}/{color}/{skin_name.replace('|', '').replace('—', '-').replace('.', '')}/"
                f"{rare}{skin_pattern}.jpg")
            skin_cost = round(skin_cost * skin_type['rare_pattern']['factor'], 2)
            # skin_name = f"{skin_name} | {skin_type['rare_pattern']['rare_type']}"

            rare_pattern = 'BG'

        else:
            raise KeyError

    except Exception:
        rare_pattern = ''
        image = Image.open(
            f"static/CaseBase/{skin_case}/{color}/{skin_name.replace('|', '').replace('—', '-').replace('.', '')}/{rare}.jpg")

    (width, height) = image.size

    time_date = f'{user_name} | ' + str(datetime.now())
    time_date = time_date[:time_date.find('.')]

    skin_name_font_size = 120

    if len(skin_name) > 27:
        skin_name_font_size /= (len(skin_name) + 8) / 27

    cs_font = ImageFont.truetype("static/fonts/cs_regular.ttf", skin_name_font_size)
    skin_money_font = ImageFont.truetype("static/fonts/cs_regular.ttf", 90)
    skin_info_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", 50)
    bot_tag_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", 30)

    # if float(skin_cost).is_integer():
    #     skin_cost = int(skin_cost)

    date_font_size = 50
    if len(time_date) > 31:
        date_font_size /= len(time_date) / 28

    skin_date_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", date_font_size)

    drawer = ImageDraw.Draw(image)

    drawer.text((width / 2, height / 8), skin_name, font=cs_font, fill='black', anchor='ms')
    drawer.text((width / 1.01, height / 1.13), time_date, font=skin_date_font,
                fill='black', anchor='rs')
    drawer.text((25, height / 1.25), f'$ {skin_cost}', font=skin_money_font, fill='black',
                anchor='ls')
    drawer.text((25, height / 1.18), f'Exterior: {rare_fullname}', font=skin_info_font,
                fill='black', anchor='ls')
    drawer.text((25, height / 1.13), f'Float: {skin_float}', font=skin_info_font,
                fill='black', anchor='ls')

    drawer.text((width / 2, height / 20), '@cs2cases_bot', font=bot_tag_font, fill='black', anchor='ms')

    image.save('new_img.jpg')
    skin_file = 'new_img.jpg'

    if stattrack:
        ffmpeg_cmd = ['ffmpeg',
                      '-i', 'new_img.jpg',
                      '-i', 'static/image_adds/stattrack_logo_2.png',
                      '-filter_complex', "overlay=30:30",
                      'output.jpg']
        # ffmpeg_cmd = (f'ffmpeg -i new_img.jpg -i stattrack_logo_2.png '
        #               f'-filter_complex "overlay=30:30" output.jpg')

        # ffmpeg_cmd = (f'ffmpeg -i new_img.jpg -i static/image_adds/stattrack_logo_3.png '
        #               f'-filter_complex "overlay=1650:900" output.jpg')
        subprocess.run(ffmpeg_cmd, check=True)

        os.remove('new_img.jpg')
        skin_file = 'output.jpg'

    return {'skin_file': skin_file, 'skin_cost': skin_cost, 'full_skin_name': real_skin_name, 'skin_date': time_date,
            'skin_float': skin_float, 'skin_name': skin_name, 'rare_pattern': rare_pattern}


def load_skin_photo(skin_name, skin_float, skin_cost, skin_date, skin_case, rare_pattern):
    skin_name = skin_name.replace('-', '—')

    skin_name = (skin_name.replace('★ ', '').replace('| Emd', '| Emerald').replace('| P1', '| Phase 1').
                 replace('| P2', '| Phase 2').replace('| P3', '| Phase 3').replace('| P4', '| Phase 4'))

    if 0 < skin_float < 0.07:
        skin_ex = 'FN'
    elif 0.07 < skin_float < 0.15:
        skin_ex = 'MW'
    elif 0.15 < skin_float < 0.38:
        skin_ex = 'FT'
    elif 0.38 < skin_float < 0.45:
        skin_ex = 'WW'
    elif 0.45 < skin_float < 1:
        skin_ex = 'BS'
    else:
        skin_ex = 'Vanilla'

    if 'StatTrak' in skin_name:
        stattrack = True
        short_skin_name = skin_name[skin_name.find('StatTrak™ ') + 10:]

    else:
        stattrack = False
        short_skin_name = skin_name[2:]

    color = {'🟦': 'blue',
             '🟪': 'purple',
             '🎆': 'pink',
             '🟥': 'red',
             '🟨': 'yellow'}[skin_name[0]]

    rare_fullname = {'FN': 'Factory New', 'MW': 'Minimal Wear', 'FT': 'Field-Tested',
                     'WW': 'Well-worn', 'BS': 'Battle-Scarred', 'Vanilla': 'Vanilla'}[skin_ex]

    if rare_pattern == 'BG':
        image = Image.open(
            f"static/CaseBase/{skin_case}/{color}/{short_skin_name.replace('|', '').replace('—', '-').replace('.', '')}/"
            f"{skin_ex}56.jpg")
        short_skin_name += f" | Blue Gem"

    else:
        image = Image.open(
            f"static/CaseBase/{skin_case}/{color}/{short_skin_name.replace('|', '').replace('—', '-').replace('.', '')}/{skin_ex}.jpg")

    (width, height) = image.size

    skin_name_font_size = 120

    if len(short_skin_name) > 27:
        skin_name_font_size /= (len(short_skin_name) + 8) / 27

    cs_font = ImageFont.truetype("static/fonts/cs_regular.ttf", skin_name_font_size)
    skin_money_font = ImageFont.truetype("static/fonts/cs_regular.ttf", 90)
    skin_info_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", 50)
    bot_tag_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", 30)

    date_font_size = 50
    if len(skin_date) > 31:
        date_font_size /= len(skin_date) / 28

    skin_date_font = ImageFont.truetype("static/fonts/Bank_Gothic_Medium.ttf", date_font_size)

    drawer = ImageDraw.Draw(image)

    drawer.text((width / 2, height / 8), short_skin_name, font=cs_font, fill='black', anchor='ms')
    drawer.text((width / 1.01, height / 1.13), skin_date, font=skin_date_font,
                fill='black', anchor='rs')
    drawer.text((25, height / 1.25), f'$ {skin_cost}', font=skin_money_font, fill='black',
                anchor='ls')
    drawer.text((25, height / 1.18), f'Exterior: {rare_fullname}', font=skin_info_font,
                fill='black', anchor='ls')
    drawer.text((25, height / 1.13), f'Float: {skin_float}', font=skin_info_font,
                fill='black', anchor='ls')

    drawer.text((width / 2, height / 20), '@cs2cases_bot', font=bot_tag_font, fill='black', anchor='ms')

    image.save('new_img.jpg')
    skin_file = 'new_img.jpg'

    if stattrack:
        ffmpeg_cmd = ['ffmpeg',
                      '-i', 'new_img.jpg',
                      '-i', 'static/image_adds/stattrack_logo_2.png',
                      '-filter_complex', "overlay=30:30",
                      'output.jpg']

        subprocess.run(ffmpeg_cmd, check=True)

        os.remove('new_img.jpg')
        skin_file = 'output.jpg'

    return skin_file
