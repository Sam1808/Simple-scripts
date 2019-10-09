#### VK photo auto publisher

This project was create to:
 - publish comics from Randall Munroe at your community a VK.com 
 

###### How to install

For use you need:
- python3 (www.python.org)
- pip3 (to install soft from requirements.txt)
- account at VK.com and registered application [https://vk.com/]
- VK Group and access Token  [https://vk.com/dev/implicit_flow_user]

When Python3 & pip3 is already installed, please use pip3 to install dependencies:

`pip install -r requirements.txt`

###### How to use

This script uses with command line interface(CLI).

`python3 main.py`

Where:
- python3 - python executable file
- main.py - name of this script

Provided options:

`python3 main.py -h` Help

`python3 main.py -id` Add your Group ID

`python3 main.py -t` Add your VK Token

You can combinate options. Example:

`python3 main.py -t 1q2w3e4r5t -id -987654321`

Where: 

`1q2w3e4r5t` - your own VK Token
`-987654321` - ID of your VK group with minus

Description:

Script uses XKCD API [https://xkcd.com] and VK.com API [https://vk.com/dev/api_requests] 


##### Important
Make your life more happy - use python dotenv library (https://bit.ly/2L5Lsg2) to hide your keys from enemy eyes :). 
Make your **.env** text file at the same folder with:

`VK_TOKEN='your VK token'`
`GROUP_ID= id of your VK group`

###### Project Goals

The code is written for educational purposes on online-course for web-developers www.dvmn.org.
