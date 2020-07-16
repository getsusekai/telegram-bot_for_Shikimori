from handlers import dp
from aiogram import executor


class User:
    def __init__(self, name_ani, id_ani):
        self.name_ani = name_ani
        self.id_ani = id_ani


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
