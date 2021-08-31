import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied 
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.WARNING)

JOIN_ASAP = "<b>You can't use this command untill you subscribe my channel</b> "

FSUBB = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="  Join My Channel 🔔 ", url=f"https://t.me/Lexiebotupdate") 
        ]]
    )        

tgraph = Client(
    "Telegraph Uploader bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH
)


@tgraph.on_message(filters.command("start"))

async def start(Client,message):
    try:
        await message.client.get_chat_member(int("-1001267157538"), message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
        text=JOIN_ASAP, disable_web_page_preview=True, reply_markup=FSUBB
    )
        return
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\nI'm Telegraph Uploader Bot",
        disable_web_page_preview=True
    )


@tgraph.on_message(filters.photo)
async def getimage(Client, message):
    dwn = await message.reply_text("Downloading...", True)
    img_path = await message.download()
    await dwn.edit_text("Uploading...")
    try:
        url_path = upload_file(img_path)[0]
    except Exception as error:
        await dwn.edit_text(f"Sorry Something Went Wrong😢\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}"
                    ),
                    InlineKeyboardButton(
                        text="Share Link",
                        url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}",
                    )
                ]
            ]
        )
    )
    os.remove(img_path)


tgraph.run()
