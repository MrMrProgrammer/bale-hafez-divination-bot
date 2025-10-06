import aiohttp

TOPIC = "HafezDivinationBot-EnvYuvYZZzA9MGHZKBv14X40hn8GrFti"

async def send_notification(message: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://ntfy.sh/{TOPIC}', data=message.encode('utf-8')) as resp:
                if resp.status != 200:
                    print(f"Failed to send notification, status: {resp.status}")
    except Exception as e:
        print(f"Error sending notification: {e}")


def build_user_info_message(message):
    user = message.from_user
    chat = message.chat

    msg = f"""
📨 **New Message Received**

🆔 Message ID: {message.message_id or "-"}
🕒 Date: {message.date or "-"}
👤 User ID: {user.id or "-"}
💬 Chat ID: {chat.id or "-"}
🧑‍💼 First Name: {chat.first_name or "-"}
🧑‍💻 Last Name: {getattr(chat, 'last_name', '-') }
📛 Username: {chat.username or "-"}
✉️ Message: {message.text or "-"}
💬 Chat Type: {chat.type or "-"}
"""
    return msg
