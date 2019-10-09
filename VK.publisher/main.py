import argparse
import os
import random
import requests
from dotenv import load_dotenv


def download_image(url, filename):
    print('Run downloading...', filename)
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VK photo auto publisher')
    parser.add_argument('-lc', '--last_comics', help='Please add current last number comics (default:2212)')
    parser.add_argument('-t', '--token', help='Add your own VK Token')
    parser.add_argument('-id', '--group_id', help='Add your own VK Group ID')
    args = parser.parse_args()

    comics_number_from = 1

    comics_number_till = args.last_comics

    if not comics_number_till:
        comics_number_till = 2212 # October 2019

    comics_number_till = int(comics_number_till)

    comics_number = random.randint(comics_number_from,comics_number_till)

    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    comics_url = response.json()['img']
    comics_description = response.json()['alt']
    comics_filename = f'comic-{comics_number}.png'
    download_image(comics_url, comics_filename)

    print(f'''
        Ok, {comics_filename} will be published.
        Getting link to upload comics and upload it...
        ''')

    load_dotenv()
    vk_token = args.token

    if not vk_token:
        vk_token = os.getenv("VK_TOKEN")

    method = 'photos.getWallUploadServer'
    url = f'https://api.vk.com/method/{method}'

    payload = {'access_token': vk_token, 'v': 5.101, 'no_agreement': 1}

    response = requests.get(url, params=payload)
    response = response.json()['response']

    with open(comics_filename, 'rb') as file:
        url = response.get('upload_url')
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()

    server = response.json()['server']
    photo = response.json()['photo']
    hash = response.json()['hash']

    payload.update({'server':server, 'photo':photo, 'hash': hash})

    print('Saving photo for VK Wall...')

    method = 'photos.saveWallPhoto'
    url = f'https://api.vk.com/method/{method}'

    response = requests.post(url, params=payload)
    response.raise_for_status()

    response =response.json()['response']
    set_of_parameters = response[0]
    media_id = set_of_parameters.get('id')
    owner_id = set_of_parameters.get('owner_id')
    attachments = f'photo{owner_id}_{media_id}'

    group_id = args.group_id

    if not group_id:
        group_id = os.getenv("GROUP_ID")

    del payload['no_agreement']
    del payload['server']
    del payload['photo']
    del payload['hash']

    payload.update({
        'owner_id': group_id,
        'message': comics_description,
        'attachments': attachments,
        'from_group': 1,
    })

    print('Publishing photo at VK Wall...')

    method = 'wall.post'
    url = f'https://api.vk.com/method/{method}'

    response = requests.get(url, params=payload)
    response.raise_for_status()

    print(f'Removing {comics_filename} local file...')
    os.remove(comics_filename)

    print('Please check your new post at the Wall. Good buy.')