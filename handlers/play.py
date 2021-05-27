#MisakiDev | ByMisakiMey


from os import path
from typing import Dict
from pyrogram import Client
from pyrogram.types import Message, Voice
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from callsmusic import callsmusic, queues
from helpers.admins import get_administrators
from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
from pyrogram import filters, emoji
from pyrogram.types import InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
import traceback
import os
import sys
from callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.admins import admins as a
import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import que
from Python_ARQ import ARQ
import json
import wget
chat_id = None

           


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer('You ain\'t allowed!', show_alert=True)
            return
    return decorator                                                                       
                                          
                                          
                                          
                                          
def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((205, 550), f"Title: {title}", (51, 215, 255), font=font)
    draw.text(
        (205, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((205, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((205, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


 

@Client.on_message(
    filters.command("playlist")
    & filters.group
    & ~ filters.edited
)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text('Çalma listesi boş')
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style='md')
    msg = "**Şimdi Oynatılıyor** {}".format(message.chat.title)
    msg += "\n- "+ now_playing
    msg += "\n- Req by "+by
    temp.pop(0)
    if temp:
        msg += '\n\n'
        msg += '**Sıra**'
        for song in temp:
            name = song[0]
            usr = song[1].mention(style='md')
            msg += f'\n- {name}'
            msg += f'\n- Req by {usr}\n'
    await message.reply_text(msg)       
    
# ============================= Settings =========================================

def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
    #if chat.id in active_chats:
        stats = '**{}** Ayarları'.format(chat.title)
        if len(que) > 0:
            stats += '\n\n'
            stats += 'Ses yüzdesi : {}%\n'.format(vol)
            stats += 'Sıradaki şarkılar : `{}`\n'.format(len(que))
            stats += 'Şimdi Oynatılıyor : **{}**\n'.format(queue[0][0])
            stats += 'İsteyen : {}'.format(queue[0][1].mention)
    else:
        stats = None
    return stats

def r_ply(type_):
    if type_ == 'play':
        ico = '▶'
    else:
        ico = '⏸'
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('⏹', 'leave'),
                InlineKeyboardButton('⏸', 'puse'),
                InlineKeyboardButton('▶️', 'resume'),
                InlineKeyboardButton('⏭', 'skip')
                
            ],
            [
                InlineKeyboardButton('Oynatma Listesi 📖', 'Oynatma Listesi'),
                
            ],
            [       
                InlineKeyboardButton("❌ Kapat",'cls')
            ]        
        ]
    )
    return mar

@Client.on_message(
    filters.command("current")
    & filters.group
    & ~ filters.edited
)
async def ee(client, message):
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)              
    else:
        await message.reply('Bu sohbette çalışan sanal devre örneği yok')

@Client.on_message(
    filters.command("player")
    & filters.group
    & ~ filters.edited
)
@authorized_users_only
async def settings(client, message):
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply('pause'))
            
        else:
            await message.reply(stats, reply_markup=r_ply('play'))
    else:
        await message.reply('Bu sohbette çalışan sanal devre örneği yok')

@Client.on_callback_query(filters.regex(pattern=r'^(playlist)$'))
async def p_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat
    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'playlist':           
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Çalma listesi boş')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "**Şimdi Oynatılıyor** {}".format(cb.message.chat.title)
        msg += "\n- "+ now_playing
        msg += "\n- Req by "+by
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg += '**Sıra**'
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n- {name}'
                 msg += f'\n- Req by {usr}\n'
        await cb.message.edit(msg)      

@Client.on_callback_query(filters.regex(pattern=r'^(play|pause|skip|leave|puse|resume|menu|cls)$'))
@cb_admin_check
async def m_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'pause':
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chat_id] == 'paused'
                ):
            await cb.answer('Sohbet bağlı değil!', show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer('Müzik Duraklatıldı!')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('play'))
                

    elif type_ == 'play':       
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chat_id] == 'playing'
            ):
                await cb.answer('Sohbet bağlı değil!', show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer('Müzik Devam Ettirildi!')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('pause'))
                     

    elif type_ == 'playlist':
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Çalma listesi boş')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "**Şimdi Oynatılıyor** {}".format(cb.message.chat.title)
        msg += "\n- "+ now_playing
        msg += "\n- Req by "+by
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg += '**Sıra**'
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n- {name}'
                 msg += f'\n- {usr} tarafından istek\n'
        await cb.message.edit(msg)      
                      
    elif type_ == 'resume':     
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chat_id] == 'playing'
            ):
                await cb.answer('Sohbet bağlı değil veya zaten oynatılıyor', show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer('Müzik Devam Ettirildi!')     
    elif type_ == 'puse':         
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chat_id] == 'paused'
                ):
            await cb.answer('Sohbet bağlı değil veya zaten duraklatılmış', show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer('Müzik Duraklatıldı!')
    elif type_ == 'cls':          
        await cb.answer('Menü kapadı')
        await cb.message.delete()       

    elif type_ == 'menu':  
        stats = updated_stats(cb.message.chat, qeue)  
        await cb.answer('Menü açıldı')
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⏹', 'leave'),
                    InlineKeyboardButton('⏸', 'puse'),
                    InlineKeyboardButton('▶️', 'resume'),
                    InlineKeyboardButton('⏭', 'skip')
                
                ],
                [
                    InlineKeyboardButton('Oynatma Listesi 📖', 'Oynatma Listesi'),
                
                ],
                [       
                    InlineKeyboardButton("❌ Kapat",'cls')
                ]        
            ]
        )
        await cb.message.edit(stats, reply_markup=marr) 
    elif type_ == 'skip':        
        if qeue:
            skip = qeue.pop(0)
        if chat_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer('Sohbet bağlı değil!', show_alert=True)
        else:
            callsmusic.queues.task_done(chat_id)

            if callsmusic.queues.is_empty(chat_id):
                callsmusic.pytgcalls.leave_group_call(chat_id)
                
                await cb.message.edit('- Artık Oynatma Listesi Yok..\n- Vc den Ayrılıyor!')
            else:
                callsmusic.pytgcalls.change_stream(
                    chat_id,
                    callsmusic.queues.get(chat_id)["file"]
                )
                await cb.answer('Skipped')
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(f'- Atlanan parça\n- Şimdi Çalıyor **{qeue[0][0]}**')

    else:      
        if chat_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chat_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chat_id)
            await cb.message.edit('Sohbetten Başarıyla Ayrıldı!')
        else:
            await cb.answer('Sohbet bağlı değil!', show_alert=True)

@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 **İşleniyor**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name =  "helper"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await _.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message.from_user.id:  
                          try:
                              invitelink = await _.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "<b>Önce beni grubunuzun yöneticisi olarak ekleyin</b>",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message.chat.id,"Bu gruba VC'de müzik çalmak için katıldım")
                              await lel.edit(
                                  "<b>Yardımcı Userbot sohbetinize katıldı</b>",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"<b>🔴 Taşkın Hata bekleyin 🔴 \nKullanıcı {user.first_name} nedeniyle userbot ağır isteklerine gruba katılmak olamazdı! emin kullanıcı grubunda yasaklı olmadığından emin olun."
                                  "\n\nVeya @MisakiDJbot'u Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} Userbot bu sohbette yok, Yöneticiden ilk kez komut göndermesini /play isteyin veya {user.first_name} öğesini manuel olarak ekleyin</i>"
        )
        return     
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    await lel.edit("🔎 **Bulunuyor**")
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await lel.edit("🎵 **İşleniyor**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit("Şarkı bulunamadı. Başka bir şarkı deneyin veya belki doğru şekilde heceleyin.")
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
            [   
                [
                               
                    InlineKeyboardButton('📖 Oynatma Listesi', callback_data='Oynatma Listesi'),
                    InlineKeyboardButton('Menu ⏯ ', callback_data='menu')
                
                ],                     
                [
                    InlineKeyboardButton(
                        text="YouTube'da İzle 🎬",
                        url=f"{url}")

                ],
                [       
                    InlineKeyboardButton(
                        text="❌ Kapat",
                        callback_data='cls')

                ]                             
            ]
        )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)  
    file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
        photo="final.png", 
        caption=f"#⃣ İstediğiniz şarkı **sıraya girdi** {position} konumunda!",
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = message.chat.id
        que[chat_id] = []
        qeue = que.get(message.chat.id)
        s_name = title            
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]      
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="▶️ **Oynatılıyor** Bu Grupta {} tarafından Grup Müzik Botu ile istenen şarkı çalınıyor 👨‍🎤".format(
        message.from_user.mention()
        ),
    )
        os.remove("final.png")
        return await lel.delete()


@Client.on_message(
    filters.command("dplay")
    & filters.group
    & ~ filters.edited
)
async def deezer(client: Client, message_: Message):
    global que
    lel = await message_.reply("🔄 **İşleniyor**")
    administrators = await get_administrators(message_.chat)
    chid = message_.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name =  "GoodVibeesMusic"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await client.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message_.from_user.id:  
                          try:
                              invitelink = await client.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "<b>Önce beni grubunuzun yöneticisi olarak ekleyin</b>",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message_.chat.id,"Bu gruba VC'de müzik çalmak için katıldım")
                              await lel.edit(
                                  "<b>Yardımcı Userbot sohbetinize katıldı</b>",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"<b>🔴 Taşkın Hata bekleyin 🔴 \nKullanıcı {user.first_name} nedeniyle userbot ağır isteklerine gruba katılmak olamazdı! emin kullanıcı grubunda yasaklı olmadığından emin olun."
                                  "\n\nVeya @MisakiUserBOt'u Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} Userbot bu sohbette yok, Yöneticiden ilk kez komut göndermesini /play isteyin veya {user.first_name} öğesini manuel olarak ekleyin</i>"
        )
        return                            
    requested_by = message_.from_user.first_name   

    text = message_.text.split(" ", 1)
    queryy = text[1]
    res = lel
    await res.edit(f"Deezer'da `{queryy}` Aranıyor")
    try:
        arq = ARQ("https://thearq.tech")
        r = await arq.deezer(query=queryy, limit=1)
        title = r[0]["title"]
        duration = int(r[0]["duration"])
        thumbnail = r[0]["thumbnail"]
        artist = r[0]["artist"]
        url = r[0]["url"]
    except:
        await res.edit(
            "Hiçbişey bulamadım usta.."
        )
        is_playing = False
        return
    keyboard = InlineKeyboardMarkup(
         [   
             [
                 InlineKeyboardButton('📖 Oynatma Listesi', callback_data='Oynatma Listesi'),
                 InlineKeyboardButton('Menu ⏯ ', callback_data='menu')     
             ],                     
             [
                 InlineKeyboardButton(
                     text="Deezer'da Dinle 🎬",
                     url=f"{url}")

             ],
             [       
                 InlineKeyboardButton(
                     text="❌ Kapat",
                     callback_data='cls')

            ]                      
         ]
     )
    file_path= await converter.convert(wget.download(url))
    await res.edit("Küçük Resim Oluşturuluyor")
    await generate_cover(requested_by, title, artist, duration, thumbnail)
    if message_.chat.id in callsmusic.pytgcalls.active_calls:
        await res.edit("sıraya ekleme")
        position = await queues.put(message_.chat.id, file=file_path)       
        qeue = que.get(message_.chat.id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.edit_text(f"♪ Good Vibes Music ♪= #️⃣ {position} konumunda sıraya alındı")
    else:
        await res.edit_text("♪ Good Vibes Music ♪=▶️ Çalınıyor.....")
        chat_id = message_.chat.id
        que[chat_id] = []
        qeue = que.get(message_.chat.id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message_.chat.id, file_path)

    await res.delete()

    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"Deezer Üzerinden [{title}]({url}) oynatma"
    ) 
    os.remove("final.png")


@Client.on_message(
    filters.command("splay")
    & filters.group
    & ~ filters.edited
)
async def jiosaavn(client: Client, message_: Message):
    global que
    lel = await message_.reply("🔄 **İşleniyor**")
    administrators = await get_administrators(message_.chat)
    chid = message_.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name =  "MisakiMusic"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await client.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message_.from_user.id:  
                          try:
                              invitelink = await client.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "<b>Önce beni grubunuzun yöneticisi olarak ekleyin</b>",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message_.chat.id,"Bu gruba VC'de müzik çalmak için katıldım")
                              await lel.edit(
                                  "<b>Yardımcı Userbot sohbetinize katıldı</b>",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"<b>🔴 Taşkın Hata bekleyin 🔴 \nKullanıcı {user.first_name} nedeniyle userbot ağır isteklerine gruba katılmak olamazdı! emin kullanıcı grubunda yasaklı olmadığından emin olun."
                                  "\n\nVeya @MisakiUserBot'u Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            "<i> Yardımcı Kullanıcı botu bu sohbette yok, Yöneticiden ilk kez komut göndermesini /play veya asistanı manuel olarak eklemesini isteyin</i>"
        )
        return     
    requested_by = message_.from_user.first_name
    chat_id=message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = lel
    await res.edit(f"Searching for `{query}` on jio saavn")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://jiosaavnapi.bhadoo.uk/result/?query={query}"
            ) as resp:
                r = json.loads(await resp.text())
        sname = r[0]["song"]
        slink = r[0]["media_url"]
        ssingers = r[0]["singers"]
        sthumb = r[0]["image"]
        sduration = int(r[0]["duration"])
    except Exception as e:
        await res.edit(
            "Ne demek istedini anlamadım bilader..."
        )
        print(str(e))
        is_playing = False
        return
    keyboard = InlineKeyboardMarkup(
         [   
             [
               InlineKeyboardButton('📖 Oynatma Listesi', callback_data='Oynatma Listesi'),
               InlineKeyboardButton('Menu ⏯ ', callback_data='menu')   
             ],                     
             [
               InlineKeyboardButton(
                   text="Müzik kanalıma katılın",
                   url='https://t.me/Fmsarkilar')
             ],
             [       
               InlineKeyboardButton(
                   text="❌ Kapat",
                   callback_data='cls')

            ]                          
         ]
     )
    file_path= await converter.convert(wget.download(slink))
    if message_.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message_.chat.id, file=file_path)
        qeue = que.get(message_.chat.id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.delete()
        m = await client.send_photo(
            chat_id=message_.chat.id,
            reply_markup=keyboard,
            photo="final.png",
            caption=f"♪ MisakiMusic ♪=#️⃣ {position} konumunda sıraya alındı",
        
        )           
           
    else:
        await res.edit_text("♪ MisakiMusic ♪=▶️ Çalıyor .....")
        chat_id = message_.chat.id
        que[chat_id] = []
        qeue = que.get(message_.chat.id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message_.chat.id, file_path)
    await res.edit("Küçük Resim Oluşturuluyor.")
    await generate_cover(requested_by, sname, ssingers, sduration, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"Jiosaavn Üzerinden {sname} Oynanıyor",
        
    )
    os.remove("final.png")

# Have u read all. If read RESPECT :-)
