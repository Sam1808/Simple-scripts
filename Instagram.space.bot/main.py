import requests
import os
from os import listdir
from instabot import Bot
from dotenv import load_dotenv

def extension(link):
    return (link[(link.rfind('.')):(len(link))])


def image_download(url, filename):
    response = requests.get(url, verify=False)
    filename = abspath + '/' + filename
    os.path.normpath(filename)
    #print(filename)
    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(spacex_url):
    response = requests.get(spacex_url)
    spisok = response.json()['links'].get('flickr_images')
    for element in enumerate(spisok):
        filename = 'spacex_' + str(element[0]) + '.jpg'
        #print(filename)
        image_download(element[1], filename)

def habble_image_download(id):
    response = requests.get(habble_url)
    spisok = response.json()['image_files']
    for element in reversed(spisok):
        last_link = 'https:' + element.get('file_url')
        #print(last_link)
        if extension(last_link) == '.jpg': #download only JPG
            filename = 'image_id_' + str(id) + str(extension(last_link))
            print('Run downloading...')
            image_download(last_link, filename)
            break

path = input('Please enter folder name (default is Image): ')
if not path:
    path = 'Images'
if not os.path.exists(path):
    os.mkdir(path)
abspath = os.path.abspath(path)


spacex_url = input('Please enter SpaceX_URL (default is latest launch): ')
if not spacex_url:
    spacex_url = 'https://api.spacexdata.com/v3/launches/latest'

choice = input('Would you like to run downloading SpaceX`s photos? (Yes/No): ')
if choice == 'Yes':
    fetch_spacex_last_launch(spacex_url)

id = input('Please enter Hubble`s image ID (default is 1000):')
if not id:
    id = 1000
habble_url = 'http://hubblesite.org/api/v3/image/' + str(id)

choice = input('Would you like to run downloading Hubble`s photos? (Yes/No):' )
if choice == 'Yes':
    habble_image_download(id)

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
        photo_path = str(abspath + '/' + pic)
        os.path.normpath(photo_path)
        print('Image will be upload: ', photo_path)
        bot.upload_photo(photo_path, caption="Space...")
else:
    print('There is no files to upload. Have a nice day!')