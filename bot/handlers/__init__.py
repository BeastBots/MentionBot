from bot.config_loader import OWNER_ID
from aiogram import types
from aiogram.filters import Command
from datetime import datetime
from bot.handlers.mention import register_mention_handlers
import logging

async def on_new_chat_member(message, db):
    if message.chat.type in ["group", "supergroup"]:
        await db["groups"].update_one({"_id": message.chat.id}, {"$set": {"title": message.chat.title}}, upsert=True)

async def on_left_chat_member(message, db):
    if message.chat.type in ["group", "supergroup"]:
        pass

def register_handlers(router, db):
    from .settings import register_settings_handlers
    from .help import register_help_handlers
    from .broadcast import register_broadcast_handlers
    from .stats import register_stats_handlers
    register_mention_handlers(router, db)
    register_settings_handlers(router, db)
    register_help_handlers(router, db)
    register_broadcast_handlers(router, db)
    register_stats_handlers(router, db)
    # User tracking
    @router.message()
    async def track_pm(message: types.Message):
        if message.chat.type == "private":
            await db["user.pm"].update_one({"_id": message.from_user.id}, {"$set": {"first_name": message.from_user.first_name, "username": message.from_user.username}}, upsert=True)
    @router.message()
    async def handle_new_member(message: types.Message):
        if message.content_type == types.ContentType.NEW_CHAT_MEMBERS:
            await on_new_chat_member(message, db)
    @router.message()
    async def handle_left_member(message: types.Message):
        if message.content_type == types.ContentType.LEFT_CHAT_MEMBER:
            await on_left_chat_member(message, db)
    @router.message(Command("cancel"))
    async def handle_cancel(message: types.Message):
        await message.reply("❌ Current operation cancelled. If you need help, type /help.")
    @router.message(Command("restart"))
    async def handle_restart(message: types.Message):
        if message.from_user.id != OWNER_ID:
            await message.reply("Only the bot owner can use this command.")
            return
        await message.reply("🔄 Restarting bot...")
        logging.info(f"/restart command received from owner {message.from_user.id}, exiting for restart.")
        import os, sys
        os._exit(0)
