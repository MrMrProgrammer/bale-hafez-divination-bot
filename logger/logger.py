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
💬 New Message Received
User ID: {user.id}
Chat ID: {chat.id}
First Name: {chat.first_name}
Last Name: {getattr(chat, 'last_name')}
Username: {chat.username}
Message: {message.text}
"""
    return msg
