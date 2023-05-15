from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


"""Клавиатуры для службы поддержки"""
question_confirm_callback = CallbackData('question', 'confirmation')

QuestionConfirmKeyboard = InlineKeyboardMarkup()

question_button_yes = InlineKeyboardButton(
    text='Да ✅',
    callback_data=question_confirm_callback.new(confirmation='True')
)

question_button_no = InlineKeyboardButton(
    text='Нет ❌',
    callback_data=question_confirm_callback.new(confirmation='False')
)

QuestionConfirmKeyboard.insert(question_button_yes)
QuestionConfirmKeyboard.insert(question_button_no)

question_action_callback = CallbackData('admin_select', 'action')

QuestionActionSelectKeyboard = InlineKeyboardMarkup()

admin_question_answer = InlineKeyboardButton(
    text='Ответить 🗣️',
    callback_data=question_action_callback.new(action='answer')
)
admin_question_delete = InlineKeyboardButton(
    text='Удалить ❌',
    callback_data=question_action_callback.new(action='delete')
)
QuestionActionSelectKeyboard.insert(admin_question_answer)
QuestionActionSelectKeyboard.insert(admin_question_delete)


"""Клавиатупры теста самодиагностики"""
symptom_callback = CallbackData('symp', 'symp_name', 'symp_status')
cancel_callback = CallbackData('cancel', 'status')

#данныя кнопка будет использоваться для завершения теста самодиагностики на любой его стадии
cancel_button = InlineKeyboardButton(
    text='Закончить тест 🚪',
    callback_data='cancel'
)

# клавиатуры, осуществляющие функционал саомдиагностики
# Вопрос 1
TempKeyboard = InlineKeyboardMarkup(row_width=3)

temp_button1 = InlineKeyboardButton(
    text='Меньше 36.6',
    callback_data=symptom_callback.new(symp_name='temp', symp_status='less36.6')
)
temp_button2 = InlineKeyboardButton(
    text='Около 36.6',
    callback_data=symptom_callback.new(symp_name='temp', symp_status='36.6')
)
temp_button3 = InlineKeyboardButton(
    text='Больше 36.6',
    callback_data=symptom_callback.new(symp_name='temp', symp_status='>36.6')
)

TempKeyboard.insert(temp_button1)
TempKeyboard.insert(temp_button2)
TempKeyboard.insert(temp_button3)
TempKeyboard.insert(cancel_button)

# Вопрос 2
NoseKeyboard = InlineKeyboardMarkup(row_width=3)

nose_button1 = InlineKeyboardButton(
    text='Сухость',
    callback_data=symptom_callback.new(symp_name='nose', symp_status='dryness')
)
nose_button2 = InlineKeyboardButton(
    text='Проблем нет',
    callback_data=symptom_callback.new(symp_name='nose', symp_status='normal_nose')
)
nose_button3 = InlineKeyboardButton(
    text='Насморк',
    callback_data=symptom_callback.new(symp_name='nose', symp_status='runny')
)

NoseKeyboard.insert(nose_button1)
NoseKeyboard.insert(nose_button2)
NoseKeyboard.insert(nose_button3)
NoseKeyboard.insert(cancel_button)

# Вопрос 3
HeadKeyboard = InlineKeyboardMarkup(row_width=3)

head_button1 = InlineKeyboardButton(
    text='Мигрень (пульсирующая боль в половине головы)',
    callback_data=symptom_callback.new(symp_name='head', symp_status='migraine')
)
head_button2 = InlineKeyboardButton(
    text='Проблем нет',
    callback_data=symptom_callback.new(symp_name='head', symp_status='normal_head')
)
head_button3 = InlineKeyboardButton(
    text='Давление (напряжение головы)',
    callback_data=symptom_callback.new(symp_name='head', symp_status='pressure')
)

HeadKeyboard.insert(head_button1)
HeadKeyboard.insert(head_button2)
HeadKeyboard.insert(head_button3)
HeadKeyboard.insert(cancel_button)

# Вопрос 4
CoughKeyboard = InlineKeyboardMarkup(row_width=3)

cough_button1 = InlineKeyboardButton(
    text='Сухой кашель',
    callback_data=symptom_callback.new(symp_name='cough', symp_status='dry')
)
cough_button2 = InlineKeyboardButton(
    text='Проблем нет',
    callback_data=symptom_callback.new(symp_name='cough', symp_status='no_cough')
)
cough_button3 = InlineKeyboardButton(
    text='Влажный кашель',
    callback_data=symptom_callback.new(symp_name='cough', symp_status='wet')
)

CoughKeyboard.insert(cough_button1)
CoughKeyboard.insert(cough_button2)
CoughKeyboard.insert(cough_button3)
CoughKeyboard.insert(cancel_button)

# Вопрос 5
BodyKeyboard = InlineKeyboardMarkup(row_width=2)

body_button1 = InlineKeyboardButton(
    text='Ломота в теле',
    callback_data=symptom_callback.new(symp_name='body', symp_status='scrappy')
)
body_button2 = InlineKeyboardButton(
    text='Проблем нет',
    callback_data=symptom_callback.new(symp_name='body', symp_status='normal_body')
)
BodyKeyboard.insert(body_button1)
BodyKeyboard.insert(body_button2)
BodyKeyboard.insert(cancel_button)