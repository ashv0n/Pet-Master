from aiogram import Router, F


router = Router()

@router.message(F.text == "🐶 Мой питомец")
async def cmd_my_pet(message: Message):
    await message.answer(
        "Это твой питомец!",
        parse_mode="HTML",
    )