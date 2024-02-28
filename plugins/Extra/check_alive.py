import time
import random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("alive", CMD))
async def check_alive(_, message):
    await message.reply_text("Hᴇʟʟᴏ Dᴇᴀʀ 😌 I ᴀᴍ ᴀʟɪᴠᴇ ❤️ Pʀᴇss /start Usᴇ Mᴇ")


@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"🏓Pᴏɴɢ! {time_taken_s:.3f} ᴍs")
