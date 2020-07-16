from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, api
import keyboards as kb
from states import *
from telegram import ParseMode


#начало поиска
@dp.callback_query_handler(state=Anime.waiting_for_command, text='search')
async def search_start(call: CallbackQuery, state: FSMContext):
    await Anime.waiting_for_search.set()
    await call.message.answer(
        text='_Введите название:_', parse_mode=ParseMode.MARKDOWN)


#вывод результтатов поиска в список
@dp.message_handler(
    state=Anime.waiting_for_search, content_types=types.ContentTypes.TEXT)
async def search_process(message: types.Message, state: FSMContext):
    ani = message.text
    search_result = {}
    dicts = api.animes.GET(search=ani, limit=10)
    if len(dicts) == 0:
        await message.answer(
            "_Ничего не смогла найти...\n"
            "Попробуй ввести название аниме попроще,либо на другом языке._",
            parse_mode=ParseMode.MARKDOWN)
        return

    for dict in dicts:
        search_result[dict['id']] = dict['name'], dict['russian'], dict['id']

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for ids in search_result.values():
        keyboard.add(InlineKeyboardButton(text=ids[0], callback_data=ids[2]))

    await message.answer(
        "_Вот, что я нашла..._",
        reply_markup=keyboard.add(kb.back_menu_btn),
        parse_mode=ParseMode.MARKDOWN)
    await state.update_data(keysave=keyboard)
    await Anime.waiting_for_result.set()


#список найденных --> меню
@dp.callback_query_handler(text='menu', state=Anime.waiting_for_result)
async def cmd_menu(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        '_Хм..._', reply_markup=kb.menu, parse_mode=ParseMode.MARKDOWN)
    await Anime.waiting_for_command.set()


#описание аниме --> список найденных
@dp.callback_query_handler(state=Anime.waiting_for_result, text='back_list')
async def search_end(call: CallbackQuery, state: FSMContext):
    list_of_search = await state.get_data()
    await call.message.answer(
        '_Давай посмотрим еще какое-нибудь..._',
        reply_markup=list_of_search['keysave'],
        parse_mode=ParseMode.MARKDOWN)
    await Anime.waiting_for_result.set()


#вывод информации о выбранном аниме
@dp.callback_query_handler(state=Anime.waiting_for_result)
async def search_end(call: CallbackQuery, state: FSMContext):
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
        reply_markup=kb.back_list_markup,
        parse_mode=ParseMode.MARKDOWN)
