import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
  iteration = min(total, iteration)
  percent = "{0:.1f}"
  percent = percent.format(100 * (iteration / float(total)))
  filled_length = int(length * iteration // total)
  pbar = fill * filled_length + zfill * (length - filled_length)
  return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify(time):
  message = f'The time is over! ({time} sec)'
  bot.send_message(chat_id, message)
  bot.send_message(chat_id, "How long to start the timer?")

def notify_progress(secs_left, msg_id, total):
  progress_message = render_progressbar(total, secs_left)
  secs_left_string = str(secs_left)
  message = f'{secs_left_string} seconds left! \n {progress_message}'
  bot.update_message(chat_id, msg_id, message)


def reply(text):
  time = parse(text)
  time_string = str(time)
  if time_string.isdigit(): # Test, if input is seconds
    message = f'Timer started for {time_string} seconds'
    bot.send_message(chat_id, message)
    message = f'{time_string} seconds left!'
    message_id = bot.send_message(chat_id, message)
    total_timer = time # Only for more readable code
    bot.create_countdown(total_timer, notify_progress, msg_id=message_id, total=total_timer)
    bot.create_timer(total_timer, notify, time)
  else:
    bot.send_message(chat_id, "Please enter the time (for example: 5s or 1.2m)")

def get_credentials():
  load_dotenv()
  token = os.getenv("TELE_TOKEN")
  chat_id =  os.getenv("CHAT_ID")
  if not token:
    token = input('Please enter your Telegram Token: ')
    chat_id = input('Please enter your Telegram own chat ID: ')
  credentials=[token,chat_id]
  return credentials

if __name__ == '__main__':
  token, chat_id = get_credentials()
  bot = ptbot.Bot(token)
  bot.send_message(chat_id, "How long to start the timer?")
  bot.wait_for_msg(reply)