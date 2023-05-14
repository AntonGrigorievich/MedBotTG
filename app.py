import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from database import DataBase

loop = asyncio.get_event_loop
storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=storage)
db = DataBase()

if __name__ == '__main__':
    from handlers import dp, admin_startup
    executor.start_polling(dp, on_startup=admin_startup)