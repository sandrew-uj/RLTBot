import json

from aiogram import types

from loader import dp
from utils.solution import aggregate_values


@dp.message_handler()
async def get_json(message: types.Message):
    user_text = message.text
    try:
        json_obj = json.loads(user_text)
        res = aggregate_values(
            dt_from_iso=json_obj["dt_from"],
            dt_upto_iso=json_obj["dt_upto"],
            group_type=json_obj["group_type"]
        )
        await message.answer(json.dumps(res))
    except Exception:
        await message.answer("Получен некорректный json!")
