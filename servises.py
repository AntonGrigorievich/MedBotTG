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