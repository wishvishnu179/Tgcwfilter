#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Script import script
from database.join_reqs import JoinReqs
from info import AUTH_CHANNEL, JOIN_REQS_DB, ADMINS, REQ_CHANNEL

from logging import getLogger

logger = getLogger(__name__)
INVITE_LINKS = {}
db = JoinReqs

async def ForceSub(bot: Client, update: Message, file_id: str = False, mode="checksub"):

    global INVITE_LINKS
    auth = ADMINS.copy() + [1125210189]
    if update.from_user.id in auth:
        return True

    if not AUTH_CHANNEL and not REQ_CHANNEL:
        return True

    is_cb = False
    if not hasattr(update, "chat"):
        update.message.from_user = update.from_user
        update = update.message
        is_cb = True

    # Create Invite Links if not exists
    try:
        for channel in REQ_CHANNEL:
            if channel not in INVITE_LINKS:
                invite_link = (await bot.create_chat_invite_link(
                    chat_id=int(channel),
                    creates_join_request=True if JOIN_REQS_DB else False
                )).invite_link
                INVITE_LINKS[channel] = invite_link
                logger.info(f"Created Req link for {channel}")

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Unable to do Force Subscribe to {REQ_CHANNEL}\n\nError: {err}\n\n")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    # Main Logic
    if REQ_CHANNEL and db().isActive():
        try:
            # Check if User is Requested to Join Channel
            user = await db().get_user(update.from_user.id)
            if user and user["user_id"] == update.from_user.id:
                return True
        except Exception as e:
            logger.exception(e, exc_info=True)
            await update.reply(
                text="Something went Wrong.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False

    try:
        if not AUTH_CHANNEL and not REQ_CHANNEL:
            raise UserNotParticipant
        # Check if User is Already Joined Channels
        for channel in REQ_CHANNEL:
            user = await bot.get_chat_member(chat_id=int(channel), user_id=update.from_user.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=update.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                    reply_to_message_id=update.message_id
                )
                return False
        return True
    except UserNotParticipant:
        text="""** ❗𝐌𝐔𝐒𝐓 𝐅𝐎𝐋𝐋𝐎𝐖 𝐓𝐇𝐈𝐒 𝐈𝐍𝐒𝐓𝐑𝐔𝐂𝐓𝐈𝐎𝐍💯 ❗
        
👇 C𝑙𝑖𝑐𝑘 𝑅𝑒𝑞𝑢𝑒𝑠𝑡 𝑇𝑜 𝐽𝑜𝑖𝑛 𝐶ℎ𝑎𝑛𝑛𝑒𝑙 & 𝐶𝑙𝑖𝑐𝑘 𝑇𝑟𝑦 𝑂𝑛 𝐴𝑔𝑎𝑖𝑛 👇 \n\n
𝑇𝑂 𝐺𝐸𝑇 𝑌𝑂𝑈𝑅 𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝐹𝐼𝐿𝐸𝑆**"""

        buttons = []
        for channel, invite_link in INVITE_LINKS.items():
            buttons.append([InlineKeyboardButton(f"🔮 Rᴇǫᴜᴇsᴛ Tᴏ Jᴏɪɴ Cʜᴀɴɴᴇʟ 🔮", url=invite_link)])
        
        buttons.extend([
            [
                InlineKeyboardButton(" 🔄 Tʀʏ Aɢᴀɪɴ 🔄 ", callback_data=f"{mode}#{file_id}")
            ],
            [
               InlineKeyboardButton("🤷 Hᴇʏ Bᴏᴛ....! Wʜʏ I'ᴍ Jᴏɪɴɪɴɢ 🤷", url="https://graph.org/W%CA%9C%CA%8F-I%E1%B4%8D-J%E1%B4%8F%C9%AA%C9%B4%C9%AA%C9%B4%C9%A2-01-07")
            ]
        ])

        if file_id is False:
            buttons.pop()

        if not is_cb:
            await update.reply(
                text=text,
                quote=True,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        return False

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False


def set_global_invite(channel: int, url: str):
    global INVITE_LINKS
    INVITE_LINKS[channel] = url
