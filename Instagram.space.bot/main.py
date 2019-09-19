import argparse
import os
import requests
from dotenv import load_dotenv
from instabot import Bot
from os import listdir


def get_extension(link):
    separation_link = os.path.splitext(link)
    extension = separation_link[1]
    return (extension)

def download_image(url, filename):
    print('Run downloading...', filename)
    response = requests.get(url, verify=False)
    filename = os.path.join(abspath,filename)
    with open(filename, 'wb') as file:
        file.write(response.content)

def fetch_spacex_last_launch(spacex_url):
    response = requests.get(spacex_url)
    catalog = response.json()['links'].get('flickr_images')
    for element in enumerate(catalog):
        file_number = str(element[0])
        file_link = element[1]
        file_name = 'spacex_' + file_number + '.jpg'
        download_image(file_link, file_name)

def fetch_habble_image(image_id):
    habble_url = 'http://hubblesite.org/api/v3/image/' + str(image_id)
    response = requests.get(habble_url)
    catalog = response.json()['image_files']
    for element in reversed(catalog):
        last_link = 'https:' + element.get('file_url')
        if get_extension(last_link) == '.jpg': #download only JPG
            file_name = 'image_id_' + str(image_id) + str(get_extension(last_link))
            download_image(last_link, file_name)
            break

def get_instagram_credentials():
    load_dotenv()
    insta_login = os.getenv("INSTA_LOGIN")
    insta_pass = os.getenv("INSTA_PASS")
    if not insta_login:
        insta_login = input('Please enter your Instagram Login: ')
        insta_pass = input('Please enter your Instagram Password: ')
    credentials = {'login':insta_login, 'password':insta_pass}
    return (credentials)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Instagram space bot')
    parser.add_argument('-p', '--path', help='''Folder name for pictures (default is 'Images')''')
    parser.add_argument('-s', '--space_url', help='URL with http(s) prefix to download SpaceX images')
    parser.add_argument('-ha', '--habble_id', help='Hubble`s image ID')
    args = parser.parse_args()

    path = args.path
    if not path:
        path = 'Images'
    os.makedirs(path, exist_ok = True)
    abspath = os.path.abspath(path)

    if args.space_url:
        fetch_spacex_last_launch(args.space_url)

    if args.habble_id:
        fetch_habble_image(args.habble_id)

    pictures = listdir(path)

    if len(pictures):
        bot = Bot()
        credentials = get_instagram_credentials()
        bot.login(username=credentials.get('login'), password=credentials.get('password'))
        for pic in pictures:
            photo_path = os.path.join(abspath,pic)
            print('Image will be upload: ', photo_path)
            bot.upload_photo(photo_path, caption="Space...")
    else:
        print('There is no files to upload. Have a nice day!')