from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from database.main import async_session
from database.models.user import User 
from database.models.issue import Issue
from datetime import datetime

class CreateUserIssue(StatesGroup):
    waiting_for_issue_text = State()

router = Router()

@router.message(F.text == "📬 Написать в поддержку")
async def cmd_new_issue(message: Message, state: FSMContext):
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, message.from_user.id)

            if not user:
                await message.answer("Пожалуйста, для начала напишите /start.")
                return

            await state.set_state(CreateUserIssue.waiting_for_issue_text)
            await message.answer(
                "Напишите текст обращения в поддержку <b>ПОДРОБНО</b>.\n"
                "Ваше сообщение будет отправлено администратору.",
                parse_mode="HTML"
            )

            await state.update_data(user_id=user.user_id)

@router.message(CreateUserIssue.waiting_for_issue_text)
async def process_issue_text(message: Message, state: FSMContext):

    issue_text = message.text.strip()
    if not issue_text:
        await message.answer("Пожалуйста, введите текст обращения.")
        return

    async with async_session() as session:
        async with session.begin():
            data = await state.get_data()
            user_id = data.get("user_id")
            
            issue_text = message.text
            
            new_issue = Issue(
                user_id=user_id,
                issue_text=issue_text,
                issue_date=datetime.utcnow().date(),
                issue_status="open",
            )
            
            session.add(new_issue)
            await session.commit()

    await state.clear()
    await message.answer("Ваше обращение в поддержку отправлено. Мы свяжемся с вами в ближайшее время.")