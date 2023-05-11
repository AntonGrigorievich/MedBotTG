from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from config import ADMIN_ID

from app import bot, dp
from states import *
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

@dp.message_handler(text='❤Симптомы')
async def start_self_diagnosis(message: Message):
    await message.answer("""
    Ответьте на несколько вопросов и мы предположим что с вами случилось.\n
    1/5) Какая у вас температура?
    """, reply_markup=None)

    await SelfDiagnosis.first()

@dp.message_handler(state=SelfDiagnosis.nose_question)
async def diagnosis_start(message: Message, state: FSMContext):
    await state.update_data(
        temp_status = message.text
    )

    await message.answer("""
    2/5) Вас беспокоят проблемы с носом?
    """, reply_markup=None)

    await SelfDiagnosis.next()

@dp.message_handler(state=SelfDiagnosis.headache_question)
async def diagnosis_start(message: Message, state: FSMContext):
    await state.update_data(
        nose_status = message.text
    )

    await message.answer("""
    3/5) У вас болит голова?
    """, reply_markup=None)

    await SelfDiagnosis.next()

@dp.message_handler(state=SelfDiagnosis.cough_question)
async def diagnosis_start(message: Message, state: FSMContext):
    await state.update_data(
        headache_status = message.text
    )

    await message.answer("""
    4/5) Вас беспокоит кашель?
    """, reply_markup=None)

    await SelfDiagnosis.next()

@dp.message_handler(state=SelfDiagnosis.scrappiness_question)
async def diagnosis_start(message: Message, state: FSMContext):
    await state.update_data(
        cough_status = message.text
    )

    await message.answer("""
    5/5) Вы ощущаете ломоту?
    """, reply_markup=None)

    await SelfDiagnosis.next()

@dp.message_handler(state=SelfDiagnosis.final_state)
async def diagnosis_start(message: Message, state: FSMContext):
    await state.update_data(
        scrappiness_status = message.text
    )

    res = dp.storage

    await message.answer(res, reply_markup=MenuKeyboard)

    await state.reset_state()