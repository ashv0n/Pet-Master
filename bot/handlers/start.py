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
            KeyboardButton(text="👤 Мой профиль"),
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
        "<b>Привет! Добро пожаловать в Pet-Master 🐾</b>\n\n"
        "Здесь ты можешь завести собственного виртуального питомца. \nЗаботься о нем, играй, корми и выводи на прогулки!\n\n"
        "Чем больше внимания ты ему уделяешь,\nтем счастливее и быстрее он растёт 💖\n\n"
        "Но будь осторожен... если забыть о питомце надолго, он может сбежать 😿\n\n"
        "Чтобы начать приключение, нажми кнопку <b>🐶 Мой питомец</b> ниже!",
        parse_mode="HTML",
        reply_markup=kb,
    )
