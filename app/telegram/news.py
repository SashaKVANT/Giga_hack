from telethon.sync import TelegramClient
import asyncio
import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(current_path, '..')
sys.path.append(project_path)

from agent.news_agent import NewsAgent

last_message_post_time = None

async def get_news_coroutine(client, source_channel, queue, stop_flag):
    while not stop_flag.is_set():
        data = await get_latest_news(client, source_channel)
        if data:
            await queue.put(data[1])
        await asyncio.sleep(10)

async def process_data_coroutine(client, dest_channel, auditory_name, queue, stop_flag):
    global last_message_post_time
    while not stop_flag.is_set():
        try:
            data = await asyncio.wait_for(queue.get(), timeout=1.0) 
        except asyncio.TimeoutError:
            continue

        if data[0] != last_message_post_time:
            agent = NewsAgent(auditory_name)
            print("Новость от агента: ")
            pretty_news = agent.run_test(data)
            if pretty_news is not None:
                last_message_post_time = data[0]
                await post_news_to_channel(client, dest_channel, pretty_news)


async def get_latest_news(client, source_channel: str):
    if client.is_connected():
        try:
            channel = await client.get_entity(source_channel)
            messages = await client.get_messages(channel, limit=1)

            if messages:
                latest_message = messages[0]
                print(f"Новость из канала {source_channel}:")
                print(f"Автор: {latest_message.sender_id}")
                print(f"Дата: {latest_message.date}")
                print(f"Текст: {latest_message.text}")

                return [latest_message.date, latest_message.text]
            else:
                print(f"Канал {source_channel} не содержит сообщений.")
        except Exception as e:
            print(f"get_latest_news_error: {e}")

async def post_news_to_channel(client, dest_channel, news_text):
    if client.is_connected():
        try:
            await client.send_message(dest_channel, news_text)
            print("Новость успешно опубликована в канале!")
        except Exception as e:
            print(f"post_news_to_channel_error: {e}")
