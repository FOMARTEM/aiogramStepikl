from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
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

user = {
    'in_game' : False,
    'magic_number' : None,
    'attemps' : None,
    'games' : 0,
    'wins' : 0
}


@dp.message(CommandStart)
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        'Привет! Я бот "Угадай Число". '
        'Предлагаю поиграть со мной)\n'
        'Отправь /help что бы ознакомиться с правилами',
        reply_markup=keyboard
    )

@dp.message(Command(commands='start'))
async def command_help_handler(message: Message) -> None :
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f'Всего игр сыграно: {user["games"]}\n'
        f'Игр выиграно: {user["wins"]}',
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
        'Я загадываю число от 1 до 100, а Вы пытаетесь угадать его, '
        'в случае если не угадываете я даю подсказку, больше или меньше.\n'
        'Что бы сыграть нажмите на кнопку Сыграем',
        reply_markup=keyboard
    )

@dp.message(Command(commands='cancel'))
async def command_cancel_handler(message: Message) -> None:
    """
    This handler receives messages with `/cancel` command
    """
    if user["in_game"]:
        user["attemps"] = 0
        user["magic_numbe"] = 0
        user["games"] += 1
        user["in_game"] = False
    
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

    if user["in_game"]:
        await message.answer(
            'Вы уже находитеся в игре\n'
            'Что бы звершить текущую игру отправьте /cancel'
        )
        return
    user["in_game"] = True
    user["games"] += 1
    user["magic_numbe"] = randint(1, 100)
    user["attemps"] = 0
    print(user["magic_numbe"])
    await message.answer(
        'Я загадал число!\n'
        'Если захочешь завершить игру отправь /cancel',
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(F.text == 'В другой раз')
async def next_time(message: Message) -> None:
    """
    This handler receives messages with `В другой раз', for start game
    """

    if user["in_game"]:
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

@dp.message(F.text.regexp(r'^(100|[1-9][0-9]?)$'))
async def get_number(message: Message) -> None:
    """
    This handler receives messages with numbers
    """

    if not user["in_game"]:
        await message.answer('Мы ещё не начали играть(')
        return
    
    user["attemps"] += 1

    if int(message.text) == user["magic_numbe"]:
        user["in_game"] = False
        user["wins"]+=1
        user["magic_numbe"] = 0
        await message.answer(
            f"Поздравляем, Вы угадали число с {user["attemps"]} попытки\n"
            f"Ваша статистика: {user["wins"]}/{user["games"]}",
            reply_markup=keyboard
        )
    elif int(message.text) > user["magic_numbe"]:
        await message.answer('Не угодали, я загадал число меньше')
    else:
        await message.answer('Не угодали, я загадал число больше')
    
@dp.message()
async def wrong_message(message: Message):
    if user["in_game"]:
        await message.answer('Вы сейчас играете, пришлите число,'
                             ' либо для завершения игры команду /cancel'
        )
        return
    await message.answer('Я умею только играть, не ломай меня')

if __name__ == '__main__':
    dp.run_polling(bot)