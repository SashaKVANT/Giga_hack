from telethon.sync import TelegramClient
import logging

LOG = logging.Logger(__name__)

api_id = '20048560'  # Замените на свой API ID
api_hash = 'c829f30fffc6bea490bd60753417fcbf'  # Замените на свой API Hash
phone_number = '89680312267'  # Ваш номер телефона с префиксом страны (например, +123456789)
channel_username = 'https://t.me/news_gigachat'  # Замените на идентификатор вашего канала (например, -1001234567890)
session_name = 'post news'

client = TelegramClient(session_name, api_id, api_hash)

async def post_news_to_channel(news_text):
    await client.connect()
    try:
        await client.start(phone_number, password=None, bot_token=None, force_sms=False)
        await client.send_message(channel_username, news_text)
        LOG.info("Новость успешно опубликована в канале!")

    except Exception as e:
        LOG.error(f"Произошла ошибка: {e}")

    await client.disconnect()