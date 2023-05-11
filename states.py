from aiogram.dispatcher.filters.state import StatesGroup, State

class SelfDiagnosis(StatesGroup):
    nose_question = State()
    headache_question = State()
    cough_question = State()
    scrappiness_question = State()
    final_state = State()