import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

currencies = {'₽': "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&sxsrf=APwXEdfj2uEXre7"
                   "-NGWNGM_GriXS7hBDNw%3A1684620787827&ei=80VpZLWKMs_-qwGWw57ICA&ved=0ahUKEwj1z4699YT_AhVP_yo"
                   "KHZahB4kQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&gs_lcp=Cgxnd3Mtd2l6LXNlcnA"
                   "QAzIHCCMQigUQJzIHCCMQigUQJzINCAAQigUQsQMQgwEQQzIQCAAQgAQQFBCHAhCxAxCDATINCAAQigUQsQMQgwEQQ"
                   "zIKCAAQigUQsQMQQzIHCAAQigUQQzIHCAAQigUQQzIKCAAQigUQsQMQQzILCAAQgAQQsQMQgwE6CggAEEcQ1gQQsAM"
                   "6CggAEIoFELADEEM6CggAEIAEEBQQhwI6BQgAEIAEOgsILhCKBRCxAxCDAToRCC4QgAQQsQMQgwEQxwEQ0QM6BAgjE"
                   "CdKBAhBGABQ7B5YuiRgsSZoAXABeACAATSIAZICkgEBNpgBAKABAcgBCsABAQ&sclient=gws-wiz-serp",

              '€': 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B5%D0%B2%D1%80%D0%B'
                   'E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B5%D0%B2%D1%80%D0%BE&aqs=chrome..69i57j0i512l9'
                   '.2177j0j7&sourceid=chrome&ie=UTF-8',

              '¥': 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D1%8E%D0%B0%D0%BD%D1%8'
                   'C&sxsrf=APwXEdf67xG2U_zZidiMIsZ--J6iKAcNFw%3A1684620552094&ei=CEVpZNW0BdSMwPAPw4aBoAc&oq=%D0%B4%D0%'
                   'BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D1%8E%D0%B0%D0%BD&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMg8IABCABBAUEIc'
                   'CEEYQggIyBQgAEIAEMgUIABCABDIFCAAQywEyBQgAEMsBMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHj'
                   'oHCCMQsAMQJzoKCAAQRxDWBBCwAzoVCC4QigUQxwEQ0QMQyAMQsAMQQxgBOhIILhCKBRDUAhDIAxCwAxBDGAE6BwgjEOoCECc6D'
                   'wgAEIoFEOoCELQCEEMYAjoHCCMQigUQJzoQCAAQgAQQFBCHAhCxAxCDAToKCAAQgAQQFBCHAjoLCC4QigUQsQMQgwE6EQguEIAE'
                   'ELEDEIMBEMcBENEDOgsIABCABBCxAxCDAToHCAAQigUQQzoHCC4QigUQQzoNCAAQigUQsQMQgwEQQzoKCAAQigUQsQMQQzoICC4'
                   'QgAQQsQM6CAgAEIAEELEDOg0IABCABBAUEIcCELEDOgsIABCKBRCxAxCDAUoECEEYAFC0C1iYHWDGKWgCcAF4AIABOIgBpwSSAQ'
                   'IxMpgBAKABAbABFMgBDMABAdoBBAgBGAjaAQYIAhABGAE&sclient=gws-wiz-serp'
              }


def get_skin_value(skin_id):
    # ссылка на скин
    skin_site = f"https://buff.163.com/goods/{skin_id}?from=market#tab=selling"
    skin_full_page = requests.get(skin_site, headers=headers)
    skin_soup = BeautifulSoup(skin_full_page.content, 'html.parser')
    money = skin_soup.findAll("strong", {"class": "f_Strong"})[0].text

    for i in money:
        if i in '()$ ':
            money = money.replace(i, '')

    money = float(money)

    # if value_type != '$':
    #     value_url = currencies[value_type]
    #     full_page = requests.get(value_url, headers=headers)
    #     soup = BeautifulSoup(full_page.content, 'html.parser')
    #     cov = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})[0].text
    #
    #     value = float(cov.replace(",", "."))
    #
    #     skin_cost = round(float(money) * value, 2)
    # else:
    #     skin_cost = float(money)

    return money


def download_skin_image(skin_url, image_url, image_name):
    skin_site = f'https://wiki.cs.money/ru/{skin_url}'
    skin_full_page = requests.get(skin_site, headers=headers)
    skin_soup = BeautifulSoup(skin_full_page.content, 'html.parser')
    skin_img = skin_soup.findAll("src")

    # img = requests.get(image_url)
    # with open(image_name + '.jpg', 'wb') as image:
    #     image.write(img.content)

    return skin_img

# print(download_skin_image('weapons/m9-bayonet/doppler-sapphire', 'https://s-wiki.cs.money/wiki_k0PBx'
#                                                                  'Nb_large_preview.png', 'knifee'))
