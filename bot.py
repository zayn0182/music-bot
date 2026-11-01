import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import os

def load_env(path=".env"):
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

from pyrogram import Client, filters

app = Client(
    "musicbot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"],
    in_memory=True,
)

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply_text("Music bot online hai.")

@app.on_message(filters.command("ping"))
async def ping(_, m):
    await m.reply_text("Pong!")


@app.on_message(filters.command("check"))
async def check(_, m):
    import shutil
    ff = shutil.which("ffmpeg")
    try:
        import pytgcalls
        tg = "ok"
    except Exception as e:
        tg = f"error: {e}"
    try:
        import yt_dlp
        yd = yt_dlp.version.__version__
    except Exception as e:
        yd = f"error: {e}"
    await m.reply_text(f"ffmpeg: {ff}\npytgcalls: {tg}\nyt-dlp: {yd}")

app.run()
