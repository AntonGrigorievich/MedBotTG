from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from config import ADMINS_ID

from app import bot, dp, db
from states import *
from keyboards.reply import *
from keyboards.inline import *
from servises import *


"""Админские обработчики"""
async def admin_startup(dp):
    for id in ADMINS_ID:
        await bot.send_message(chat_id=id, text='Бот запущен')

@dp.message_handler(Command('user_questions'))
async def get_user_questions(message: Message):
    if message.from_id not in ADMINS_ID:
        await message.answer(f'У вас нет доступа к этой команде.')
    else:
        questions_data = db.get_questions()
        if questions_data:
            kb = create_support_keyboard(questions_data)
            await message.answer('Выберите вопрос, на который вы можете дать ответ', reply_markup=kb)
        else:
            await message.answer('В данный момент вопросов нет.')

@dp.message_handler(Command('start'))
async def show_menu(messge: Message):
    await messge.answer('Как мы можем вам помочь?', reply_markup=MenuKeyboard)


""" Обработчики кнопок основного меню """
@dp.message_handler(text='📍 Помощь', state='*')
async def bot_help(message: Message):
    await message.answer("""
Данный обладает следующим функционалом:\n
    • 📋Записаться к врачу - данная кнопка позволяет записаться на прием к врачу, которого вы желаете посетить (в случае, если запись бесплатна).\n
    • ❤Симптомы - Данная кнопка позволяет провести самодиагностику.\n
    • ❔ Задать вопрос - Данная кнопка позволяет спросить у бота часто задаваемый вопрос (быстро но неточно).\n
    • i Информация - Данная кнопка позволяет получить справочную информацию, касающуюся Орской больницы, ее филиалов и сотрудников.\n
    • ☎ Обратиться в поддержку - Данная кнопка позволяет обратиться за помощью к реальному человеку (медленно но верно).\n
    """)

@dp.message_handler(text='📋 Записаться к врачу', state='*')
async def make_appointment(message: Message):
    await message.answer("""
    Записаться на приём к врачу можно через Госуслуги, лично и по телефону.\n
Госуслуги - https://gosuslugi.ru/\n
Телефон - 8 (495) 000-00-00\n
    """
    )

@dp.message_handler(text='☎ Обратиться в поддержку')
async def start_support_state(message: Message):
    await message.answer("Задайте ваш вопрос в текстовом сообщении", reply_markup=None)

    await SupportQuestion.first()

@dp.message_handler(state=SupportQuestion.support_question)
async def confirm_support_question(message: Message, state: FSMContext):
    await state.update_data(
        user_id = message.from_id,
        question = message.text
    )

    await message.answer(
        text=f"""Ваш вопрос: {message.text}\n
Вы уверены что хотите отправить его в службу поддержки?""",
        reply_markup=QuestionConfirmKeyboard)
    
    await SupportQuestion.next()


@dp.callback_query_handler(question_confirm_callback.filter(confirmation='True'), state=SupportQuestion.support_question_confirm)
async def accept_question(call: CallbackData, state: FSMContext):
    await call.answer('Вопрос принят в обработку')
    async with state.proxy() as data:
        user_id = data.as_dict()['user_id']
        question = data.as_dict()['question']
        db.add_question(user_id, question)

    await state.finish()

    await call.message.edit_text('Ваш вопрос принят в обработку')
    await call.message.edit_reply_markup()

@dp.callback_query_handler(question_confirm_callback.filter(confirmation='False'), state=SupportQuestion.support_question_confirm)
async def accept_question(call: CallbackData, state: FSMContext):
    await call.answer('Отмена отправления вопроса')

    await state.finish()

    await call.message.edit_text('Отправление вопроса отменено')
    await call.message.delete_reply_markup()

""" Обработчики кнопок теста самодиагностики """
@dp.message_handler(text='❤Симптомы')
async def start_self_diagnosis(message: Message):
    await message.answer("""
    Ответьте на несколько вопросов и мы предположим что с вами случилось.\n
    1/5) Какая у вас температура?
    """, reply_markup=TempKeyboard)

    await SelfDiagnosis.first()

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