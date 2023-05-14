import sqlite3
import logging

class DataBase:
    logging.basicConfig(level=logging.INFO, filemode='db_log.log')

    def __init__(self):
        self.db = sqlite3.connect('database.db')
        self.cur = self.db.cursor()
        
        # при инициализации бд создаем нужные таблицы
        self.create_table(
            'questions',
            id='INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
            user_id='INTEGER',
            question_text='TEXT',
            )

        self.create_table(
            'doctors',
            id='INTEGER NOT NULL PRIMARY KEY',
            name='TEXT',
            speciality_id='INTEGER REFERENCES specialities(id)', # тут будет FOREIGN KEY
            address='TEXT',
            image='TEXT',
            )

    def create_table(self, table_name, **kwargs):
        # для использования метода передаем в качестве аргумента
        # название таблицы и ее столбцы в формате ключевых аргументов
        try:
            rows = ', '.join([' '.join([kw, kwargs[kw]]) for kw in kwargs])
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({rows})")
            logging.info(f'Таблица {table_name} создана или существует')
            return
        except Exception as ex:
            logging.error(f"Не удалось создать таблицу {table_name}\nОшибка: {type(ex)} |{ex}|")
            return

    def delete_table(self, table_name):
        try:
            self.cur.execute(f'DROP TABLE IF EXISTS {table_name}')
        except Exception as ex:
            logging.error(f"""Не удалось удалить таблицу {table_name}, возможно она не существует\n
            {type(ex)} |{ex}|""")
            return 

    def add_question(self, user_id, question):
        try:
            self.cur.execute(f"INSERT INTO questions (user_id, question_text) VALUES ({user_id}, '{question}')")
            logging.info(f"""Вопрос {question} от пользователя {user_id} добавлен в базу данных""")
            self.db.commit()
        except Exception as ex:
            logging.error(f"""Не удалось добавить вопрос в базу данных.\n{type(ex)} |{ex}|""")
            return

    def get_questions(self):
        try:
            self.cur.execute("SELECT user_id, question_text FROM questions")
            questions = self.cur.fetchall()
            return questions
        except Exception as ex:
            logging.error(f'Не удалось получить вопросы. Возможно их нет\n{type(ex)} |{ex}|')
            return False

db = DataBase()
print(db.get_questions())