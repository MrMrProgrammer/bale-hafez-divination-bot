import asyncio
from bale import Bot, Message, MenuKeyboardMarkup, MenuKeyboardButton
import aiohttp
from decouple import config
from models import User
from db import init_db

divination_base_url = "https://hafezdivination.pythonanywhere.com/api/divination/"
TOKEN = config("TOKEN")
client = Bot(token=TOKEN)


async def save_user(message):
    chat_id = str(message.chat.id)
    first_name = getattr(message.chat, "first_name", "")
    last_name = getattr(message.chat, "last_name", "")
    username = getattr(message.chat, "username", "")

    user, created = await User.get_or_create(
        chat_id=chat_id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username
        }
    )

    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        await user.save()


async def get_divination():
    async with aiohttp.ClientSession() as session:
        async with session.get(divination_base_url) as resp:
            res = await resp.json()
            return res['number'], res["poem"], res["interpretation"]


@client.event
async def on_message(message: Message):
    await save_user(message)

    if message.content == "/start":
        await message.reply(
            f"سلام {message.author.first_name} 🌸\nبرای گرفتن فال روی دکمه زیر بزن 👇",
            components=MenuKeyboardMarkup().add(
                MenuKeyboardButton('دریافت فال حافظ 📜')
            )
        )

    elif message.text == 'دریافت فال حافظ 📜':
        number, poem, interpretation = await get_divination()

        text = f"""
غزل شماره {number}

{poem}

{interpretation}
"""
        await client.send_message(
            chat_id=message.chat_id,
            text=text
        )


loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())

client.run()
