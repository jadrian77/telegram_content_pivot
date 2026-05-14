from urllib.parse import urlparse, parse_qs
from telethon import TelegramClient
from telethon.tl.types import (
    Message,
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    MessageMediaDocument,
    MessageMediaPhoto,
)
import os
from typing import Optional, Union


def is_telegram_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and result.netloc in (
            "t.me",
            "telegram.me",
        )
    except:
        return False


class Telegram_URL:
    channel_id: Union[str, int, None] = None
    is_protect: bool = False
    message_id: Optional[int] = None
    comment_id: Optional[int] = None
    topic_id: Optional[int] = None


def check_url_type(telegram_url: str) -> Telegram_URL:

    try:
        url_components = urlparse(telegram_url)
        url_infos = [c for c in url_components.path.split("/") if c]
        query = parse_qs(url_components.query)
    except Exception:
        raise

    url_data = Telegram_URL()
    if len(url_infos) == 2 and url_infos[0] != "c":
        url_data.channel_id = url_infos[0]
        url_data.message_id = int(url_infos[1])
    if "comment" in query:
        url_data.channel_id = url_infos[0]
        url_data.message_id = int(url_infos[1])
        url_data.comment_id = int(query["comment"][0])

    if len(url_infos) == 3:
        if url_infos[0] == "c":
            url_data.channel_id = int(f"-100{url_infos[1]}")
            url_data.message_id = int(url_infos[2])
            url_data.is_protect = True
        else:
            url_data.channel_id = url_infos[0]
            url_data.message_id = int(url_infos[2])
    elif len(url_infos) == 4 and url_infos[0] == "c":
        url_data.channel_id = int(f"-100{url_infos[1]}")
        url_data.message_id = int(url_infos[3])
        url_data.is_protect = True
    if not url_data.channel_id or not url_data.message_id:
        raise ValueError("cannot split any message id")
    return url_data


async def get_group_message(
    user_client: TelegramClient, url_data: Telegram_URL
) -> list:
    messages = await user_client.get_messages(
        url_data.channel_id,
        ids=[
            msg_id
            for msg_id in range(url_data.message_id - 9, url_data.message_id + 11)
        ],
    )
    media_group_id = (
        messages[9].grouped_id
        if len(messages) == 20
        else messages[url_data.message_id - 1].grouped_id
    )
    if media_group_id is None:
        return list()
    return list(msg for msg in messages if msg and msg.grouped_id == media_group_id)


def get_media_type(message: Message) -> Optional[str]:
    if not message.media:
        return None
    if isinstance(message.media, MessageMediaPhoto):
        return "photo"
    if isinstance(message.media, MessageMediaDocument):
        doc = message.media.document
        for attr in doc.attributes:
            if hasattr(attr, "voice") and isinstance(attr.voice, bool):
                return "voice" if attr.voice else "audio"
            if hasattr(attr, "round_message") and isinstance(attr.round_message, bool):
                return "video_note" if attr.round_message else "video"
        return "document"
    return None


async def url_handler(
    telegram_url: str, user_client: TelegramClient, bot_client: TelegramClient
):
    url_data = check_url_type(telegram_url)

    msg_entity = await user_client.get_messages(
        url_data.channel_id, ids=url_data.message_id
    )
    caption = msg_entity.message
    msg_media = getattr(msg_entity, "media")
    user_me = await user_client.get_me()
    if not msg_media:
        await bot_client.send_message(user_me.id, caption)
        return

    messages = [msg_entity]
    if msg_entity.grouped_id:
        messages = await get_group_message(user_client, url_data)

    if len(messages) <= 0:
        raise Exception("not get any message.")

    if not url_data.is_protect:
        bot_read_msg_entitys = await bot_client.get_messages(
            url_data.channel_id, ids=list(msg.id for msg in messages if msg)
        )
        bot_read_msg_entitys = list(
            msg_entitys for msg_entitys in bot_read_msg_entitys if msg_entitys
        )
        if len(bot_read_msg_entitys) > 0:
            try:
                await bot_client.forward_messages(user_me.id, bot_read_msg_entitys)
                return
            except:
                pass

    files = []
    attributes = []
    voice = None
    for message in messages:

        media_type = get_media_type(message)
        if not media_type:
            continue

        if media_type == "video":
            msg_file_metadata = getattr(message, "file")
            attributes.append(
                DocumentAttributeVideo(
                    h=msg_file_metadata.height,
                    w=msg_file_metadata.width,
                    duration=msg_file_metadata.duration,
                    round_message=True,
                    supports_streaming=True,
                )
            )
        if media_type == "photo" or media_type == "document":
            attributes.append(None)
        if media_type == "voice" or media_type == "audio":
            msg_file_metadata = getattr(message, "file")
            duration, title = msg_file_metadata.duration, msg_file_metadata.title
            attributes.append(
                DocumentAttributeAudio(
                    duration=duration,
                    voice=(media_type == "voice"),
                    title=title,
                )
            )
        files.append(await user_client.download_media(message))
        if media_type == "voice":
            voice = files[len(files) - 1]
            break

    if len(files) > 0:
        wait_send_files = files
        if voice != None:
            wait_send_files = voice
        await bot_client.send_file(
            user_me.id, wait_send_files, caption=caption, attributes=attributes
        )
        for file in files:
            os.remove(file)
    print(f"done for url={telegram_url}")


async def event_handler(event, user_client, bot_client):
    event_text = event.raw_text
    if is_telegram_url(event_text):
        await url_handler(event_text, user_client, bot_client)
    else:
        raise Exception("not a telegram message url")
