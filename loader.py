from aiogram import Bot, Dispatcher, types
from config import TOKEN
from db import SQLRequests

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = SQLRequests('yawns_user.db')
