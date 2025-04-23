from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from config import OWNER_ID
from datetime import datetime
import re

async def broadcast_command(message: Message, db, bot):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the bot owner can use this command.")
    text = message.get_args()
    if not text:
        return await message.reply("Usage: /broadcast <message>")
    # Detect parse mode
    if re.search(r'<.*?>', text):
        parse_mode = types.ParseMode.HTML
    elif re.search(r'\\*|_', text):
        parse_mode = types.ParseMode.MARKDOWN_V2
    else:
        parse_mode = types.ParseMode.MARKDOWN
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

def register_broadcast_handlers(dp: Dispatcher, db):
    @dp.message_handler(commands=["broadcast"])
    async def handle_broadcast(message: Message):
        from bot.__main__ import bot
        await broadcast_command(message, db, bot)
