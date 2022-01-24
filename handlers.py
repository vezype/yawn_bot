from loader import dp
from aiogram import types
from loader import db
import time


@dp.message_handler(commands=['reg'], chat_type=types.ChatType.GROUP)
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await message.reply(f'Докладываю голосом Америки, поставил тебя на учёт по зевкам.')
        db.add_user(message.from_user.id)
    else:
        await message.reply(f'Кажется у тебя из головы вылетел тот факт, что ты  уже стоишь на учёте.\n\n'
                            f'*/stats* - посмотреть историю зевков.', parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(content_types=types.ContentTypes.STICKER, chat_type=types.ChatType.GROUP)
async def get_sticker(message: types.Message):
    if db.user_exists(message.from_user.id) and message.sticker.emoji == '😮':
        date = time.strftime('%d.%m.%y | %H:%M:%S')
        await message.reply(f'Записал!\n\n'
                            f'*Дата и время: {date}.*', parse_mode=types.ParseMode.MARKDOWN)
        db.new_date(message.from_user.id, date)


@dp.message_handler(commands=['stats'], chat_type=types.ChatType.GROUP)
async def stats(message: types.Message):
    if db.user_exists(message.from_user.id):
        dates = db.get_dates(message.from_user.id)

        await message.reply(f'Общее количество зевков: *{len(dates)}*.', parse_mode=types.ParseMode.MARKDOWN)

        yawns_stats = {}
        for date in dates:
            x, y = date.split(' | ')
            if x not in yawns_stats.keys():
                yawns_stats[x] = [y]
            else:
                yawns_stats[x].append(y)
        for x, y in yawns_stats.items():
            text = f'*{x}*:\n\n'
            for z in y:
                text += f'{z}\n'
            text += f'\nКоличество зевков за этот день: *{len(y)}*.'

            try:
                await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)
            except:
                await message.answer(f'\nКоличество зевков за *{x}*: *{y}*.', parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def echo(message: types.Message):
    await message.answer('Работаю только в чатах. Добавьте меня в группу и я начну вести учёт Ваших зевков.\n\n'
                         'Не забудьте написать */reg* в чате.', parse_mode=types.ParseMode.MARKDOWN)
