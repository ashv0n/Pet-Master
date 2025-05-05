import os
from dotenv import load_dotenv

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

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")