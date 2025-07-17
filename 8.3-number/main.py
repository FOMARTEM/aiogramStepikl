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

@dp.message(Command(commands='help'))
async def command_help_handler(message: Message) -> None :
    """
    This handler receives messages with `/help` command
    """
    await message.answer('Команды:\n'
                         '/start - перезапуск бота\n'     
                         '/cancel - выход из текущей игры\n'
                         '/help - вывод руководства пользователя\n'
                         'Правила игры\n'
                         'Я загадываю число, а Вы пытаетесь угадать его,'
                         'в случае если не угадываете я даю подсказку, больше или меньше.\n'
                         'Что бы сыграть нажмите на кнопку Сыграем'
    )

if __name__ == '__main__':
    dp.run_polling(bot)