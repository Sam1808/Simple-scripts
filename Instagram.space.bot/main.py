import os
import requests
from dotenv import load_dotenv
from instabot import Bot
from os import listdir

path = input('Please enter folder name (default is Images): ')
spacex_url = input('Please enter SpaceX_URL (default is latest launch): ')
spacex_choice = input('Would you like to run downloading SpaceX`s photos? (Yes/No): ')
image_id = input('Please enter Hubble`s image ID (default is 1000):')
hubble_choice = input('Would you like to run downloading Hubble`s photos? (Yes/No):' )

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
        filename = 'spacex_' + file_number + '.jpg'
        download_image(file_link, filename)

def fetch_habble_image(image_id):
    response = requests.get(habble_url)
    catalog = response.json()['image_files']
    for element in reversed(catalog):
        last_link = 'https:' + element.get('file_url')
        if get_extension(last_link) == '.jpg': #download only JPG
            filename = 'image_id_' + str(image_id) + str(get_extension(last_link))
            download_image(last_link, filename)
            break


if __name__ == '__main__':

    if not path:
        path = 'Images'
    os.makedirs(path, exist_ok = True)
    abspath = os.path.abspath(path)

    if not spacex_url:
        spacex_url = 'https://api.spacexdata.com/v3/launches/latest'

    if spacex_choice == 'Yes':
        fetch_spacex_last_launch(spacex_url)

    if not image_id:
        image_id = 1000
    habble_url = 'http://hubblesite.org/api/v3/image/' + str(image_id)

    if hubble_choice == 'Yes':
        fetch_habble_image(image_id)

    pictures = listdir(path)

    if len(pictures) != 0:
        load_dotenv()
        INSTA_LOGIN = os.getenv("INSTA_LOGIN")
        INSTA_PASS = os.getenv("INSTA_PASS")
        if not INSTA_LOGIN:
            INSTA_LOGIN = input('Please enter your Instagram Login: ')
            INSTA_PASS =  input('Please enter your Instagram Password: ')
        bot = Bot()
        bot.login(username=INSTA_LOGIN, password=INSTA_PASS)
        for pic in pictures:
            photo_path = os.path.join(abspath,pic)
            print('Image will be upload: ', photo_path)
            bot.upload_photo(photo_path, caption="Space...")
    else:
        print('There is no files to upload. Have a nice day!')