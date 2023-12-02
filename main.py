import asyncio
from server.server import NewsAgentServer

async def main():
    server = NewsAgentServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
