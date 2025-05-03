from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text="🐣 Завести питомца")
            ],

            [
            KeyboardButton(text="📬 Написать в поддержку"),
            KeyboardButton(text="📖 Информация"),
            KeyboardButton(text="👤 Профиль")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer(
        "Привет! Это проект Pet-Master. Тут ты можешь завести себе питомца и заботиться о нем.\n"
        "Питомец будет расти и развиваться, а ты сможешь его кормить, гулять с ним и играть." \
        "\n"
        "Помни о своем питомце ежедневно, иначе он просто убежит от тебя...\n",
        parse_mode="HTML",
        reply_markup=kb,
    )