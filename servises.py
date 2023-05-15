from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


### Файл для второстепенных функций

# Данная функция анализирует поступившие в нее данные пользователя и предпологает его диагноз
def detect_diagnosis(data):
    data = [el for el in data]
    res = 'Возможные диагнозы:\n'
    if ('less36.6' in data) and ('normal_head' not in data):
        res += '''• Головная боль напряжения, менингит\n
Возможно, требуется экстренная медицинская помощь!\n'''
    elif 'normal' not in ''.join(data):
        res += """• Простуда, коронавирусная инфекция\n"""
    elif ('dry' in data) and ('normal_head' not in data) and ('scrappy' in data):
        res += '• Пневмония, бронхит\n'
    elif ('wet' in data) and ('runny' in data):
        res += '• Вирусная инфекция горла, простуда\n'
    elif ('scrappy' in data) and ('pressure' in data):
        res +='• растяжение мышц шеи'

    if res == 'Возможные диагнозы:\n':
        res = 'Не удалось определить диагноз\n'
    
    res += """
Записаться на приём к врачу можно через Госуслуги, лично и по телефону.\n
Госуслуги - https://gosuslugi.ru/\n
Телефон - 8 (495) 000-00-00\n
    """
    return res

# Данная функция формирует ответ на вопрос, основываясь на ключевых словах
def find_keywords(text):
    text = text.lower()
    res = ''
    if 'запис' in text:
        res += """
Записаться на приём к врачу можно через Госуслуги, лично и по телефону.\n
Госуслуги - https://gosuslugi.ru/\n
Телефон - 8 (495) 000-00-00\n
    """
    elif 'анализ' in text and 'результ' in text:
        res += 'Результаты анализов можно узнать лично и по телефону.\nТелефон - 8 (495) 000-00-00\n'
    elif 'распис' in text or 'время' in text:
        res += 'Время работы и приема можно узнать на сайте https://gosuslugi.ru/'
    elif 'справк' in text and 'получ' in text:
        res += 'Для получения медецинской справки ребенку не нужны документы, взрослому потребуется взять паспорт.'
    elif 'страхов' in text and 'плат' in text:
        res += 'За счет медецинской страховки можно оплатить комплексное обследование.'
    else:
        res += 'Бот не смог найти ответ на данный вопрос'
    return res


# Данная функция создает клавиатуру для администратора, основываясь на информации из базы данных
support_admin_callback = CallbackData('admin_answer', 'question_id', 'user_id')
def create_support_keyboard(data):
    # Создание клавиатуры для службы поддержки
    SupportAdminKeyboard = InlineKeyboardMarkup(row_width=1)
    for id, user_id, text in data:
        SupportAdminKeyboard.insert(InlineKeyboardButton(
            text=text,
            callback_data=support_admin_callback.new(question_id=f'{id}', user_id=f'{user_id}')
            )
        )
    return SupportAdminKeyboard