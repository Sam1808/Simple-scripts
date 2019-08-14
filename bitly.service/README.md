#### Bitly url shorterer

This project was create to:
 - make short links with **bitly.com** (www.bitly.com) service
 - to count clicks with exists short links 

###### How to install

For use you need:
- python3 (www.python.org)
- pip3 (to install soft from requirements.txt)
- special TOKEN from bitly.com [https://bitly.is/2Z2tgNf] and of course registration on bitly.com

When Python3 & pip3 is already installed, please use pip3 to install dependencies:

`pip install -r requirements.txt`

###### How to use

This script uses with command line interface(CLI).

`python3 script.py URL`

Where:
- python3 - python executable file
- script.py - name of this script
- URL - url for count clicks or make shot url

Examples:

1. `python3 script.py https://www.googe.com` - make short bit.ly link for www.google.com
2. `python3 script.py bitly.is/2Z2tgNf` - count clicks for this short link
3. `python3 script.py www.googe.com` - raise error: please use http(s) prefix

###### Project Goals

The code is written for educational purposes on online-course for web-developers www.dvmn.org.
