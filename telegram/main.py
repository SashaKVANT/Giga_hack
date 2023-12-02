import asyncio
import news
import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(current_path, '..')
sys.path.append(project_path)

from agent.news_agent import NewsAgent

last_message_post_time = None

async def get_news_corutine(queue):
    while True:
        data = await news.get_latest_news()
        if data:
            await queue.put(data[1])
        await asyncio.sleep(10)

async def process_data_corutine(queue):
    global last_message_post_time
    while True:
        data = await queue.get()
        if data[0] != last_message_post_time:
            agent = NewsAgent('любители животных') #TODO
            print("Новость от агента: ")
            pretty_news = agent.Run(data)
            if pretty_news != None:
                last_message_post_time = data[0]
                await news.post_news_to_channel(pretty_news)

async def main():
    loop = asyncio.get_event_loop()
    data_queue = asyncio.Queue()

    get_news_task = loop.create_task(get_news_corutine(data_queue))
    post_news_task = loop.create_task(process_data_corutine(data_queue))

    await asyncio.gather(get_news_task, post_news_task)

asyncio.run(main())