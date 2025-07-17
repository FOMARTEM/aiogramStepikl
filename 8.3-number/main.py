from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from config_reader import config

token = config.bot_token.get_secret_value()

bot = Bot(token=token)
dp = Dispatcher()



if __name__ == '__main__':
    dp.run_polling(bot)