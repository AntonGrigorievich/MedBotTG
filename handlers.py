from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from config import ADMIN_ID

from app import bot, dp
from states import *
from keyboards.reply import *
from keyboards.inline import *
from servises import *


async def admin_startup(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')

@dp.message_handler(Command('start'))
async def show_menu(messge: Message):
    await messge.answer('Как мы можем вам помочь?', reply_markup=MenuKeyboard)


""" Обработчики кнопок основного меню """
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

@dp.message_handler(text='☎ Обратиться в поддержку')
async def ask_support(message: Message):
    await message.answer("Задайте ваш вопрос в текстовом сообщении")

@dp.message_handler(text='❤Симптомы')
async def start_self_diagnosis(message: Message):
    await message.answer("""
    Ответьте на несколько вопросов и мы предположим что с вами случилось.\n
    1/5) Какая у вас температура?
    """, reply_markup=TempKeyboard)

    await SelfDiagnosis.first()


""" Обработчики кнопок теста самодиагностики """
@dp.callback_query_handler(symptom_callback.filter(symp_name='temp'), state=SelfDiagnosis.nose_question)
async def diagnosis_question_nose(call: CallbackData, callback_data: dict, state: FSMContext):
    await call.answer()
    await state.update_data(
        temp_status = callback_data['symp_status']
    )
    await call.message.edit_text('2/5) Вас беспокоят проблемы с носом?')
    await call.message.edit_reply_markup(NoseKeyboard)
    await SelfDiagnosis.next()

@dp.callback_query_handler(symptom_callback.filter(symp_name='nose'), state=SelfDiagnosis.headache_question)
async def diagnosis_question_head(call: CallbackData, callback_data: dict, state: FSMContext):
    await call.answer()
    await state.update_data(
        nose_status = callback_data['symp_status']
    )
    await call.message.edit_text('3/5) У вас болит голова?')
    await call.message.edit_reply_markup(HeadKeyboard)

    await SelfDiagnosis.next()

@dp.callback_query_handler(symptom_callback.filter(symp_name='head'), state=SelfDiagnosis.cough_question)
async def diagnosis_question_cough(call: CallbackData, callback_data: dict, state: FSMContext):
    await call.answer()
    await state.update_data(
        head_status = callback_data['symp_status']
    )
    await call.message.edit_text('4/5) Вас беспокоит кашель?')
    await call.message.edit_reply_markup(CoughKeyboard)
    
    await SelfDiagnosis.next()

@dp.callback_query_handler(symptom_callback.filter(symp_name='cough'), state=SelfDiagnosis.scrappiness_question)
async def diagnosis_question_body(call: CallbackData, callback_data: dict, state: FSMContext):
    await call.answer()
    await state.update_data(
        cough_status = callback_data['symp_status']
    )
    await call.message.edit_text('5/5) Вы ощущаете ломоту?')
    await call.message.edit_reply_markup(BodyKeyboard)
    
    await SelfDiagnosis.next()

@dp.callback_query_handler(symptom_callback.filter(symp_name='body'), state=SelfDiagnosis.final_state)
async def diagnosis_final(call: CallbackData, callback_data: dict, state: FSMContext):
    await call.answer()
    await state.update_data(
        body_status = callback_data['symp_status']
    )
    res = ''

    async with state.proxy() as data:
        res = detect_diagnosis(data.values())

    await state.reset_state()

    await call.message.edit_text(res)
    await call.message.delete_reply_markup()

@dp.callback_query_handler(text='cancel', state='*')
async def cancel_test(call: CallbackQuery, state: FSMContext):
    await call.answer('Тест завершён')
    await state.reset_state()
    await call.message.delete_reply_markup()
    await call.message.edit_text('Тест завершён')