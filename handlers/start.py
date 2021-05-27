# ZauteMusic (Telegram bot project )
# Copyright (C) 2021  ZauteKm 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn




@Client.on_message(
    filters.command("start")
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b><b>Hoş geldiniz {message.from_user.first_name}!</b>

<b>🎙️ GoodVibesMusic</b> yeni yöntemlerle</b> olabildiğince basit, gruplarınızda müzik <b>Oynatmak,</b> için tasarlanmış bir <b>as projedir</b> sesli sohbetler.

<b>❓ Nasıl kullanılır?</b>
botun komutlarının tam listesini görmek için! » 🎛 <b>Komutlar</b> düğmesine ve Hits /help düğmesine basın <b>GoodVibesMusic!</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Beni Grubunuza Ekleyin ➕", url="t.me/GoodVibeesBot?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "🎛️ Komutlar", url="https://telegra.ph/GoodVibesMusic-05-12"
                    ),
                    InlineKeyboardButton(
                        "👑Sahibim👑", url="https://t.me/Poyraz2103")
                    ],[
                    InlineKeyboardButton(
                        "Müzik Kanalım🎵", url="https://t.me/Fmsarkilar"
                    ),
                    InlineKeyboardButton(
                        "Assistanım🎼", url="https://t.me/GoodVibeesMusic"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "👑Boz Kürt👑", url="https://t.me/sarlockHolmes"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(
    filters.command("start")
    & filters.group
    & ~ filters.edited
)
async def start(client: Client, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ <b>Bir YouTube videosu mu aramak istiyorsunuz?</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Müzik Kanalım🎵", url="https://t.me/Fmsarkilar"
                    )
                ],    
                [    
                    InlineKeyboardButton(
                        "✅ Evet", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "❌ Hayır", callback_data="close"
                    )
                ]
            ]
        )
    )

@Client.on_message(
    filters.command("help")
    & filters.private
    & ~ filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b><u>Yararlı Komutlar!</u>
\n/play <song name> - istediğiniz şarkıyı çalın
/dplay <song name> - deezer aracılığıyla istediğiniz şarkıyı çalın
/splay <song name> - jio saavn aracılığıyla istediğiniz şarkıyı çalın
/playlist - Şimdi çalma listesini göster
/current - Şimdi çalan göster
/song <song name> - istediğiniz şarkıları hızlı bir şekilde indirin
/search <query> - youtube'daki videoları ayrıntılarla arayın
/deezer <song name> - istediğiniz şarkıları deezer ile hızlıca indirin
/saavn <song name> - istediğiniz şarkıları saavn aracılığıyla hızlıca indirin
/video <song name> - istediğiniz videoları hızlı bir şekilde indirin
\n<u>Yalnızca yöneticiler</u>
/player - müzik çalar ayarları panelini aç
/pause - şarkı çalmayı duraklatır
/resume - şarkıyı çalmaya devam et
/skip - sonraki şarkıyı çal
/end - müzik çalmayı durdur
/userbotjoin - asistanı sohbetinize davet edin
/admincache - Yönetici listesini yeniler
 </b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Müzik Kanalım🎵", url="https://t.me/Fmsarkilar"
                    )
                ]
            ]
        )
    )    
