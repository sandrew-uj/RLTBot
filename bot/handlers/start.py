from aiogram import types

from loader import dp


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет, чтобы получить ответ из бд, просто передай json сообщением!")
