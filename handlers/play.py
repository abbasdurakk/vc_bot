import os
from os import path
import requests
import aiohttp
import youtube_dl

import callsmusic
import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, PLAY_PIC
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name

from youtube_search import YoutubeSearch
from callsmusic import callsmusic, queues

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Voice
from pyrogram import Client

@Client.on_message(command("play") & other_filters)
@errors
async def play(_, message: Message):

    lel = await message.reply(f"**{bn} :-** 🔄 Müziği arıyorum izninizle...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    hell_pic = PLAY_PIC

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🤖 Bot",
                        url="https://t.me/zevzekcalarbot")
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**{bn} :-** 😥 {DURATION_LIMIT} süreli video oynatamıyoruz"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text(f"**{bn} :-**😟 Ama bana oynatacak bir şey vermedin ki?")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await lel.edit(f"**{bn} :-** #️⃣ Sıraya aldım iyi dinlemeler #{position} !")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo=hell_pic,
        reply_markup=keyboard,
        caption="▶️ Müziği çalıyorum... \n**Ne güzel müzik zevkin varmış :-** {}!".format(
        message.from_user.mention()
        ),
    )
        return await lel.delete()


@Client.on_message(command("ytplay") & other_filters)
@errors
async def play(_, message: Message):

    lel = await message.reply(f"**{bn} :-** 🔎 YouTube'den arama yapıyorum...")
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await lel.edit(f"**{bn} :-** 🎵 Oynatmaya çalışıyorum. {query}")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["Başlık"][:40]       
        thumbnail = results[0]["küçük fotograf"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["süresi"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["görüntüleme"]

    except Exception as e:
        lel.edit(
            f"**{bn} :-** ❌ Müziği bulamadım. \nMüziğin adını yanlış yazmış olabilirsin tekrar dener misin?"
        )
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YouTube'da İzle 🎬",
                        url=f"{url}")
                   
                ]
            ]
        )

    keyboard2 = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YouTube'da İzle 🎬",
                        url=f"{url}")
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    if audio:
        await lel.edit_text(f"**{bn} :-** Hehe 🥴")

    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text(f"**{bn} :-** 😑 Oynatacak bir şey vermedinde verir misin?")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=thumb_name, 
        caption=f"**{bn} :-** İstediğiniz müzik **queued** şekilde #{position} !",
        reply_markup=keyboard2)
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo=thumb_name,
        reply_markup=keyboard,
        caption="▶️ **Oynatıyorum** müzik zevkini beğendim dostum. {}".format(
        message.from_user.mention()
        ),
    )
        return await lel.delete()
