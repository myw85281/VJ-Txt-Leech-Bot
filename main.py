# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(
        f"Hello {m.from_user.mention} 👋\n\n"
        "I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram.\n"
        "Send `/upload` to start.\nUse `/stop` to stop an ongoing task."
    )

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('Send TXT file ⚡️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read().split("\n")

        links = []
        for line in content:
            parts = line.split("://", 1)
            if len(parts) == 2 and parts[1].strip() != "":
                links.append(parts)

        os.remove(x)

        if not links:
            await m.reply_text("No valid links found in file.")
            return

    except Exception as e:
        await m.reply_text(f"**Invalid file input.**\n{e}")
        os.remove(x)
        return

    await editable.edit(f"**Total Links Found:** {len(links)}\nSend starting number (default = 1)")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("Please Send Your Batch Name")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("Enter resolution (144,240,360,480,720,1080)")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    res_map = {
        "144": "256x144", "240": "426x240", "360": "640x360",
        "480": "854x480", "720": "1280x720", "1080": "1920x1080"
    }
    res = res_map.get(raw_text2, "UN")

    await editable.edit("Now Enter A Caption")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)

    MR = " " if raw_text3 == 'Robin' else raw_text3

    await editable.edit("Now send the Thumb URL or 'no'")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        try:
            count = int(raw_text)
        except:
            count = 1

    try:
        for i in range(count - 1, len(links)):
            if len(links[i]) < 2:
                continue  # skip bad lines

            V = links[i][1].replace("file/d/", "uc?export=download&id=") \
                           .replace("www.youtube-nocookie.com/embed", "youtu.be") \
                           .replace("?modestbranding=1", "") \
                           .replace("/view?usp=sharing", "")

            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={
                        'User-Agent': 'Mozilla/5.0'
                    }) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if 'videos.classplusapp' in url:
                url = requests.get(
                    f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                    headers={'x-access-token': 'TOKEN_HERE'}
                ).json()['url']

            if '/master.mpd' in url:
                id = url.split("/")[-2]
                url = f"https://d26g5bnklkwsh4.cloudfront.net/{id}/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "") \
                               .replace("+", "").replace("#", "").replace("|", "") \
                               .replace("@", "").replace("*", "").replace(".", "") \
                               .replace("https", "").replace("http", "").strip()

            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}. {name1}{MR}\n**Batch:** {raw_text0}'
            cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf\n**Batch:** {raw_text0}'

            try:
                if "drive" in url:
                    ka = await helper.download(url, name)
                    await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    count += 1
                    os.remove(ka)
                elif ".pdf" in url:
                    os.system(f'yt-dlp -o "{name}.pdf" "{url}"')
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                    count += 1
                    os.remove(f'{name}.pdf')
                else:
                    Show = f"**Downloading...**\n\n**Name:** `{name}`\n**Quality:** {raw_text2}\n**URL:** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, res_file, thumb, name, prog)
                    count += 1
            except FloodWait as e:
                time.sleep(e.x)
                continue
            except Exception as e:
                await m.reply_text(f"Error: {e}\nName: {name}\nLink: `{url}`")
                continue

    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("**✅ Done Boss 😎**")

bot.run()
