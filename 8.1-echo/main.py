from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F


from config_reader import config

token = config.bot_token.get_secret_value()

bot = Bot(token=token)
dp = Dispatcher()


async def command_start(message: Message):
    await message.answer('Привет\nЯ эхо-бот\nНапиши мне что нибудь')

async def command_help(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

async def send_echo(message: Message):
    await message.reply(text=message.text)

async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

dp.message.register(command_start, Command(commands='start'))
dp.message.register(command_help, Command(commands='help'))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)