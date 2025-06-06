import logging
from aiogram import types
from aiogram.types import Message
from aiogram.enums import ParseMode
from datetime import datetime
from aiogram.filters import Command

async def help_command(message: Message, db):
    text = (
        "<b>Mention Bot Help</b>\n"
        "@all or #all — Mention all group members\n"
        "@admin or #admin — Mention all admins\n"
        "/help — Show this help\n"
        "/settings — Settings menu (admins only)\n"
        "/cancel — Cancel running command\n"
        "/broadcast <msg> — Owner only: broadcast message\n"
        "/stats — Owner only: show bot stats\n"
    )
    await message.reply(text, parse_mode=ParseMode.HTML)
    await db["commands.history"].insert_one({
        "command": "help",
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

def register_help_handlers(router, db):
    @router.message(Command("help"))
    async def handle_help(message: Message):
        logging.info(f"/help command received in chat {message.chat.id} by user {message.from_user.id}")
        await help_command(message, db)
