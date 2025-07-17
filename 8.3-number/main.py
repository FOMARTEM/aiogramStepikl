from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from config_reader import config

token = config.bot_token.get_secret_value()

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer('Привет! Я бот "Угадай Число".'
                         'Предлагаю поиграть со мной)\n'
                         'Отправь /help что бы ознакомиться с правилами'
    )


if __name__ == '__main__':
    dp.run_polling(bot)