from aiogram.dispatcher.filters.state import StatesGroup, State

class SelfDiagnosis(StatesGroup):
    nose_question = State()
    headache_question = State()
    cough_question = State()
    scrappiness_question = State()
    final_state = State()

class SupportQuestion(StatesGroup):
    support_question = State()
    support_question_confirm = State()

class SupportAnswer(StatesGroup):
    question_action_select = State()
    action_execute = State()
    answer_get = State()
    answer_confirm = State()

class KeywordsAnswer(StatesGroup):
    get_question = State()