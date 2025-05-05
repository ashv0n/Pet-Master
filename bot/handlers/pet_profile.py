from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from database.main import async_session
from database.models.user import User 
from database.models.pet import Pet 
import os

router = Router()

@router.message(F.text == "🐶 Мой питомец")
async def p_profile(message: Message, user: User, pet: Pet):
        async with async_session() as session:
            async with session.begin():
                user = await session.get(User, message.from_user.id)

                if not user:
                    await message.answer("Пожалуйста, для начала напишите /start.")
                    return            

                pet = await session.get(Pet, user.user_pet_id)
                if not user:
                    return
                if not user.user_pet_id or not pet:
                    return

                from .actions import pets

                pet_type_correct = "NULL"
                for pet_l, code in pets:
                    if code == pet.pet_type:
                        pet_type_correct = pet_l
                        break

                image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "GPT-IMG", f"{code}.png"))
                photo = FSInputFile(image_path)
                
                caption = (
                    f"<b>📜 Профиль питомца {pet.pet_name}</b>\n"
                    f"<b>{pet_type_correct}</b>\n"
                    f"🎂 Дата рождения: <code>{pet.pet_birthday}</code>\n"
                    f"❤️ Здоровье: <b>{pet.pet_health} / 100</b>\n"
                    f"🍗 Сытость: <b>{pet.pet_hunger} / 100</b>\n"
                    f"😊 Настроение: <b>{pet.pet_happiness} / 100</b>\n"
                    f"⭐ Уровень: <b>{pet.pet_lvl}</b>\n"
                    f"✨ Опыт: <b>{pet.pet_xp}</b>"
                )

                await message.answer_photo(photo, caption=caption, parse_mode="html")
