from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Меню
m_btn = InlineKeyboardButton('Меню', callback_data='Ё')
search_btn = InlineKeyboardButton('Поиск', callback_data='search')
fav_btn = InlineKeyboardButton(text='Закладки', callback_data='fav')
menu = InlineKeyboardMarkup().add(m_btn).add(search_btn).insert(fav_btn)

#кнопки для закладок
add_fav_btn = InlineKeyboardButton(
    'Добавить в закладки 📝', callback_data='add_fav')
fav_back_btn = InlineKeyboardButton(
    text='【К закладкам】', callback_data='back_fav')
del_fav_btn = InlineKeyboardButton(
    text='Удалить из закладок 🗑', callback_data='del_fav')
fav_back_markup = InlineKeyboardMarkup().add(del_fav_btn).add(fav_back_btn)

# Кнопки "назад"
back_list_btn = InlineKeyboardButton(
    text='【К результатам поиска】', callback_data='back_list')
back_list_markup = InlineKeyboardMarkup().add(add_fav_btn).add(back_list_btn)

back_menu_btn = InlineKeyboardButton(text='【В меню】', callback_data='menu')
back_menu_markup = InlineKeyboardMarkup().add(back_list_btn)
