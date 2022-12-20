from decouple import config
from random import choice, randint

import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = config('APIKEY')
CorrectAnswers = 0
IncorrectAnswers = 0
GameIsGoing = False
RightEquation = ''
g_keyboard = types.ReplyKeyboardMarkup()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global GameIsGoing
    if not GameIsGoing:
        await message.reply("Начнём игру")
        GameIsGoing = True
        global RightEquation
        RightEquation = f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'
        g_keyboard.add(types.KeyboardButton(RightEquation))
        for i in range(3):
            g_keyboard.add(types.KeyboardButton(f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'))
        await message.reply(eval(RightEquation), reply_markup=g_keyboard)
    else:
        await message.reply('Игра уже идёт')

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ - математический игробот версии 2.0\nПравила игры такие: я даю тебе число, а ты на клавиатуре выбираешь результатом какого выражения может быть это число\nЧтобы начать игру напиши /start\nЧтобы остановить игру напиши /stop_game")

    
@dp.message_handler(commands=['stop_game'])
async def send_welcome(message: types.Message):
    global GameIsGoing
    global CorrectAnswers
    global IncorrectAnswers
    if GameIsGoing:
        await message.reply(f"Игра окончена, вот результаты\nКоличество правильных ответов: {CorrectAnswers}\nКоличество неправильных ответов: {IncorrectAnswers}")
        GameIsGoing = False
        if CorrectAnswers > IncorrectAnswers:
            await message.reply('\U0001F642')
        else:
            await message.reply('\U0001F61E')
        CorrectAnswers = 0
        IncorrectAnswers = 0
        global g_keyboard
        g_keyboard = types.ReplyKeyboardMarkup()
    else:
        await message.reply('Ты ещё не начал игру\nЧтобы начать игру напиши /start')
        
@dp.message_handler()
async def echo(message: types.Message):
    global RightEquation
    global g_keyboard
    if GameIsGoing:
        if message.text == RightEquation:
            global CorrectAnswers
            CorrectAnswers += 1
            await message.reply('Правильно')
            g_keyboard = types.ReplyKeyboardMarkup()
            RightEquation = f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'
            g_keyboard.add(types.KeyboardButton(RightEquation))
            for i in range(3):
                g_keyboard.add(types.KeyboardButton(f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'))
            await message.reply(eval(RightEquation), reply_markup=g_keyboard)
        else:
            global IncorrectAnswers
            IncorrectAnswers += 1
            await message.reply('Неравильно')
            g_keyboard = types.ReplyKeyboardMarkup()
            RightEquation = f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'
            g_keyboard.add(types.KeyboardButton(RightEquation))
            for i in range(3):
                g_keyboard.add(types.KeyboardButton(f'{randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)} {choice(["+", "-", "*", "/"])} {randint(1, 100)}'))
            await message.reply(eval(RightEquation), reply_markup=g_keyboard)
    else:
        await message.reply('Ты ещё не начал игру\nЧтобы начать игру напиши /start')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)