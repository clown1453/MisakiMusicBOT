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




from callsmusic.callsmusic import client as USER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from helpers.decorators import errors, authorized_users_only

@Client.on_message(filters.group & filters.command(["userbotjoin"]))
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Önce beni grubunuzun yöneticisi olarak ekleyin</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name =  "GoodVibeesMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id,"İstediğiniz gibi buraya katıldım")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Yardımcı zaten sohbetinizde</b>",
        )
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Taşkın Hata bekleyin 🛑 \n Kullanıcı {user.first_name} userbot için katılma isteklerini nedeniyle ağır şekilde gruba katılmak emin kullanıcı grubunda yasaklı olmadığından emin olun olamazdı! Make sure user is not banned in group."
            "\n\nVeya @GoodVibeesMusic'ı Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
        )
        return
    await message.reply_text(
            "<b>yardımcı kullanıcı botu sohbetinize katıldı</b>",
        )
    
@USER.on_message(filters.group & filters.command(["userbotleave"]))
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:  
        await message.reply_text(
            f"<b>Kullanıcı grubunuzdan ayrılamadı! Sel beklemesi olabilir."
            "\n\nVeya beni Grubunuzdan elle atabilirsiniz</b>",
        )
        return
