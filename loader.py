from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, ACCESS_ID
from middlewares import AccessMiddleware
from shikimori_api import Shikimori

session = Shikimori()
api = session.get_api()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AccessMiddleware(ACCESS_ID))
