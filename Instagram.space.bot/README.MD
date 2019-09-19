#### Instagram space bot

This project was create to:
 - downloading space photos...
 - ...and upload its to your Insta account 

###### How to install

For use you need:
- python3 (www.python.org)
- pip3 (to install soft from requirements.txt)
- account at Instagram [https://www.instagram.com] and of course LOGIN and PASSWORD

When Python3 & pip3 is already installed, please use pip3 to install dependencies:

`pip install -r requirements.txt`

###### How to use

This script uses with command line interface(CLI).

`python3 main.py [options]`

Where:
- python3 - python executable file
- main.py - name of this script
- options - options to create folder and download images. To list all options please use:

`python3 main.py --help` 

Examples:

`python3 main.py -p Pictures -s https://api.spacexdata.com/v3/launches/82 -ha 3892`

Where:

`-p` Folder name for pictures (default is 'Images');

`-s` URL with http(s) prefix to download SpaceX images;

`-ha` Hubble`s image ID

Description:

Script uses SpaceX API [http://bit.ly/2N2V9Pz] and Habble API [http://bit.ly/2UKQgLT] 



##### Important
Make your life more happy - use python dotenv library (https://bit.ly/2L5Lsg2) to hide your login&password from enemy eyes :). 
Make your **.env** text file at the same folder with:

`INSTA_LOGIN=your_login`

`INSTA_PASS=your_password`


###### Project Goals

The code is written for educational purposes on online-course for web-developers www.dvmn.org.
