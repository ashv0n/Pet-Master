from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery 
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import State, StatesGroup
from database.main import async_session 
from database.models.user import User 
from database.models.pet import Pet 
from datetime import datetime
from .pet_profile import p_profile

pets = [
    ("🐶 Собачка", "dog"),
    ("🐱 Кошечка", "cat"),
    ("🐧 Пингвинчик", "penguin"),
    ("🟢 Слаймик", "slime"),
    ("🐵 Бабуинчик", "baboon"),
    ("🐼 Пандочка", "panda"),
    ("🐻 Медвежонок", "bear"),
    ("🐉 Дракончик", "dragon"),
    ("🍄 Грибочек", "mushroom"),
    ("🤖 Хомячок", "hamster"),
    ("👻 Котенок-дух", "ghostcat"),
    ("🫧 Амёба", "amoeba"),
]

class CreateUserPet(StatesGroup):
    waiting_for_pet_name = State()

router = Router()

@router.message(F.text == "🐶 Мой питомец")
async def cmd_my_pet(message: Message):

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, message.from_user.id)
            if user.user_pet_id:
                pet = await session.get(Pet, user.user_pet_id)
            else:
                pet = None
            if not pet:

                kb = InlineKeyboardBuilder()

                kb.button(text="🐶 Завести питомца", callback_data="create_pet")
                kb.button(text="❌ Отмена", callback_data="cancel_pet")
                kb.adjust(2)

                await message.answer(
                    "К сожалению, у вас нет питомца. Давайте заведем его?\n",
                    reply_markup=kb.as_markup()
                )
            
            else: 
                await p_profile(message, user, pet)
            
@router.callback_query(F.data == "create_pet")
async def create_pet(callback: CallbackQuery):
    await callback.message.delete()

    kb = InlineKeyboardBuilder()
    for name, code in pets:
        kb.button(text=name, callback_data=f"choose_{code}")
    kb.button(text="❌ Отмена", callback_data="cancel_pet")
    kb.adjust(3)


    await callback.message.answer(
        "Выберите какого питомца вы хотите",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data == "cancel_pet")
async def cancel_pet(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Вы отменили создание своего нового питомца.\n"
        "Если кнопок нет, пропишите /start для обновления меню."
    )

@router.callback_query(F.data.startswith("choose_"))
async def handle_choose_pet(callback: CallbackQuery, state: FSMContext):
    pet_code = callback.data.removeprefix("choose_")
    
    for pet, code in pets:
        if code == pet_code:
            await callback.message.delete()

            await state.update_data(pet_type=code, pet_w=pet)
            await state.set_state(CreateUserPet.waiting_for_pet_name)

            await callback.message.answer(
                f"Вы выбрали <b>{pet}</b>, теперь давайте дадим ему имя\n"
                "Введите как вы хотите его назвать", parse_mode="html"
            )
            return
        
    await callback.message.answer("Такого питомца не существует")
    
@router.message(CreateUserPet.waiting_for_pet_name)
async def process_pet_name(message: Message, state: FSMContext):

    kb = InlineKeyboardBuilder()
    kb.button(text="🐶 Мой питомец", callback_data="my_pet")
    kb.adjust(1)

    pet_name = message.text.strip().capitalize()

    data = await state.get_data()
    pet_type = data.get("pet_type")
    pet_w = data.get("pet_w")

    async with async_session() as session:
        async with session.begin():
            new_pet = Pet(
                owner_id=message.from_user.id,

                pet_type=pet_type, 
                pet_name=pet_name,
                pet_birthday=datetime.utcnow().date(),

                pet_hunger=100,
                pet_happiness=100,
                pet_health=100,
                pet_lvl=1,
                pet_xp=0,

            )
            session.add(new_pet)
            await session.flush()
            user = await session.get(User, message.from_user.id)
            user.user_pet_id = new_pet.pet_id

    await state.clear()

    await message.answer(
        f"Ваш новый питомец <b>{pet_w}</b> и зовут его <b>{pet_name}</b>! 🎉\n", parse_mode="html"
    )