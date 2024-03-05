from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

'''USER'''
keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Поиск', callback_data='user.func.search')]])
keyboard_menubutton = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

'''ADMIN'''
