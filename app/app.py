from typing import Dict
from telethon import TelegramClient, events
import asyncio
from .worker import event_handler


def register_event(user_client: TelegramClient, bot_client: TelegramClient):

    @bot_client.on(events.NewMessage)
    async def new_message_handler(event):
        await event_handler(event, user_client, bot_client)


class app:

    user_client = None
    bot_client = None

    def __init__(
        self, user_client: TelegramClient = None, bot_client: TelegramClient = None
    ):
        pass

    def init_app(self, config: dict):
        proxy = config.get("proxy")
        proxy_dict = None
        if proxy:
            proxy_dict = {
                "proxy_type": proxy["scheme"],
                "addr": proxy["hostname"],
                "port": proxy["port"],
                "username": proxy.get("username"),
                "password": proxy.get("password"),
            }
        self.user_client = TelegramClient(
            "telegram_forward_bot",
            api_id=config["api_id"],
            api_hash=config["api_hash"],
            proxy=proxy_dict,
        )
        self.bot_client = TelegramClient(
            "bot",
            api_id=config["api_id"],
            api_hash=config["api_hash"],
            proxy=proxy_dict,
        ).start(bot_token=config["bot_token"])
        register_event(self.user_client, self.bot_client)
        print("init app finish ")

    async def start_client(self):
        await self.user_client.start()
        print("server start.")

    def run(self, config: Dict):
        self.init_app(config)
        try:
            asyncio.get_event_loop().run_until_complete(self.start_client())
            self.bot_client.run_until_disconnected()
        except Exception as e:
            print(e)
