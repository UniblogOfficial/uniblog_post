import asyncio
import configparser

import requests
from aiogram import Bot, types


def get_bot_token():
    config = configparser.ConfigParser()
    config.read("settings.ini", encoding='utf-8')
    bot_token = config["Bot"]["bot_tokens"].split(";")[0]

    return bot_token


def get_channel_id(username):  # Возвращает id канала по нику пользователя
    bot_token = get_bot_token()

    r = requests.get(url=f"https://api.telegram.org/bot{bot_token}/getUpdates")

    events = list(filter(lambda x: "my_chat_member" in x.keys(), r.json()['result']))
    if len(events) == 0:
        return "not completed"

    events = list(filter(lambda x: x["my_chat_member"]["from"]["username"] == username, events))
    events.sort(key=lambda x: -int(x["my_chat_member"]["date"]))

    current_channel = events[0]
    if len(events) == 0:
        return "wrong username"
    elif False in [current_channel["my_chat_member"]["new_chat_member"]["can_post_messages"],
                   current_channel["my_chat_member"]["new_chat_member"]["can_edit_messages"]]:
        return "not enough rights"

    channel_id = events[0]["my_chat_member"]["chat"]["id"]
    return int(channel_id)


async def send_text_post(channel_id, post="Hello, world!"):  # Отправка поста (html вкл.)
    bot_token = get_bot_token()
    bot = Bot(token=bot_token)

    await bot.send_message(channel_id, post, parse_mode=types.ParseMode.HTML)

    await bot.close()


async def send_media_post(channel_id, text="Hello, world", files=None):  # files = [только фото и видео в формате mp4]
    if files is None:
        files = ["photo.png", "video.mp4"]

    bot_token = get_bot_token()
    bot = Bot(token=bot_token)

    group = types.MediaGroup()
    inputs = []
    i = 0
    for file in files:
        if file.split(".")[-1] == "mp4":
            if i == 0:
                inputs.append(types.InputMedia(type="video", media=open(f"media/{file}", "rb"), caption=text))
            else:
                inputs.append(types.InputMedia(type="video", media=open(f"media/{file}", "rb")))
            i += 1
        else:
            try:
                if i == 0:
                    inputs.append(types.InputMedia(type="photo", media=open(f"media/{file}", "rb"), caption=text))
                else:
                    inputs.append(types.InputMedia(type="photo", media=open(f"media/{file}", "rb")))
                i += 1
            except Exception as e:
                print(e)

    for inp in inputs:
        group.attach_many(inp)

    await bot.send_media_group(channel_id, media=group)


async def check_rights(channel_id):  # Проверка на права администратора
    bot_token = get_bot_token()
    bot = Bot(token=bot_token)

    admins = await bot.get_chat_administrators(channel_id)
    await bot.close()

    try:
        me = list(filter(lambda x: x.user.username == "uniblog_1bot", admins))[0]
        if me.can_post_messages and me.can_edit_messages and me.can_delete_messages:
            return True
        return False
    except IndexError:
        return False


'''          #Example
    id = get_channel_id("channel")
    if asyncio.get_event_loop().run_until_complete(check_rights(id)):
        asyncio.get_event_loop().run_until_complete(send_post(channel_id=id, post="New post"))
        # asyncio.get_event_loop().run_until_complete(send_media_post(channel_id=id, text="New post", files=["photo.png", "video.mp4"]))
'''
