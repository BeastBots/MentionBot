import logging
import asyncio
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from motor.motor_asyncio import AsyncIOMotorClient
from bot.config_loader import BOT_TOKEN, MONGODB_URI, OWNER_ID
from bot.handlers import register_handlers

# MongoDB setup
mongo_client = AsyncIOMotorClient(MONGODB_URI)
db = mongo_client["mention"]

async def on_startup(bot: Bot):
    # Ensure DB collections exist
    colls = await db.list_collection_names()
    if "user.pm" not in colls:
        await db.create_collection("user.pm")
    if "groups" not in colls:
        await db.create_collection("groups")
    if "commands.history" not in colls:
        await db.create_collection("commands.history")
    if "boot" not in colls:
        await db.create_collection("boot")
    await db["boot"].insert_one({"event": "booted", "time": str(asyncio.get_event_loop().time())})
    commands = [
        BotCommand(command="help", description="Show help and instructions"),
        BotCommand(command="settings", description="Show settings menu (admins only)"),
        BotCommand(command="cancel", description="Cancel running command")
    ]
    await bot.set_my_commands(commands)
    logging.info("Bot started and commands set.")

async def main():
    logging.basicConfig(level=logging.INFO)
    # Check for UPSTREAM_REPO in config or env before running update.py
    from bot.config_loader import UPSTREAM_REPO
    import os
    upstream_repo = UPSTREAM_REPO or os.environ.get("UPSTREAM_REPO", "")
    if upstream_repo:
        try:
            import subprocess
            logging.info("Running update.py (git pull) before starting bot...")
            result = subprocess.run([sys.executable, "-m", "bot.update"], capture_output=True, text=True)
            logging.info(f"update.py output: {result.stdout}\n{result.stderr}")
        except Exception as e:
            logging.error(f"Failed to run update.py: {e}")
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    from aiogram import Router
    router = Router()
    register_handlers(router, db)
    dp = Dispatcher()
    dp.include_router(router)
    # Start web server for health check
    from webapp import setup_web_app
    app = setup_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()
    await on_startup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
