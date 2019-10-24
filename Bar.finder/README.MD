#### TITLE

This project was create to:
 - reason 1 
 - reason 2  

###### How to install

For use you need:
- python3 (www.python.org)
- pip3 (to install soft from requirements.txt)
- access to API YANDEX.ru with secret key [https://api.superjob.ru/]

When Python3 & pip3 is already installed, please use pip3 to install dependencies:

`pip install -r requirements.txt`

###### How to use

This script uses with command line interface(CLI) with options.

`python3 main.py [options]`

Where:
- python3 - python executable file
- main.py - name of this script

Provided options:
-h  - Help
-l  - put your location
-sl - show log



Description:

Script uses HH.ru API [https://dev.hh.ru/] and SuperJob API [https://api.superjob.ru/] 



##### Important
Make your life more happy - use python dotenv library (https://bit.ly/2L5Lsg2) to hide your keys from enemy eyes :). 
Make your **.env** text file at the same folder with:

`SUPERJOB_KEY = your_secret_key`


###### Project Goals

The code is written for educational purposes on online-course for web-developers www.dvmn.org.
