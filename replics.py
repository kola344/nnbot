from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import db
import config
import keyboards
import os
import branches

'''USERS'''
replic_menu = '😄 Благодаря мне ты можешь просмотреть инвентаризацию многих заведений!\n🤔 Начнем?'

def replic_welcome():
    keyboard = []
    for district in config.districts:
        keyboard.append([KeyboardButton(text=district)])
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    text = '👋 Привет! Перед использованием бота необходимо зарегистрироваться.\nУкажи свой район'
    return text, markup

replic_nobuttonerror = ('🤔 Ошибка! Пожалуйста, нажимай только на кнопки.')
replic_invalidsession = ('😕 Недействительная сессия')
replic_nodata = ('🤔 Не указано ни одного конкретного места')

def replic_regother(district, edu, public, street):
    if edu == None:
        btn1 = InlineKeyboardButton(text='Учебные учреждения', callback_data=f'list.all.educations')
    else:
        btn1 = InlineKeyboardButton(text=edu, callback_data=f'list.all.educations')
    if public == None:
        btn2 = InlineKeyboardButton(text='Общественные места', callback_data=f'list.all.publics')
    else:
        btn2 = InlineKeyboardButton(text=public, callback_data=f'list.all.publics')
    if street == None:
        btn3 = InlineKeyboardButton(text='Улицы', callback_data=f'list.all.streets')
    else:
        btn3 = InlineKeyboardButton(text=street, callback_data=f'list.all.streets')
    btn4 = InlineKeyboardButton(text='✔️ Применить', callback_data=f'reg..end')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4]])
    text = f'😊 Отлично! Выбран район {district}.\nТеперь укажи конкретные места в твоем районе, выбирая их по кнопкам ниже'
    return text, markup

def replic_regedu(disctrict):
    place = db.places()
    educations = place.get_educations(disctrict)
    keyboard = []
    for education in educations:
        keyboard.append([InlineKeyboardButton(text=education, callback_data=f'e.e.{education}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'menu..')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'📋 Список учебных учреждений района {disctrict}'
    return text, markup

def replic_regpublics(disctrict):
    place = db.places()
    publics = place.get_public_places(disctrict)
    keyboard = []
    for public in publics:
        keyboard.append([InlineKeyboardButton(text=public, callback_data=f'e.p.{public}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'menu..')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'📋 Список общественных мест района {disctrict}'
    return text, markup

def replic_regstreets(disctrict):
    place = db.places()
    streets = place.get_streets(disctrict)
    keyboard = []
    for street in streets:
        keyboard.append([InlineKeyboardButton(text=street, callback_data=f'e.s.{street}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'menu..')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'📋 Список улиц района {disctrict}'
    return text, markup

def replic_profile(user_id):
    user = db.users_db()
    user_data = user.get_userdata(user_id)
    first_name, last_name, username = user_data['first_name'], user_data['last_name'], user_data['username']
    district = user_data['district']
    education, public_place, street = user_data['education'], user_data['public_place'], user_data['street']
    text = f'👤 Профиль\n{first_name}\n{last_name} (@{username})\nРайон: {district}\nУчебное учреждение: {education}\nОбщественное место: {public_place}\nУлица: {street}'
    return text, keyboards.keyboard_menubutton

def replic_search():
    tries = branches.get_tries()
    keyboard = []
    for i in tries:
        keyboard.append([InlineKeyboardButton(text=i, callback_data=f'u.t.{i}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = '😄 Выбери место'
    return text, markup

def replic_informator(tree, branch):
    items = branches.Tree(tree).informator(branch)
    keyboard = []
    for item in items:
        keyboard.append([InlineKeyboardButton(text=item, callback_data=f'u.i.{item}')])
    if branch == []:
        text = tree
    else:
        keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'u.back.')])
        text = branch[-1]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return text, markup


'''ADMIN'''
replic_notrights = '😕 Недостаточно прав'
replic_admindisctrict= 'Редактирование района'
replic_admin_addplace = 'Введи название места'
replic_admin_addtree = 'Введи название дерева'
replic_admin_addbranch = 'Введи название ветки'

def replic_admin_districts():
    keyboard = []
    for district in config.districts:
        keyboard.append([InlineKeyboardButton(text=district, callback_data=f'e..{district}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Выбери район для редактирования'
    return text, markup

def replic_admin_educations(disctrict):
    database = db.places()
    educations = database.get_educations(disctrict)
    keyboard = []
    for education in educations:
        keyboard.append([InlineKeyboardButton(text=education, callback_data=f'del.edu.{education}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'add.edu.{disctrict}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'e..{disctrict}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'Образовательные учреждения района {disctrict}. Для удаления места нажми на него'
    return text, markup

def replic_admin_publicplaces(district):
    database = db.places()
    places = database.get_public_places(district)
    keyboard = []
    for place in places:
        keyboard.append([InlineKeyboardButton(text=place, callback_data=f'del.pub.{place}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'add.public.{district}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'e..{district}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'Общественные места района {district}. Для удаления места нажми на него'
    return text, markup

def replic_admin_streets(district):
    database = db.places()
    streets = database.get_streets(district)
    keyboard = []
    for street in streets:
        keyboard.append([InlineKeyboardButton(text=street, callback_data=f'del.str.{street}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'add.street.{district}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'e..{district}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'Улицы района {district}. Для удаления места нажми на него'
    return text, markup

def replic_inventory_editor_menu():
    items = branches.get_tries()
    keyboard = []
    for item in items:
        keyboard.append([InlineKeyboardButton(text=item, callback_data=f'tree.e.{item}')])
    keyboard.append([InlineKeyboardButton(text='➕ Создать', callback_data=f'tree.add.')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Деревья'
    return text, markup

def replic_branch_informator(tree, branch):
    items = branches.Tree(tree).informator(branch)
    keyboard = []
    for item in items:
        keyboard.append([InlineKeyboardButton(text=item, callback_data=f'b.e.{item}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'b.add.')])
    if branch == []:
        keyboard.append([InlineKeyboardButton(text='❌ Удалить дерево', callback_data=f'tree.del.{tree}')])
        text = tree
    else:
        keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'b.back.')])
        text = branch[-1]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return text, markup




