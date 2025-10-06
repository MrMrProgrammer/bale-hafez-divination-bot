from bale import Bot, CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, MenuKeyboardMarkup, MenuKeyboardButton
import aiohttp
from decouple import config

divination_base_url = "https://hafezdivination.pythonanywhere.com/api/divination/"
TOKEN = config("TOKEN")

client = Bot(token=TOKEN)

async def get_divination():
    async with aiohttp.ClientSession() as session:
        async with session.get(divination_base_url) as resp:
            res = await resp.json()
            return res['number'], res["poem"], res["interpretation"]


@client.event
async def on_message(message: Message):
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

        # inline_keyboard = InlineKeyboardMarkup().add(
        #     InlineKeyboardButton("📖 دریافت تفسیر", callback_data=interpretation)
        # )

        await client.send_message(
            chat_id=message.chat_id,
            text=text,
            # components=inline_keyboard
        )


# @client.event
# async def on_callback_query(callback: CallbackQuery):
#     interpretation = callback.data
#     await client.send_message(
#         chat_id=callback.message.chat_id,
#         text=f"📖 تفسیر فال:\n\n{interpretation}"
#     )


client.run()
