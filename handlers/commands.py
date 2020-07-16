from telegram import ParseMode
import keyboards as kb
from aiogram import types
from loader import dp
from states import *

@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message):
      await message.answer(f'Привет, {message.from_user.full_name} 💖\nМеня зовут _Томиэ Каваками_. Я твой личный шикимори-бот\nЕсли хочешь узнать больше обо мне, то -*/help*', parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['help'], state="*")
async def cmd_help(message: types.Message):
      await message.answer('*Я могу:*\n'
                           '~ найти аниме по названию на русском или английском языке, либо на [ромадзи по системе Хепбёрна](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%A5%D1%8D%D0%BF%D0%B1%D1%91%D1%80%D0%BD%D0%B0)  \n'
                           '~ вывести список аним, которые ты добавил в закладки\n'
                           'Для начала работы со мной достаточно вызвать меню- */menu*', parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@dp.message_handler(commands=['menu'], state="*")
async def cmd_menu(message: types.Message):
      await message.answer('_Что хотим сделать?_', reply_markup=kb.menu, parse_mode=ParseMode.MARKDOWN)
      await Anime.waiting_for_command.set()

@dp.message_handler(regexp = '/', state="*")
async def cmd_help(message: types.Message):
      if message.text[0] == '/':
            await message.answer('_Ой, такой команды я не знаю..._', parse_mode=ParseMode.MARKDOWN)
