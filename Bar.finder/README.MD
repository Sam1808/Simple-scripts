#### TITLE

This project was create to:
 - to find Bar on map 
 - to break mind with YA API(http://bit.ly/363xe96)

###### How to install

For use you need:
- python3 (www.python.org)
- pip3 (to install soft from requirements.txt)
- access to API YANDEX.ru with secret key(http://bit.ly/363xe96)
- JSON database file(http://bit.ly/32KGz3l) with Moscow bars

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

###### Examples

`python3 main.py -l 'охотный ряд'`

Find bars near 'охотный ряд'.

`python3 main.py -l 'метро аннино' -sl YES`

Find bars near 'метро аннино' and see info messages.



Description:

Script uses Moscow bars datebase and Yandex API.
After run of script please enter URL http://0.0.0.0:5000/ at your brouser to see bar map.
To stop script press Ctrl+C


##### Important
Make your life more happy - use python dotenv library (https://bit.ly/2L5Lsg2) to hide your keys from enemy eyes :). 
Make your **.env** text file at the same folder with:

`YA_TOKEN= your_secret_key`


###### Project Goals

The code is written for educational purposes on online-course for web-developers www.dvmn.org.
