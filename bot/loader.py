from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
