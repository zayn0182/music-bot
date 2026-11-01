import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import os
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

app.run()
