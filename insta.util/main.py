import time
from instabot import Bot
from datetime import datetime

def get_credentials():
  username = input('Please enter your Instagram User name: ')
  password = input('Please enter your Instagram password: ')
  bot = Bot()
  request = bot.login(username = username, password = password)
  if not request:
      print('''
      ******************************
      * Wrong Username or Password *
      ******************************
      ''')
      input('Press Enter to exit')
      return None
  else:
      credentials=[username,password]
      return credentials

def create_blocklist(blocklist):
    print('--------------------------------')
    critical_following = int(input('Please enter critical number of "following": '))
    print('--------------------------------')
    followers = bot.get_user_followers(username)
    for insta_id in followers:
        follower_name = bot.get_user_info(insta_id)
        following_count = int(follower_name.get('following_count'))
        if following_count > critical_following:
            blocklist.append(insta_id)
    return blocklist, critical_following


def get_usercatalog(array):
    current_time = str(datetime.now()) + '\n'
    write_history(current_time)
    for number, insta_id in enumerate(array):
        follower_name = bot.get_user_info(insta_id)
        catalog_string = 'Number: ' + str(number) + '| Instagram name: ' + str(follower_name.get('username')) + '| Following: ' + str(follower_name.get('following_count'))
        print(catalog_string)
        write_history(catalog_string)


def check_exclude_list(array):
    array = array.split(',')
    try:
        array = [int(element) for element in array]
        array = set(array)
        array = sorted(array, reverse=True)
        return array
    except:
        print('Something wrong... Please check your exclude list.')
        return None

def unfollowing_users(array, critical_following):
    bot.max_following_to_block = critical_following
    text = '''
    -------------------
    Working with users...
    -------------------'''
    print(text)
    write_history(text)
    get_usercatalog(array)
    bot.block_users(array)
    print('-------------------')
    print('Let`s wait 10 seconds...')
    print('-------------------')
    time.sleep(10)
    bot.unblock_users(array)

def write_history(text):
    text = text + '\n'
    with open('history.txt', 'a') as file:
        file.write(text)



if __name__ == '__main__':

    print('''
    ***************************
    * Instagram util.
    * Idea: -> Svetlana Pozdnyakova
    * Hands: -> Anton Pozdnyakov (anton.pozdnyakov.i@gmail.com)
    * Version: 2019.09
    This simple scrip unfollow users, who have a big 'following' status.
    It`s free and there is no any kind of responsibility ;)
    ! To stop this script please press Ctrl+C
    ! Please read README.md for detailed information.
    ***************************
    ''')
    print('--------------------------------')
    input('Please press Enter to continue...')
    print('--------------------------------')


    username, password = get_credentials()

    bot = Bot()
    bot.login(username = username, password = password)

    blocklist = []
    blocklist, critical_following = create_blocklist(blocklist)



    if not len(blocklist):
        print('-------------------')
        print('There are no users with this number of "following": ', critical_following)
        print('-------------------')

    else:
        print('-------------------')
        print('Please wait...')
        print('-------------------')

        get_usercatalog(blocklist)

        print('-------------------')
        exclude_users = input('PLease enter _numbers_ to _exlcude_ with comma(for example: 3,5): ')
        print('-------------------')

        if len(exclude_users):
            exclude_users = check_exclude_list(exclude_users)
            if not exclude_users:
                print ('...and after that, please start the script again...')
            else:
                for element in exclude_users:
                    del blocklist[element]
                unfollowing_users(blocklist, critical_following)
        else:
            unfollowing_users(blocklist, critical_following)

    print('-------------------')
    input('''
    Good bye...
    ... and if you wanna buy some coffee for authors,
    please follow this link:
    ***********************
    https://paypal.me/AntonPozdnyakov
    ***********************
    Press Enter to exit''')