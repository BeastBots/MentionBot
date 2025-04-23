from aiogram import types
from aiogram.types import Message
from aiogram.enums import ParseMode
from bot.config_loader import OWNER_ID
from datetime import datetime
import re
from aiogram.filters import Command
import logging

async def broadcast_command(message: Message, db, bot):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the bot owner can use this command.")
    text = message.get_args()
    if not text:
        return await message.reply("Usage: /broadcast <message>")
    # Detect parse mode
    if re.search(r'<.*?>', text):
        parse_mode = ParseMode.HTML
    elif re.search(r'\\*|_', text):
        parse_mode = ParseMode.MARKDOWN_V2
    else:
        parse_mode = ParseMode.MARKDOWN
    # Send to all users and groups
    users = await db["user.pm"].distinct("_id")
    groups = await db["groups"].distinct("_id")
    for uid in users + groups:
        try:
            await bot.send_message(uid, text, parse_mode=parse_mode)
        except Exception:
            continue
    await message.reply("Broadcast sent.")
    await db["commands.history"].insert_one({
        "command": "broadcast",
        "user_id": message.from_user.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

def register_broadcast_handlers(router, db):
    @router.message(Command("broadcast"))
    async def handle_broadcast(message: Message):
        logging.info(f"/broadcast command received in chat {message.chat.id} by user {message.from_user.id}")
        from bot.__main__ import bot
        await broadcast_command(message, db, bot)
