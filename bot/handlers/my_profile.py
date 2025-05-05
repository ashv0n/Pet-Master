from aiogram import Router, F
from aiogram.types import Message
from database.main import async_session
from database.models.user import User 
from database.models.pet import Pet


router = Router()

@router.message(F.text == "👤 Мой профиль")
async def cmd_my_profile(message: Message):
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, message.from_user.id)

            if not user:
                await message.answer("Пожалуйста, для начала напишите /start.")
                return

            pet = None
            if user.user_pet_id:
                pet = await session.get(Pet, user.user_pet_id)

            from .actions import pets
            pet_type_correct = "NULL"
            if pet:
                for pet_l, code in pets:
                    if code == pet.pet_type:
                        pet_type_correct = pet_l
                        break

            text = (
                f"👤 <b>Профиль пользователя {user.user_name}</b>\n\n"
                f"💬 ID: <code>{user.user_id}</code>\n"
                f"👤 Никнейм: <code>{user.user_name}</code>\n"
            )

            if pet:
                text += (
                    f"\n🐶 Имя питомца: <code>{pet.pet_name}</code>\n"
                    f"<b>{pet_type_correct}</b>\n"
                )

            text += (
                f"\n💼 Статус: <b>{'Администратор' if user.is_admin else 'Пользователь'}</b>"
            )

            await message.answer(text, parse_mode="HTML")
