from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🐶 Мой питомец")
async def cmd_my_pet(message: Message):
    await message.answer(
        "Это твой питомец!",
        parse_mode="HTML",
    )