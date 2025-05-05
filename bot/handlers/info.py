from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📖 Информация")
async def info_project(message: Message):
    await message.answer(
        "<b>🐶 Pet-Master ждёт тебя!</b>\n\n"
        "В этом месте начинается твоя маленькая история.\n"
        "Ты сможешь познакомиться с тем, кто будет рядом — нуждаться в тебе, радоваться вместе и меняться со временем.\n\n"
        "Забота, внимание и немного игры — вот что ему нужно.\n"
        "Но помни... если забыть надолго, кто-то может почувствовать себя одиноким 😿\n\n"
        "Чтобы начать, нажми или напиши <b>🐶 Мой питомец</b>.",
        parse_mode="HTML",
    )
