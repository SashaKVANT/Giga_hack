from fastapi import FastAPI
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig
from fastapi.middleware.cors import CORSMiddleware
from telethon.sync import TelegramClient
import asyncio
import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(current_path, '..')
sys.path.append(project_path)

from telegram.client_conf import TelegramClientConfig, phone_number
from telegram.news import get_news_coroutine, process_data_coroutine
from server.models import AgentRequestModel

class NewsAgentServer:
    phone_number: str = phone_number

    def __init__(self):
        self.data_queue = asyncio.Queue()
        self.stop_flag = asyncio.Event()

    async def start(self, port: int = 8000):
        """Start the agent server."""
        print("Starting the agent server...")
        config = HypercornConfig()
        config.bind = [f"localhost:{port}"]
        app = FastAPI(
            title="News Agent Server",
            version="v0.2",
        )

        # Add CORS middleware
        origins = [
            "http://localhost:5000",
            "http://127.0.0.1:5000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            # Add any other origins you want to whitelist
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        telegram_config = TelegramClientConfig(
            session_name='get news',
            api_id='20048560',
            api_hash='c829f30fffc6bea490bd60753417fcbf',
        )
        self.telegram_client = TelegramClient(telegram_config.session_name, 
                                              telegram_config.api_id, 
                                              telegram_config.api_hash)
        await self.telegram_client.connect()
        await self.telegram_client.start(self.phone_number, password=None, bot_token=None, force_sms=False)

        print(f"NewsAgentServer server starting on http://localhost:{port}")

        @app.post("/start")
        async def start_generating_news(request: AgentRequestModel):
            self.stop_flag.clear()

            asyncio.create_task(get_news_coroutine(self.telegram_client, 
                                                   request.source_channel, 
                                                   self.data_queue, 
                                                   self.stop_flag))
            asyncio.create_task(process_data_coroutine(self.telegram_client, 
                                                       request.dest_channel, 
                                                       request.auditory_name,
                                                       self.data_queue, 
                                                       self.stop_flag))

            return {"message": "Generating news started"}
        
        @app.post("/stop")
        async def stop_generating_news():
            self.stop_flag.set()

            return {"message": "Stop"}
        
        await hypercorn_serve(app, config)

    async def process_data(self):
        return {"Hello": "World"}

        # dest_channel = request_data.dest_channel
        # source_channel = request_data.source_channel
        # auditory_name = request_data.auditory_name