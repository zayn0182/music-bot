import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import os
import shutil

def load_env(path=".env"):
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

import yt_dlp
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=os.environ["BOT_TOKEN"],
    in_memory=True,
)
assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=os.environ["SESSION_STRING"],
    in_memory=True,
)
call = PyTgCalls(assistant)


def find_audio(query):
    opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "default_search": "ytsearch1",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        return info["title"], info["url"]


@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply_text("Music bot online hai.")


@app.on_message(filters.command("ping"))
async def ping(_, m):
    await m.reply_text("Pong!")


@app.on_message(filters.command("check"))
async def check(_, m):
    await m.reply_text(f"ffmpeg: {shutil.which('ffmpeg')}")


@app.on_message(filters.command("play") & filters.group)
async def play(_, m):
    if len(m.command) < 2:
        return await m.reply_text("Use: /play song name ya link")
    q = " ".join(m.command[1:])
    msg = await m.reply_text("Searching...")
    try:
        title, url = await asyncio.get_running_loop().run_in_executor(
            None, find_audio, q
        )
    except Exception as e:
        return await msg.edit_text(f"Search error: {str(e)[:300]}")
    try:
        await call.play(
            m.chat.id,
            MediaStream(url, video_flags=MediaStream.Flags.IGNORE),
        )
    except Exception as e:
        return await msg.edit_text(f"Play error: {type(e).__name__}: {str(e)[:300]}")
    await msg.edit_text(f"Playing: {title}")


@app.on_message(filters.command("pause") & filters.group)
async def pause(_, m):
    try:
        await call.pause(m.chat.id)
        await m.reply_text("Paused.")
    except Exception as e:
        await m.reply_text(f"Error: {type(e).__name__}")


@app.on_message(filters.command("resume") & filters.group)
async def resume(_, m):
    try:
        await call.resume(m.chat.id)
        await m.reply_text("Resumed.")
    except Exception as e:
        await m.reply_text(f"Error: {type(e).__name__}")


@app.on_message(filters.command("stop") & filters.group)
async def stop(_, m):
    try:
        await call.leave_call(m.chat.id)
        await m.reply_text("Stopped.")
    except Exception as e:
        await m.reply_text(f"Error: {type(e).__name__}")


async def main():
    await app.start()
    await assistant.start()
    await call.start()
    print("Bot started")
    await idle()


loop.run_until_complete(main())
