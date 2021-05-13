import os

from pyrogram import Client
from pyrogram.types import Message, Voice

import youtube_dl
from youtube_search import YoutubeSearch
import requests

from config import BOT_NAME as Bn
from helpers.filters import command, other_filters
from helpers.decorators import errors

@Client.on_message(command("song") & other_filters)
@errors
async def a(client, message: Message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    okvai = query.capitalize()
    print(query.capitalize())
    m = await message.reply(f"**{Bn} :-** 🔍 Müziği arıyorum. {okvai}")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["Başlık"]
            thumbnail = results[0]["küçük fotograf"][0]
            duration = results[0]["süresi"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["Görüntüleme"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            m.edit(f"**{Bn} :-** 😕 Malesef bulamadım. Yazım hatası yapmış olabilir misin?\n\n{e}")
            return
    except Exception as e:
        m.edit(
           f"**{Bn} :-** 😕 Bulamadım. üzgünüm.\n\nMüziğin adını doğru yazdın mı?."
        )
        print(str(e))
        return
    await m.edit(f"**{Bn} :-** 📥 indiriyorum...\n**arattığınız :-** {query}")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎶 **Başlık:** [{title[:35]}]({link})\n⏳ **Süre:** {duration}\n👀 **Görüntüleme:** {views}'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await  message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        await m.delete()
    except Exception as e:
        m.edit(f"❌ Hata!! \n\n{e}")
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
