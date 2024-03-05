from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import db
import config
import keyboards

'''USERS'''

def replic_welcome():
    keyboard = []
    for district in config.districts:
        keyboard.append([KeyboardButton(text=district)])
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
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
        keyboard.append([InlineKeyboardButton(text=education, callback_data=f'e.s.{education}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'menu..')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'📋 Список учебных учреждений района {disctrict}'
    return text, markup

def replic_regpublics(disctrict):
    place = db.places()
    publics = place.get_public_places(disctrict)
    keyboard = []
    for public in publics:
        keyboard.append([InlineKeyboardButton(text=public, callback_data=f'p.s.{public}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'menu..')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'📋 Список общественных мест района {disctrict}'
    return text, markup

def replic_regstreets(disctrict):
    place = db.places()
    streets = place.get_street(disctrict)
    keyboard = []
    for street in streets:
        keyboard.append([InlineKeyboardButton(text=street, callback_data=f's.s.{street}')])
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


'''ADMIN'''
def admin_menu():
    bases = db.get_bases()
    keyboard = []
    for base in bases:
        keyboard.append([InlineKeyboardButton(text=base, callback_data=f'info.{base}.main')])

def informator(base, branch):
    pass
