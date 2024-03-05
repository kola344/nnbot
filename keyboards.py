from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

'''USER'''
keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔍 Поиск', callback_data='user.func.search')]])
keyboard_menubutton = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

'''ADMIN'''
keyboard_admindisctrict = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Учебные учреждения', callback_data='e.d.edu')], [InlineKeyboardButton(text='Общественные места', callback_data='e.d.public')], [InlineKeyboardButton(text='Улицы', callback_data='e.d.streets')], [InlineKeyboardButton(text='Инвентаризация', callback_data='inventory..')]])

