import datetime
import logging
import telegram
import timer3

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

logging.basicConfig()


class Bot():

    def __init__(self, api_key):
        if not api_key:
            raise(ValueError("Токен не указан"))
        self.api_key = api_key
        # self.user_id = user_id
        self.bot = telegram.Bot(token=api_key)
        self.logger = logging.getLogger('tbot')
        self.updater = Updater(self.api_key)
        self.dispatcher = self.updater.dispatcher
        self.logger.debug('Bot initialized')

    def send_message(self, chat_id, message):
        self.logger.debug(f'Message send: {message}')
        return self.bot.send_message(chat_id=chat_id, text=message).message_id

    def update_message(self, chat_id, message_id, new_message):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_message)
        self.logger.debug(f'Update message {message_id}: {new_message}')

    def create_timer(self, timeout_secs, callback, *args, **kwargs):
        if not callable(callback):
            raise TypeError('Ожидаем функцию на вход')
        if not timeout_secs:
            raise TypeError("Не могу запустить таймер на None секунд")
        timer3.apply_after(timeout_secs * 1000, callback, args=args, kwargs=kwargs)

    def create_countdown(self, timeout_secs, callback, **kwargs):
        if not callable(callback):
            raise TypeError('Ожидаем функцию на вход')
        if not timeout_secs:
            raise TypeError("Не могу запустить таймер на None секунд")

        def callback_wrapper(**kwargs):
            now_timestamp = datetime.datetime.now().timestamp()
            secs_left = int(timeout_secs - now_timestamp + start_timestamp)
            try:
                callback(**kwargs, secs_left=secs_left)
            finally:
                if not max(secs_left, 0):
                    timer.stop()

        start_timestamp = datetime.datetime.now().timestamp()
        timer = timer3.Timer()
        timer.apply_interval(1000, callback_wrapper, kwargs=kwargs)

    def wait_for_msg(self, callback):
        if not callable(callback):
            raise TypeError('Ожидаем функцию на вход')

        def handle_text(bot, update):
            users_reply = update.message.text
            callback(users_reply)

        self.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
        self.updater.start_polling()
        self.updater.idle()
