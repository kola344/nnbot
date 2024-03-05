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
import branches as branchTools
import copy

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

admin_editor_data = {}
class admin_editor():
    def __init__(self, district):
        self.district = district

class adminDisctict(StatesGroup):
    district = State()
    edu = State()
    public_place = State()
    street = State()

branches_data = {}
class branches:
    def __init__(self, tree):
        self.tree = tree
        self.branch = []

class branchState(StatesGroup):
    tree_create = State()
    branch = State()
    branch_create = State()

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
                await message.answer(replic_menu, reply_markup=keyboard_menu)

@dp.message(F.text == '/admin')
async def admin(message: Message, state: FSMContext):
    if not message.chat.id in config.admins:
        await message.answer(replic_notrights)
    else:
        if message.chat.type == 'private':
            await state.clear()
            text, markup = replic_admin_districts()
            await message.answer(text, reply_markup=markup)

@dp.message(branchState.branch_create, F.text)
async def branch_createFunc(message: Message, state: FSMContext):
    branch_session = branches_data[message.chat.id]
    tree = branchTools.Tree(branch_session.tree)
    tree.create_branch(copy.deepcopy(branch_session.branch), message.text)
    branch_session.branch.append(message.text)
    text, markup = replic_branch_informator(branch_session.tree, branch_session.branch)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@dp.message(branchState.tree_create, F.text)
async def tree_createFunc(message: Message, state: FSMContext):
    branchTools.Tree(message.text)
    text, markup = replic_inventory_editor_menu()
    await message.answer(text, reply_markup=markup)
    await state.clear()

@dp.message(adminDisctict.edu, F.text)
async def admin_eduaddFunc(message: Message, state: FSMContext):
    adm_session = admin_editor_data[message.chat.id]
    place = db.places()
    place.add_education(message.text, adm_session.district)
    text, markup = replic_admin_educations(adm_session.district)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@dp.message(adminDisctict.public_place, F.text)
async def admin_publicplaceaddFunc(message: Message, state: FSMContext):
    adm_session = admin_editor_data[message.chat.id]
    place = db.places()
    place.add_public_place(message.text, adm_session.district)
    text, markup = replic_admin_publicplaces(adm_session.district)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@dp.message(adminDisctict.street, F.text)
async def admin_publicplaceaddFunc(message: Message, state: FSMContext):
    adm_session = admin_editor_data[message.chat.id]
    place = db.places()
    place.add_street(message.text, adm_session.district)
    text, markup = replic_admin_streets(adm_session.district)
    await message.answer(text, reply_markup=markup)
    await state.clear()

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
        if message.text == 'Меню':
            await message.answer(replic_menu, reply_markup=keyboard_menu)


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
            if func == 'e':
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
    if dir == 'user':
        if func == 'func':
            if value == 'search':
                text, markup = replic_search()
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
    elif dir == 'u':
        if func == 't':
            branch = branches(value)
            branches_data[user_id] = branch
            text, markup = replic_informator(value, branch.branch)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'i':
            branch_session = branches_data[user_id]
            branch_session.branch.append(value)
            text, markup = replic_informator(branch_session.tree, branch_session.branch)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'back':
            branch_session = branches_data[user_id]
            branch_session.branch = branch_session.branch[:-1]
            text, markup = replic_informator(branch_session.tree, branch_session.branch)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    if user_id in config.admins:
        if dir == 'e':
            if func == 'd':
                editor_session = admin_editor_data[user_id]
                if value == 'edu':
                    text, markup = replic_admin_educations(editor_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
                elif value == 'public':
                    text, markup = replic_admin_publicplaces(editor_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
                elif value == 'streets':
                    text, markup = replic_admin_streets(editor_session.district)
                    await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            else:
                admin_editor_data[user_id] = admin_editor(value)
                await bot.edit_message_text(replic_admindisctrict, user_id, call.message.message_id, reply_markup=keyboard_admindisctrict)
        elif dir == 'del':
            editor_session = admin_editor_data[user_id]
            place = db.places()
            if func == 'edu':
                place.delete_education(value, editor_session.district)
                text, markup = replic_admin_educations(editor_session.district)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 'pub':
                place.delete_public_place(value, editor_session.district)
                text, markup = replic_admin_publicplaces(editor_session.district)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 'str':
                place.delete_street(value, editor_session.district)
                text, markup = replic_admin_streets(editor_session.district)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif dir == 'add':
            await bot.edit_message_text(replic_admin_addplace, user_id, call.message.message_id)
            if func == 'edu':
                await state.set_state(adminDisctict.edu)
            elif func == 'public':
                await state.set_state(adminDisctict.public_place)
            elif func == 'street':
                await state.set_state(adminDisctict.street)
        elif dir == 'inventory':
            text, markup = replic_inventory_editor_menu()
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif dir == 'tree':
            if func == 'add':
                await bot.edit_message_text(replic_admin_addtree, user_id, call.message.message_id)
                await state.set_state(branchState.tree_create)
            elif func == 'e':
                branch = branches(value)
                branches_data[user_id] = branch
                text, markup = replic_branch_informator(value, branch.branch)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 'del':
                tree = branchTools.Tree(value)
                tree.del_tree()
                text, markup = replic_inventory_editor_menu()
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif dir == 'b':
            if func == 'add':
                await bot.edit_message_text(replic_admin_addbranch, user_id, call.message.message_id)
                await state.set_state(branchState.branch_create)
            elif func == 'e':
                branch_session = branches_data[user_id]
                branch_session.branch.append(value)
                text, markup = replic_branch_informator(branch_session.tree, branch_session.branch)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif func == 'back':
                branch_session = branches_data[user_id]
                branch_session.branch = branch_session.branch[:-1]
                text, markup = replic_branch_informator(branch_session.tree, branch_session.branch)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Starting bot...')
    asyncio.run(main())