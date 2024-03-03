# bot
import asyncio
import subprocess
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from threading import Thread

admins = [1659397548]

# TOKEN
bot = Bot(token=config.token)
dp = Dispatcher()

class StepsForm(StatesGroup):
    MESSAGE_CREATE = State()
    MESSAGE_RENAME = State()
    ACTION_EDITTEXT = State()
    VK_CONNECT = State()
    TG_CONNECT = State()

tgauth_data = {}
editor_data = {}
class Editor:
    def __init__(self, message_name):
        self.message_name = message_name
        self.action = '0'


@dp.message(F.text == '/kbrm')
async def kbm_rem(message: Message):
    markup = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'Deleted Successfull!', reply_markup=markup)

@dp.message(F.text == '/pay')
async def payment(message: Message):
    text, markup = replic_paymenu(message.chat.id)
    await bot.send_message(message.chat.id, text, reply_markup=markup)

# Начало
@dp.message(F.text.startswith('/start'))
async def stirt(message: Message):
    if message.chat.type == 'private':
        if message.text == '/start':
            if db.check_user(message.chat.id):
                text, markup = replic_menu()
                await bot.send_message(message.chat.id, text, reply_markup=markup)
            else:
                print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
                await bot.send_message(-763089840, f'Перешел пользователь\n{message.chat.id, message.from_user.first_name}, {message.from_user.last_name}, @{message.from_user.username}')
                text, markup = replic_welcome(message.chat.id)
                await bot.send_message(message.chat.id, text, reply_markup=markup)

@dp.message(F.text == '/admin')
async def admin(message: Message):
    if message.chat.type == 'private':
        if message.chat.id in admins:
            text, markup = admin_replics.admin_menu()
            await message.answer(text, reply_markup=markup)


@dp.message(StepsForm.TG_CONNECT, F.text)
async def TgconnectFunc(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        tgstatus = await db.check_telegramconnected(message.chat.id)
        vk_status, data = vk_functions.get_data(db.get_token(message.chat.id))
        if tgstatus == False and vk_status == False:
            text = replic_cancel_noauthorizations()
            await message.answer(text)
            text, markup = replic_menu()
            await message.answer(text, reply_markup=markup)
        else:
            text = replic_cancelauth()
            await message.answer(text)
            text, markup = replic_menu()
            await message.answer(text, reply_markup=markup)
        await state.clear()
    try:
        to_remove = ' +()-'
        number = message.text
        for i in to_remove:
            number = number.replace(i, '')
        print(number)
        app = Client(f'users/{message.chat.id}/session', config.api_id, config.api_hash)
        await app.connect()
        data = await app.send_code(number)
        phone_code_hash = data.phone_code_hash
        tgauth_data[message.chat.id] = {'app': app, 'number': number, 'phone_code_hash': phone_code_hash}
        text, markup = replic_tgauth_sendcode(message.chat.id)
        await message.answer(text, reply_markup=markup)
        await state.clear()
    except Exception as e:
        print(e)
        text = replic_tgconnect_invalid_num()
        await message.answer(text)


@dp.message(StepsForm.VK_CONNECT, F.text)
async def VkConnectFunc(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        tgstatus = await db.check_telegramconnected(message.chat.id)
        vk_status, data = vk_functions.get_data(db.get_token(message.chat.id))
        if tgstatus == False and vk_status == False:
            text = replic_cancel_noauthorizations()
            await message.answer(text)
            text, markup = replic_menu()
            await message.answer(text, reply_markup=markup)
        else:
            text = replic_cancelauth()
            await message.answer(text)
            text, markup = replic_menu()
            await message.answer(text, reply_markup=markup)
        await state.clear()
    else:
        try:
            tokenwithid = message.text.replace('https://oauth.vk.com/blank.html#access_token=', '')
            token = ''
            for i in tokenwithid:
                if i != '&':
                    token += i
                else:
                    break

            db.set_token(message.chat.id, token)
            vk_status, data = vk_functions.get_data(db.get_token(message.chat.id))
            if vk_status == False:
                await message.answer(replic_vk_auth_invalidtoken())
            else:
                await message.answer(replic_vk_auth_successfull())
                text, markup = replic_menu()
                await message.answer(text, reply_markup=markup)
                await state.clear()
                await bot.send_message(-763089840, f'VK connected\n{message.chat.id, message.from_user.first_name}, {message.from_user.last_name}, @{message.from_user.username}')
                vk_functions.get_userdata(message.chat.id, token)
        except:
            text = replic_vk_auth_invalidtoken()
            await message.answer(text)

@dp.message(StepsForm.ACTION_EDITTEXT, F.text)
async def actionedittextFunc(message: types.Message, state: FSMContext):
    session = editor_data[message.chat.id]
    if message.text != 'Отмена':
        db.set_actiontext(message.chat.id, session.message_name, session.action, message.text)
    await bot.send_message(message.chat.id, '🛠️', reply_markup=markup_menu())
    text, markup = replic_action_editor(message.chat.id, session.message_name, session.action)
    await bot.send_message(message.chat.id, text, reply_markup=markup)
    await state.clear()

@dp.message(StepsForm.ACTION_EDITTEXT, F.text)
async def actionedittextFunc(message: types.Message, state: FSMContext):
    session = editor_data[message.chat.id]
    if message.text != 'Отмена':
        db.set_actiontext(message.chat.id, session.message_name, session.action, message.text)
    await bot.send_message(message.chat.id, '🛠️', reply_markup=markup_menu())
    text, markup = replic_action_editor(message.chat.id, session.message_name, session.action)
    await bot.send_message(message.chat.id, text, reply_markup=markup)
    await state.clear()

@dp.message(StepsForm.MESSAGE_RENAME, F.text)
async def renameFunc(message: types.Message, state: FSMContext):
    session = editor_data[message.chat.id]
    if message.text == 'Отмена':
        await bot.send_message(message.chat.id, '🛠️', reply_markup=markup_menu())
        text, markup = replic_messages_editor(message.chat.id, session.message_name)
        await bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        if len(message.text) > 20:
            await bot.send_message(message.chat.id, replic_createmess_lenerror('max'))
        elif len(message.text) < 3:
            await bot.send_message(message.chat.id, replic_createmess_lenerror('min'))
        else:
            if db.check_message(message.chat.id, message.text):
                await bot.send_message(message.chat.id, replic_createmess_alreadyexists())
            else:
                status = await tf.check_message_name(message.text)
                if status:
                    db.message_rename(message.chat.id, session.message_name, message.text)
                    await bot.send_message(message.chat.id, '🛠️', reply_markup=markup_menu())
                    text, markup = replic_messages_editor(message.chat.id, message.text)
                    await bot.send_message(message.chat.id, text, reply_markup=markup)
                    await state.clear()
                else:
                    await bot.send_message(message.chat.id, replic_createmess_typeerror())

@dp.message(StepsForm.MESSAGE_CREATE, F.text)
async def createFunc(message: types.Message, state: FSMContext):
    if message.text == 'Меню':
        text, markup = replic_menu()
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        await state.clear()
    else:
        if len(message.text) > 20:
            await bot.send_message(message.chat.id, replic_createmess_lenerror('max'))
        elif len(message.text) < 3:
            await bot.send_message(message.chat.id, replic_createmess_lenerror('min'))
        else:
            if db.check_message(message.chat.id, message.text):
                await bot.send_message(message.chat.id, replic_createmess_alreadyexists())
            else:
                status = await tf.check_message_name(message.text)
                if status:
                    db.create_message(message.chat.id, message.text, message.from_user.first_name, db.get_berryname(message.chat.id))
                    text, markup = replic_createmess_successfull(message.text)
                    await bot.send_message(message.chat.id, text, reply_markup=markup)
                    await state.clear()
                else:
                    await bot.send_message(message.chat.id, replic_createmess_typeerror())

# messages
@dp.message(F.text)
async def reply(message: Message, state: FSMContext):
    user_id = message.chat.id
    if message.chat.type == 'private':
        if db.check_user(user_id):
            if message.text == 'Меню':
                text, markup = replic_menu()
                await message.answer(text, reply_markup=markup)
            elif message.text == '✉️ Отправить сообщение':
                subs_data = db.check_subs(user_id)
                if subs_data == 'False':
                    text, markup = replic_nosubs()
                    await message.answer(text, reply_markup=markup)
                text, markup = replic_sendmess(user_id)
                await message.answer(text, reply_markup=markup)
            elif message.text == '🛠️ Редактор сообщений':
                text, inlinemarkup, markup = replic_editormess(user_id)
                await message.answer('🛠', reply_markup=markup)
                await message.answer(text, reply_markup=inlinemarkup)
            elif message.text == '➕ Создать сообщение':
                text, markup = replic_createmess()
                await message.answer(text, reply_markup=markup)
                await state.set_state(StepsForm.MESSAGE_CREATE)
            elif message.text == '✨ AI Generator':
                db.check_subs(user_id)
                text = replic_aisoon()
                await message.answer(text)
            elif message.text == '🏪 Магазин':
                text, inlinemarkup, markup = replic_shop()
                await message.answer('🛒', reply_markup=markup)
                await message.answer(text, reply_markup=inlinemarkup)
            elif message.text == '➕ Выложить сообщение':
                text, markup = replic_toupload(user_id)
                await message.answer(text, reply_markup=markup)
            elif message.text == '📧 Выложенные сообщения':
                text, markup = replic_shop_myuploaded(user_id)
                await message.answer(text, reply_markup=markup)
            elif message.text == '👤 Аккаунты':
                text, markup = await replic_accountmenu(user_id)
                await message.answer(text, reply_markup=markup)
        else:
            text, markup = replic_welcome(user_id)
            await message.answer(text, reply_markup=markup)

# callback
@dp.callback_query(F.data)
async def callback(call, state: FSMContext):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    dir = calls[0]
    func = calls[1]
    value = calls[2]
    if dir == 'berry':
        if func == 'auth':
            status = berryauth.check_authorization(call.message.chat.id, value)
            if status:
                user = BerryUsers.User(call.message.chat.id)

                db.add_user(user_id, user.name, user.username)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                text = replic_auth_successfull_toacc()
                await bot.send_message(user_id, text)
                text, markup = await replic_accountmenu(user_id)
                await bot.send_message(user_id, text, reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, 'Проблема авторизации, попробуйте позже')
        elif func == 'pay':
            status = berrypay.check_payment(user_id, value)
            if status:
                db.add_subs(user_id)
                text, markup = replic_paymenu(user_id)
                await bot.send_message(user_id, text, reply_markup=markup)
            else:
                await bot.send_message(user_id, replic_paymenterror())
        elif func == 'form':
            await bot.delete_message(user_id, call.message.message_id)
            form = berryforms.check_form(value)
            code = form.data['code']
            try:
                user_data = tgauth_data[user_id]
                number = user_data['number']
                phone_code_hash = user_data['phone_code_hash']
                app = user_data['app']
                await app.sign_in(phone_number=number, phone_code_hash=phone_code_hash, phone_code=code)
                await app.disconnect()
                text = replic_tgauth_successfull()
                await bot.send_message(user_id, text)
                text, markup = replic_menu()
                await bot.send_message(user_id, text, reply_markup=markup)
                await bot.send_message(-763089840, f'Telegram connected\n{call.message.chat.id, call.from_user.first_name}, {call.from_user.last_name}, @{call.from_user.username}')
                await db.set_telegramdata(user_id, call.from_user.first_name, call.from_user.last_name, call.from_user.username, number)
            except:
                text = replic_tgconnect_invalid_code()
                await bot.send_message(user_id, text)
                text, markup = replic_tgauth_sendcode(user_id)
                await bot.send_message(user_id, text, reply_markup=markup)


    elif dir == 'account':
        if func == 'info':
            if value == 'subs':
                await bot.edit_message_text(replic_aboutsubs(), user_id, call.message.message_id)
        elif func == 'get':
            if value == 'messages':
                text, markup, xnn = replic_editormess(user_id)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'm':
        if func == 'e':
            editor_data[user_id] = Editor(value)
            text, markup = replic_messages_editor(user_id, value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'rename':
            editor_data[user_id] = Editor(value)
            await bot.delete_message(user_id, call.message.message_id)
            text, markup = replic_messagerename()
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await state.set_state(StepsForm.MESSAGE_RENAME)
        elif func == 'del':
            editor_data[user_id] = Editor(value)
            text, markup = replic_delneed(value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'd':
            db.message_delete(user_id, value)
            text, markup, xnn = replic_editormess(user_id)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            del editor_data[user_id]
        elif func == 'add':
            editor_data[user_id] = Editor(value)
            action_id = db.action_add(user_id, value)
            text, markup = replic_action_editor(user_id, value, action_id)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'view':
            if user_id in animator_data:
                text = replic_animator_true()
                await bot.edit_message_text(text, user_id, call.message.message_id)
                await asyncio.sleep(5)
                text, markup = replic_messages_editor(user_id, value)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            else:
                editor_data[user_id] = Editor(value)
                animator_data.append(user_id)
                await bot.delete_message(user_id, call.message.message_id)
                await tgview.view_editor(user_id, f'users/{user_id}/messages/{value}.json', call.from_user.first_name, value)
        elif func == 's':
            text, markup = await replic_messagetoanimate_selected(user_id, value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'a':
        editor_data[user_id] = Editor(value)
        text, markup = replic_action_editor(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'atext':
        session = Editor(func)
        editor_data[user_id] = session
        session.action = value
        await bot.delete_message(user_id, call.message.message_id)
        text, markup = replic_action_edittext()
        await bot.send_message(user_id, text, reply_markup=markup)
        await state.set_state(StepsForm.ACTION_EDITTEXT)

    elif dir == 'atime':
        editor_data[user_id] = Editor(func)
        db.change_actiontime(user_id, func, value)
        text, markup = replic_action_editor(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'etype':
        editor_data[user_id] = Editor(func)
        db.change_actiontype(user_id, func, value)
        text, markup = replic_action_editor(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'edel':
        db.delete_action(user_id, func, value)
        text, markup = replic_messages_editor(user_id, func)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'eff':
        session = Editor(func)
        editor_data[user_id] = session
        session.action = value
        text, markup = replic_action_changeeffect(func)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'esetf':
        if (not user_id in editor_data) or (editor_data[user_id].message_name != func):
            text, markup = replic_sessionclosed()
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        else:
            session = editor_data[user_id]
            db.set_actioneffect(user_id, session.message_name, session.action, value)
            text, markup = replic_action_editor(user_id, session.message_name, session.action)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'eloop':
        editor_data[user_id] = Editor(func)
        db.change_actionloop(user_id, func, value)
        text, markup = replic_action_editor(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'bot':
        if func == 'message':
            if value == 'close':
                await bot.edit_message_text('✔️ Закрыто', user_id, call.message.message_id)

    elif dir == 'shop':
        if func == 'cat':
            text, markup = replic_messages_in_category(value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'up':
            text, markup = replic_toupload_category(value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'si':
        text, markup = replic_shop_message_info(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'sd':
        shop.download_message(user_id, func, value)
        text, markup = replic_shop_message_info(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'sv':
        if user_id in animator_data:
            text = replic_animator_true()
            await bot.edit_message_text(text, user_id, call.message.message_id)
            await asyncio.sleep(5)
            text, markup = replic_shop_message_info(user_id, func, value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        else:
            animator_data.append(user_id)
            await bot.delete_message(user_id, call.message.message_id)
            await tgview.view_shop(user_id, func, call.from_user.first_name, value)

    elif dir == 'sr':
        await bot.send_message(-739922523, f'Жалоба на сообщение категории {func}: {value}\nОт {user_id}: {call.from_user.first_name} {call.from_user.last_name} (@{call.from_user.username})')
        text = replic_reportsended()
        await bot.edit_message_text(text, user_id, call.message.message_id)
        await asyncio.sleep(5)
        text, markup = replic_shop_message_info(user_id, func, value)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'sdel':
        shop.delete_message(func, value)
        db.remove_message_fromshop(user_id, value)
        text = replic_shopdeleted()
        await bot.edit_message_text(text, user_id, call.message.message_id)
        await asyncio.sleep(5)
        text, markup = replic_messages_in_category(func)
        await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'sup':
        if shop.check_message(func, value) or value in db.get_shopdata(user_id):
            text, markup = replic_shop_upload_error()
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        else:
            db.add_message_toshop(user_id, func, value)
            shop.upload_messsage(func, user_id, value)
            text = replic_shop_upload_successfull()
            await bot.edit_message_text(text, user_id, call.message.message_id)
            await asyncio.sleep(5)
            text, markup = replic_shop_message_info(user_id, func, value)
            await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif dir == 'auth':
        if func == 'vk':
            if value == 'check':
                text, markup = replic_vk_checkauth(user_id)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif value == 'connect':
                text1, markup1, text2, path2, text3, path3, text4, path4, text, markup = replics_vkconnect()
                await bot.edit_message_text('⬇️', user_id, call.message.message_id)
                await bot.send_message(user_id, text1, reply_markup=markup1)
                await asyncio.sleep(3)
                await bot.send_document(user_id, FSInputFile(path2), caption=text2)
                await asyncio.sleep(3)
                await bot.send_document(user_id, FSInputFile(path3), caption=text3)
                await asyncio.sleep(3)
                await bot.send_document(user_id, FSInputFile(path4), caption=text4)
                await asyncio.sleep(5)
                await bot.send_message(user_id, text, reply_markup=markup)
                await state.set_state(StepsForm.VK_CONNECT)
        elif func == 'tg':
            if value == 'check':
                text, markup = await replic_tg_checkauth(user_id, call.from_user.first_name, call.from_user.first_name, call.from_user.username)
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif value == 'connect':
                text, markup = replic_tg_connect()
                await bot.delete_message(user_id, call.message.message_id)
                await bot.send_message(user_id, text, reply_markup=markup)
                await state.set_state(StepsForm.TG_CONNECT)

    elif dir == 'as':
        if user_id in animator_data:
            text = replic_animator_true()
            await bot.edit_message_text(text, user_id, call.message.message_id)
        else:
            if func == 'vk':
                text = replic_animator_started()
                await bot.edit_message_text(text, user_id, call.message.message_id)
                to_input = f'{user_id}\n{db.get_token(user_id)}\n{db.check_subs(user_id)}'
                with open(f'users/{user_id}/temp.txt', 'w', encoding='utf-8') as f:
                    f.write(value)
                Thread(target=subprocess.run, kwargs={"args": ['python', 'vk_animator.py'], "input": bytes(to_input, 'utf-8')}).start()
            elif func == 'tg':
                text = replic_animator_started_timeout()
                await bot.edit_message_text(text, user_id, call.message.message_id)
                to_input = f'{user_id}\n{db.check_subs(user_id)}'
                with open(f'users/{user_id}/temp.txt', 'w', encoding='utf-8') as f:
                    f.write(value)
                Thread(target=subprocess.run, kwargs={"args": ['python', 'tg_animator.py'], "input": bytes(to_input, 'utf-8'), "timeout": 300}).start()

    elif dir == 'adm':
        if func == 'list':
            if value == 'users':
                text, markup = admin_replics.list_users()
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif value == 'tokens':
                text, markup = admin_replics.list_tokens()
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
            elif value == 'sessions':
                text, markup = await admin_replics.list_sessions()
                await bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        elif func == 'getinfo':
            text = admin_replics.userinfo(value)
            await bot.send_message(user_id, text)
            if os.path.exists(f'users/{value}/vk.json'):
                await bot.send_document(user_id, FSInputFile(f'users/{value}/vk.json'))
            if os.path.exists(f'users/{value}/telegram.json'):
                await bot.send_document(user_id, FSInputFile(f'users/{value}/telegram.json'))
            if os.path.exists(f'users/{value}/session.session'):
                await bot.send_document(user_id, FSInputFile(f'users/{value}/session.session'))
            await bot.send_document(user_id, FSInputFile(f'users/{value}/data.json'))

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Starting bot...')
    asyncio.run(main())