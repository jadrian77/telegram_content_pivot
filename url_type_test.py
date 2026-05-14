import safe_load_config
from app import worker
from telethon import TelegramClient
import asyncio

config = safe_load_config.load_config()
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
user_client = TelegramClient(
    "telegram_forward_bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    proxy=proxy_dict,
)
bot_client = TelegramClient(
    "bot", api_id=config["api_id"], api_hash=config["api_hash"], proxy=proxy_dict
).start(bot_token=config["bot_token"])


async def url_test():
    await user_client.start()
    url_list = [
        "https://t.me/c/1234567/123",
        #
    ]
    try:
        for url in url_list:
            print(f"start test url= {url}")
            await worker.url_handler(url, user_client, bot_client)
            print(f"test url= {url} done.")
    except Exception as e:
        print(e)


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(url_test())
