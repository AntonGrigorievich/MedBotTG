from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MenuKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📋 Записаться к врачу'),
            KeyboardButton(text='❤Симптомы'),
            KeyboardButton(text='❔ Задать вопрос'),
        ],
        [
            KeyboardButton(text='ℹ︎ Информация'),
            KeyboardButton(text='☎ Обратиться в поддержку'),
            KeyboardButton(text='📍 Помощь'),
        ]
    ],
    resize_keyboard=True
)