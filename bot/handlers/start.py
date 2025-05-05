from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from database.main import async_session
from database.models.user import User

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text="🐶 Мой питомец"),
            ],
            [
            KeyboardButton(text="📬 Написать в поддержку"),
            KeyboardButton(text="📖 Информация"),
            KeyboardButton(text="👤 Профиль"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    user_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                new_user = User(
                    user_id=user_id,
                    user_name=username,

                    user_pet_id=None,

                    is_admin=False,
                    is_banned=False,
                )
                session.add(new_user)
                await session.commit()

    await message.answer(
        "Привет! Это проект Pet-Master. Тут ты можешь завести себе питомца и заботиться о нем.\n"
        "Питомец будет расти и развиваться, а ты сможешь его кормить, гулять с ним и играть." \
        "\n"
        "Помни о своем питомце ежедневно, иначе он просто убежит от тебя...\n"
        "Чтобы начать, нажми на кнопку <b>🐶 Мой питомец.</b>\n\n",
        parse_mode="HTML",
        reply_markup=kb,
    )