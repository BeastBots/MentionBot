from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from bot.config_loader import OWNER_ID
from datetime import datetime
import platform
import psutil
import time
import os
from aiogram.filters import Command

STATS_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bot Stats", callback_data="stats_bot"),
            InlineKeyboardButton(text="Chats", callback_data="stats_chats")
        ]
    ]
)

start_time = time.time()

async def stats_command(message: Message, db):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the bot owner can use this command.")
    await message.reply("Select an option:", reply_markup=STATS_MENU)
    await db["commands.history"].insert_one({
        "command": "stats",
        "user_id": message.from_user.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

def register_stats_handlers(router, db):
    @router.message(Command("stats"))
    async def handle_stats(message: Message):
        await stats_command(message, db)

    @router.callback_query()
    async def handle_stats_callback(call: types.CallbackQuery):
        if not call.data or not call.data.startswith("stats_"):
            return
        if call.data == "stats_bot":
            uptime = int(time.time() - start_time)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            text = (
                f"<b>Bot Stats</b>\n"
                f"OS: {platform.system()} {platform.release()}\n"
                f"Uptime: {uptime // 3600}h {(uptime % 3600) // 60}m\n"
                f"RAM: {mem.available // (1024**2)}MB free / {mem.total // (1024**2)}MB\n"
                f"CPU: {psutil.cpu_percent()}%\n"
                f"Storage: {disk.free // (1024**3)}GB free / {disk.total // (1024**3)}GB\n"
            )
            await call.message.edit_text(text, parse_mode=ParseMode.HTML)
        elif call.data == "stats_chats":
            users = await db["user.pm"].count_documents({})
            groups = await db["groups"].count_documents({})
            text = f"<b>Chats</b>\nUsers: {users}\nGroups: {groups}"
            await call.message.edit_text(text, parse_mode=ParseMode.HTML)
        await call.answer()
