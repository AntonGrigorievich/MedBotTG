from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from config import ADMIN_ID

from app import bot, dp
from keyboards.reply import *

async def admin_startup(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')

@dp.message_handler(Command('start'))
async def show_menu(messge: Message):
    await messge.answer('Как мы можем вам помочь?', reply_markup=MenuKeyboard)

@dp.message_handler(text='📍 Помощь')
async def bot_help(message: Message):
    await message.answer("""
    Данный обладает следующим функционалом:\n
    • 📋Записаться к врачу - данная кнопка позволяет записаться на прием к врачу, которого вы желаете посетить (в случае, если запись бесплатна).\n
    • ❤Симптомы - Данная кнопка позволяет провести самодиагностику.\n
    • ❔ Задать вопрос - Данная кнопка позволяет спросить у бота часто задаваемый вопрос (быстро но неточно).\n
    • i Информация - Данная кнопка позволяет получить справочную информацию, касающуюся Орской больницы, ее филиалов и сотрудников.\n
    • ☎ Обратиться в поддержку - Данная кнопка позволяет обратиться за помощью к реальному человеку (медленно но верно).\n
    """)

@dp.message_handler(text='📋 Записаться к врачу')
async def make_appointment(message: Message):
    await message.answer("""
    Записаться на приём к врачу можно через Госуслуги, лично и по телефону.\n
    Госуслуги - https://gosuslugi.ru/\n
    Телефон - 8 (495) 000-00-00\n
    """
    )