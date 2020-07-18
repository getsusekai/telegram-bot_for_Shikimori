from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, api
import keyboards as kb
from states import *
from telegram import ParseMode


#добавить в закладки
@dp.callback_query_handler(text='add_fav', state=Anime.waiting_for_result)
async def fav_add(call: CallbackQuery, state: FSMContext):
    anisaved = await state.get_data()
    line_ani = str(anisaved['anisaveid']['name']) + ' ' + str(
        anisaved['anisaveid']['id']) + '\n'
    with open('fav.txt', 'r+', encoding='utf-8') as f:
        if line_ani in f.readlines():
            await call.answer('Уже в закладках')
            f.close()
        else:
            f.write(line_ani)
            await call.answer('Добавлено')
            f.close()


#вывести список закладок
@dp.callback_query_handler(text='fav', state=Anime.waiting_for_command)
async def fav_list(call: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    with open('fav.txt', 'r', encoding='utf-8') as f:
        for line_ani in f.readlines():
            keyboard.add(
                InlineKeyboardButton(
                    text=line_ani[:line_ani.rfind(' ')],
                    callback_data=line_ani[line_ani.rfind(' ') + 1:]))
    await call.message.answer(
        "_Что тут у нас..._",
        reply_markup=keyboard.add(kb.back_menu_btn),
        parse_mode=ParseMode.MARKDOWN)
    await state.update_data(keysave=keyboard)
    await Anime.waiting_for_fav.set()


#избранное --> меню
@dp.callback_query_handler(text='menu', state=Anime.waiting_for_fav)
async def cmd_menu(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        '_Хм..._', reply_markup=kb.menu, parse_mode=ParseMode.MARKDOWN)
    await Anime.waiting_for_command.set()


#описание аниме --> список закладок
@dp.callback_query_handler(state=Anime.waiting_for_fav, text='back_fav')
async def search_end(call: CallbackQuery, state: FSMContext):
    list_of_fav = await state.get_data()
    await call.message.answer(
        '_Давай посмотрим еще какое-нибудь..._',
        reply_markup=list_of_fav['keysave'],
        parse_mode=ParseMode.MARKDOWN)
    Anime.waiting_for_fav.set()


#удалить аниме из закладок
@dp.callback_query_handler(state=Anime.waiting_for_fav, text='del_fav')
async def search_end(call: CallbackQuery, state: FSMContext):
    anisaved = await state.get_data()
    line_ani = str(
        str(anisaved['anisaveid']['name']) + ' ' +
        str(anisaved['anisaveid']['id']) + '\n')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    with open('fav.txt', 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        if line_ani in lines:
            lines.remove(line_ani)
    f.close()
    await call.answer('Аниме удалено из закладок')
    f = open('fav.txt', 'w', encoding='utf-8')
    for i in lines:
        i = i.replace('\n', '')
        keyboard.add(
            InlineKeyboardButton(
                text=i[:i.rfind(' ')],
                callback_data=str(i[i.rfind(' ') + 1:]) + '\n'))
        f.write(i + '\n')
    await call.message.answer(
        "_Что тут у нас..._",
        reply_markup=keyboard.add(kb.back_menu_btn),
        parse_mode=ParseMode.MARKDOWN)


#вывести информацию об аниме
@dp.callback_query_handler(state=Anime.waiting_for_fav)
async def fav_end(call: CallbackQuery, state: FSMContext):
    ids_anime = call.data
    ani = api.animes(ids_anime).GET()
    await state.update_data(anisaveid=ani)
    await call.message.answer_photo(
        photo='http://shikimori.one{}'.format(ani['image']['original']))
    status = {
        'released': 'вышедшее',
        'latest': 'недавно вышедшее',
        'ongoing': 'сейчас выходит',
        'anons': 'анонсировано'
    }
    genres = ''
    for genre in ani['genres']:
        genres += genre['name'] + ' ,'
    for a in ani:
        if ani[a] == None or ani[a] == "0.0":
            ani[a] = '-'
    await call.message.answer(
        text='_Название:_ {} ({})\n'
        '_Тип:_ {}\n'
        '_Статус:_ {}\n'
        '_Жанр:_ {}\n'
        '_Оценка:_ {}\n'
        '_Количество эпизодов:_ {}\n'
        '_Дата выхода:_ {}\n'
        '_Открыть на сайте:_ shikimori.one{}\n'
        '_Описание:_ {}'.format(
            ani['russian'], ani['name'], ani['kind'], status[ani['status']],
            genres.rstrip(','), ani['score'], ani['episodes'], ani['aired_on'],
            ani['url'], ani['description']),
        reply_markup=kb.fav_back_markup,
        parse_mode=ParseMode.MARKDOWN)