from aiogram.dispatcher.filters.state import StatesGroup, State


class Anime(StatesGroup):
    waiting_for_command = State()
    waiting_for_search = State()
    waiting_for_result = State()
    waiting_for_fav = State()
