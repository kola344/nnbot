# bot
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import config
import db
from replics import *
from keyboards import *
from aiogram import types
from aiogram.types import ReplyKeyboardRemove as kbremove

admins = [1659397548]

# TOKEN
bot = Bot(token=config.token)
dp = Dispatcher()

registration_data = {}
class registration:
    def __init__(self):
        self.district = None
        self.education = None
        self.public_place = None
        self.street = None

class regForm(StatesGroup):
    district = State()
    other = State()


# Начало
@dp.message(F.text.startswith('/start'))
async def start(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == '/start':
            database = db.users_db()
            if not database.check_user(user_id=message.chat.id):
                text, markup = replic_welcome()
                await message.answer(text, reply_markup=markup)
                await state.set_state(regForm.district)
            else:
                pass

@dp.message(regForm.district, F.text)
async def registration_disctictFunc(message: types.Message, state: FSMContext):
    reg_session = registration()
    registration_data[message.chat.id] = reg_session
    if message.text not in config.districts:
        await message.answer(replic_nobuttonerror)
    else:
        text, markup = replic_regother(message.text, None, None, None)
        await message.answer(text, reply_markup=markup)
        reg_session.district = message.text
        await state.set_state(regForm.other)

# messages
@dp.message(F.text)
async def reply(message: Message, state: FSMContext):
    user_id = message.chat.id
    if message.chat.type == 'private':
        pass


# callback
@dp.callback_query(regForm.other, F.data)
async def reg_callback(call, state: FSMContext):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    dir = calls[0]
    func = calls[1]
    value = calls[2]
    if user_id in registration_data:
        reg_session = registration_data[user_id]
        if dir == 'menu':
            text, markup = replic_regother(reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif dir == 'list':
            if func == 'all':
                if value == 'educations':
                    text, markup = replic_regedu(reg_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
                elif value == 'publics':
                    text, markup = replic_regpublics(reg_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
                elif value == 'streets':
                    text, markup = replic_regstreets(reg_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif dir == 'reg':
            if value == 'end':
                if reg_session.education == None and reg_session.street == None and reg_session.public_place == None:
                    await bot.edit_message_text(replic_nodata, user_id, call.message.message_id)
                    await asyncio.sleep(3)
                    text, markup = replic_regother(reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
                else:
                    database = db.users_db()
                    database.add_user(user_id, call.from_user.first_name, call.from_user.last_name, call.from_user.username, 'Нижний Новгород', reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
                    await bot.delete_message(user_id, call.message.message_id)
                    text, markup = replic_profile(user_id)
                    await bot.send_message(user_id, text, reply_markup=markup)
                    await state.clear()
        elif dir == 'e':
            if func == 's':
                reg_session.education = value
                text, markup = replic_regother(reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 'p':
                reg_session.public_place = value
                text, markup = replic_regother(reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 's':
                reg_session.street = value
                text, markup = replic_regother(reg_session.district, reg_session.education, reg_session.public_place, reg_session.street)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
    else:
        await bot.edit_message_text(replic_invalidsession, user_id, call.message.message_id)
        await state.clear()


@dp.callback_query(F.data)
async def callback(call, state: FSMContext):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    dir = calls[0]
    func = calls[1]
    value = calls[2]
    pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Starting bot...')
    asyncio.run(main())