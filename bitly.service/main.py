import requests
import os
from dotenv import load_dotenv
import argparse

def url2bitly(original_url, your_token):
  headers={"Authorization": your_token}
  payload = {"long_url": original_url}
  response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=payload)
  answer = response.json()
  if answer.get('message') == 'INVALID_ARG_LONG_URL':
      return None
  else:
      return answer.get('link')

def count_clicks(bitlink, your_token):
    headers = {"Authorization": your_token}
    click_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks'
    payload = {'unit':'day'}
    response = requests.get(click_url.format(bitlink), headers=headers, params=payload)
    response.raise_for_status()
    answer = response.json().get("link_clicks")
    if len(answer) == 0:
        return None
    else:
        return answer


if __name__ == "__main__":

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL to create bitly link or count exist link")
    args = parser.parse_args()

    original_url = args.URL

    if not os.getenv("BITLY_TOKEN"):
        your_token = "Bearer " +  input('Please enter your token: ')
    else:
        your_token = "Bearer " + str(os.getenv("BITLY_TOKEN"))


    if original_url.startswith('bit.ly'):
        try:
            result = count_clicks(original_url, your_token)
            if result:
                for element in result:
                    print ('Date: ', element.get('date')[:10],'Clicks: ',element.get('clicks'))
            else:
                print ('There are no clicks.')
        except requests.exceptions.HTTPError:
            result = '''Error. Invalid URL.
            Please input URL correctly and w/o http(s)-prefix'''
            print(result)
    else:
        result = url2bitly(original_url, your_token)
        if not result:
            print('''Error. Invalid URL.
            Please input right URL with http(s) prefix.''')
        else:
            print ('Your shot url is:', result)

    print ('Good Bye!')
