import argparse
import logging
import os
import random
import requests
from dotenv import load_dotenv


def download_image(url, filename):
    logging.info(u'Downloading file. ')
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def get_last_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    last_number = response.json()['num']
    return last_number

def download_comics(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    set_of_data = response.json()
    comics_url = set_of_data.get('img')
    comics_description = set_of_data.get('alt')
    comics_filename = f'comics-{comics_number}.png'
    download_image(comics_url, comics_filename)
    return comics_filename, comics_description

def get_vk_response(method, payload):
    url = f'https://api.vk.com/method/{method}'
    response = requests.get(url, params=payload)
    try:
        response = response.json()['response']
        return response
    except:
        response = response.json()['error']
        error_message = response.get('error_msg')
        logging.error(f'VK error: {error_message}')
        os.remove(comics_filename)
        exit()

def post_request(url, params, files):
    response = requests.post(url, params=params, files=files)
    return response.json()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VK photo auto publisher')
    parser.add_argument('-t', '--token', help='Add your own VK Token')
    parser.add_argument('-id', '--group_id', help='Add your own VK Group ID')

    args = parser.parse_args()

    comics_number_from = 1
    comics_number_till = get_last_comics_number()
    comics_number = random.randint(comics_number_from,comics_number_till)

    comics_filename, comics_description = download_comics(comics_number)

    print(f'Ok, {comics_filename} will be published.')

    load_dotenv()
    vk_token = args.token

    if not vk_token:
        vk_token = os.getenv("VK_TOKEN")

    method = 'photos.getWallUploadServer'
    payload = {'access_token': vk_token, 'v': 5.101, 'no_agreement': 1}

    response = get_vk_response(method, payload)

    with open(comics_filename, 'rb') as file:
        url = response.get('upload_url')
        files = {'photo': file}
        response = post_request(url,None,files)

    server = response.get('server')
    photo = response.get('photo')
    received_hash = response.get('hash')

    method = 'photos.saveWallPhoto'
    payload.update({'server':server, 'photo':photo, 'hash': received_hash})
    url = f'https://api.vk.com/method/{method}'

    response = post_request(url, payload, None)

    set_of_parameters = response['response'][0]
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

    method = 'wall.post'
    payload.update({
        'owner_id': group_id,
        'message': comics_description,
        'attachments': attachments,
        'from_group': 1,
    })

    response = get_vk_response(method,payload)

    os.remove(comics_filename)
    print('Please check your new post at the Wall. Good buy.')