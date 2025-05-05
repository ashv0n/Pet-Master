from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message()
async def handle_everything(message: Message):
    await message.answer(f"""\
{message.text} — не удалось обработать как команду.
Возможно, вы допустили опечатку, или у вас нет доступа.
Напишите /start для обновления меню.
""")