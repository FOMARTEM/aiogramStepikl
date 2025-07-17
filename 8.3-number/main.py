from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton, 
    Message, 
    ReplyKeyboardMarkup
)
from aiogram import F

from config_reader import config

token = config.bot_token.get_secret_value()

bot = Bot(token=token)
dp = Dispatcher()

# Стандартная клавиатура для всей игры
kb = [
    [KeyboardButton(text="Сыграем")],
    [KeyboardButton(text="В другой раз")]
]
keyboard = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True
)

# Якобы глобальные переменные
# Побед
wins = 0
# Попыток
attemps = 0
# Игр
games = 0
# Загаданное число
magic_number = 0
#Состояние
in_game = False

@dp.message(Command(commands='start'))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer('Привет! Я бот "Угадай Число".'
                         'Предлагаю поиграть со мной)\n'
                         'Отправь /help что бы ознакомиться с правилами',
                        reply_markup=keyboard
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

@dp.message(Command(commands='cancel'))
async def command_cancel_handler(message: Message) -> None:
    """
    This handler receives messages with `/cancel` command
    """
    if in_game:
        attemps = 0
        magic_number = 0
        games+=1
    
    await message.answer(
        'Спасибо за игру!\n'
        'В случае если решите сыграть ещё раз нажимте на кнопку Сыграем',
        reply_markup=keyboard
    )
        




if __name__ == '__main__':
    dp.run_polling(bot)