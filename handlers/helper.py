from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import command, other_filters2, other_filters



@Client.on_message(command("help") & other_filters2)
async def helper(ok, message: Message):
    await message.reply_text(
        f"""💅 Merhaba! Beni şu komutlar ile yönetebilirsin **{bn}** -
Hali hazırda desteklediğim komutlar:

👶🏻 **Kullanıcı komutu **
⚜️ /play   - > __Müziği başlatır.__
⚜️ /song   - > __Müzik araması yapar.__
⚜️ /ytplay - > __YouTube linki oynatır.__
⚜️ /repo   - > __Yapımcımın kanallarına ve kendisine ulaşabilirsin__


🧑🏻 **Admin komutları:**
⚜️ /pause  - > __Müziği durdurur__
⚜️ /resume - > __Oyantma listesini devam ettirir__
⚜️ /skip   - > __Bir sonraki müzige geçeer__
⚜️ /stop   - > __Müzik listesini temizyip sesli sohbetten ayrılır.__""")

@Client.on_message(command("help") & other_filters)
async def ghelp(_, message: Message):
    await message.reply_text(f"**{bn} :-** Komutlarımı öğrenmek istiyorsan pm gelir misin? 😉")
