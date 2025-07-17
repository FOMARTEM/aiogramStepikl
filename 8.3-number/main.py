from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton, 
    Message, 
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram import F

from random import randint

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
    await message.answer(
        'Привет! Я бот "Угадай Число".'
        'Предлагаю поиграть со мной)\n'
        'Отправь /help что бы ознакомиться с правилами',
        reply_markup=keyboard
    )

@dp.message(Command(commands='help'))
async def command_help_handler(message: Message) -> None :
    """
    This handler receives messages with `/help` command
    """
    await message.answer(
        'Команды:\n'
        '/start - перезапуск бота\n'     
        '/cancel - выход из текущей игры\n'
        '/help - вывод руководства пользователя\n'
        'Правила игры\n'
        'Я загадываю число, а Вы пытаетесь угадать его,'
        'в случае если не угадываете я даю подсказку, больше или меньше.\n'
        'Что бы сыграть нажмите на кнопку Сыграем',
        reply_markup=keyboard
    )

@dp.message(Command(commands='cancel'))
async def command_cancel_handler(message: Message) -> None:
    """
    This handler receives messages with `/cancel` command
    """
    global in_game, games, magic_number, attemps
    if in_game:
        attemps = 0
        magic_number = 0
        games+=1
        in_game = False
    
    await message.answer(
        'Спасибо за игру!\n'
        'В случае если решите сыграть ещё раз нажимте на кнопку Сыграем',
        reply_markup=keyboard
    )

@dp.message(F.text == 'Сыграем')
async def start_game(message: Message) -> None:
    """
    This handler receives messages with `Сыграем', for start game
    """
    global in_game, games, magic_number
    if in_game:
        await message.answer(
            'Вы уже находитеся в игре\n'
            'Что бы звершить текущую игру отправьте /cancel'
        )
        return
    in_game = True
    games+=1
    magic_number = randint(1, 100)
    await message.answer(
        'Я загадал число!'
        'Если захочешь завершить игру отправь /cancel',
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(F.text == 'В другой раз')
async def next_time(message: Message) -> None:
    """
    This handler receives messages with `В другой раз', for start game
    """

    global in_game

    if in_game:
        await message.answer(
            'Вы находитеся в игре\n'
            'Необходимо закончить игру /cancel'
        )
        return
    
    await message.answer(
        'Буду ждать тебя!\n'
        'Если надумешь поиграть нажми кнопку Сыграем\n'
        'Если запутался отправь /help'
    )



if __name__ == '__main__':
    dp.run_polling(bot)