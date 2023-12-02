from telethon.sync import TelegramClient

api_id = '20048560'  # Замените на свой API ID, который можно получить на https://my.telegram.org/auth
api_hash = 'c829f30fffc6bea490bd60753417fcbf'  # Замените на свой API Hash, который можно получить на https://my.telegram.org/auth
phone_number = '89680312267'  # Ваш номер телефона с префиксом страны (например, +123456789)

channel_username = 't.me/dobnews'  # Замените на имя пользователя (username) публичного канала
session_name = 'get news'

client = TelegramClient(session_name, api_id, api_hash)

async def get_latest_news():
    await client.connect()

    try:
        await client.start(phone_number, password=None, bot_token=None, force_sms=False)
        channel = await client.get_entity(channel_username)
        messages = await client.get_messages(channel, limit=1)

        if messages:
            latest_message = messages[0]
            print(f"Новость из канала {channel_username}:")
            print(f"Автор: {latest_message.sender_id}")
            print(f"Дата: {latest_message.date}")
            print(f"Текст: {latest_message.text}")

            return [latest_message.date, latest_message.text]
        else:
            print(f"Канал {channel_username} не содержит сообщений.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    await client.disconnect()

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(get_latest_news())