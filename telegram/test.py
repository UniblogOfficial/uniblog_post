import asyncio

from aiogram import Bot, types


async def main():
    bot_token = "5364686786:AAEsjKSkTFeKTMK6yNrjZu54rpS13xehIks"
    bot = Bot(token=bot_token)

    group = types.MediaGroup()
    inputs = [types.InputMedia(media=open("media/photo.png", "rb"), caption="123"),
              types.InputMedia(type="video", media=open("media/video.avi", "rb"))]
    for inp in inputs:
        group.attach_many(inp)

    await bot.send_media_group(1156324879, media=group)


for i, a in enumerate(["a"]):
    print(i)
