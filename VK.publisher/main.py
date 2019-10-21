import argparse
import logging
import os
import random
import requests
from dotenv import load_dotenv


def download_image(url, filename):
    logging.info(f'Downloading file {filename}')
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)

def get_last_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_number = response.json()['num']
    return last_number

def get_comics_properties(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_properties = response.json()
    return comics_properties

def get_vk_response(method, payload):
    url = f'https://api.vk.com/method/{method}'
    response = requests.get(url, params=payload)
    response = response.json()
    if 'error' in response:
        inform_error(response)
        return None
    response = response.get('response')
    return response

def post_request(url, params, files):
    response = requests.post(url, params=params, files=files)
    response = response.json()
    if 'error' in response:
        inform_error(response)
        return None
    return response

def get_vk_token(vk_token):
    load_dotenv()
    if not vk_token:
        vk_token = os.getenv("VK_TOKEN")
    return vk_token

def get_vk_group_id(group_id):
    load_dotenv()
    if not group_id:
        group_id = os.getenv("GROUP_ID")
    return group_id

def inform_error(response):
    response = response.get('error')
    error_message = response.get('error_msg')
    logging.error(f'VK error: {error_message}')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VK photo auto publisher')
    parser.add_argument('-t', '--token', help='Add your own VK Token')
    parser.add_argument('-id', '--group_id', help='Add your own VK Group ID')

    args = parser.parse_args()

    comics_number_from = 1

    try:
        comics_number_till = get_last_comics_number()
    except requests.exceptions.ConnectionError:
        logging.error(f'Connection Error: Please check your Internet connection and try later.')
        exit()

    comics_number = random.randint(comics_number_from,comics_number_till)

    try:
        comics_properties = get_comics_properties(comics_number)
    except requests.exceptions.ConnectionError:
        logging.error(f'Connection Error: Please check your Internet connection and try later.')
        exit()

    comics_url = comics_properties.get('img')
    comics_description = comics_properties.get('alt')
    comics_filename = f'comics-{comics_number}.png'

    try:
        download_image(comics_url, comics_filename)
    except requests.exceptions.ConnectionError:
        logging.error(f'Connection Error: Please check your Internet connection and try later.')
        exit()

    print(f'Ok, {comics_filename} will be published.')

    vk_token = args.token
    group_id = args.group_id

    if not vk_token:
        logging.info('VK Token was not provided. Trying get credentials from .env file...')
        vk_token = get_vk_token(vk_token)

    if not group_id:
        logging.info('VK Group ID was not provided. Trying get credentials from .env file...')
        group_id = get_vk_group_id(group_id)

    method = 'photos.getWallUploadServer'
    payload = {'access_token': vk_token, 'v': 5.101, 'no_agreement': 1}

    response = get_vk_response(method, payload)
    if not response:
        os.remove(comics_filename)
        exit()

    with open(comics_filename, 'rb') as file:
        url = response.get('upload_url')
        files = {'photo': file}
        response = post_request(url,None,files)
        if not response:
            os.remove(comics_filename)
            exit()

    server = response.get('server')
    photo = response.get('photo')
    received_hash = response.get('hash')

    method = 'photos.saveWallPhoto'
    payload.update({'server':server, 'photo':photo, 'hash': received_hash})

    url = f'https://api.vk.com/method/{method}'

    response = post_request(url, payload, None)
    if not response:
        os.remove(comics_filename)
        exit()

    set_of_parameters = response['response'][0]
    media_id = set_of_parameters.get('id')
    owner_id = set_of_parameters.get('owner_id')
    attachments = f'photo{owner_id}_{media_id}'

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
    if not response:
        os.remove(comics_filename)
        exit()

    os.remove(comics_filename)
    print('Please check your new post at the Wall. Good buy.')