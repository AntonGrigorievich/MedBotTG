import asyncio
from aiogram import Bot, Dispatcher, executor

from config import TOKEN

loop = asyncio.get_event_loop
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handlers import dp, admin_startup
    executor.start_polling(dp, on_startup=admin_startup)