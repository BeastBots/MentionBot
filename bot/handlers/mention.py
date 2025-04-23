from aiogram import types
from aiogram.types import Message
from aiogram.enums import ParseMode
from datetime import datetime

MENTION_COMMANDS = ["all", "#all", "admin", "#admin"]

async def mention_all(message: Message, db):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("This command can only be used in groups.")
    await db["groups"].update_one({"_id": message.chat.id}, {"$set": {"title": message.chat.title}}, upsert=True)
    # Fetch all members (requires bot to be admin)
    try:
        members = []
        async for member in message.bot.iter_chat_members(message.chat.id):
            if not member.user.is_bot:
                members.append(member.user)
    except Exception as e:
        return await message.reply("❌ Failed to fetch members. Make sure the bot is admin.")
    # Get mention settings
    group_settings = await db["groups"].find_one({"_id": message.chat.id}) or {}
    mention_format = group_settings.get("mention_format", "small")
    silent = group_settings.get("silent", False)
    # Prepare mention text
    def mention_user(user):
        if silent:
            return f"[{user.first_name}](https://t.me/{user.username or 'user?id=' + str(user.id)})"
        else:
            return f"@{user.username}" if user.username else f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    batch_size = 5 if mention_format == "small" else 30
    mentions = [mention_user(u) for u in members]
    for i in range(0, len(mentions), batch_size):
        text = " ".join(mentions[i:i+batch_size])
        try:
            await message.reply(text, parse_mode=ParseMode.MARKDOWN if silent else ParseMode.HTML, disable_notification=silent)
        except Exception:
            continue
    await db["commands.history"].insert_one({
        "command": "mention_all",
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

async def mention_admins(message: Message, db):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("This command can only be used in groups.")
    await db["groups"].update_one({"_id": message.chat.id}, {"$set": {"title": message.chat.title}}, upsert=True)
    try:
        admins = await message.bot.get_chat_administrators(message.chat.id)
        members = [a.user for a in admins if not a.user.is_bot]
    except Exception as e:
        return await message.reply("❌ Failed to fetch admins. Make sure the bot is admin.")
    group_settings = await db["groups"].find_one({"_id": message.chat.id}) or {}
    mention_format = group_settings.get("mention_format", "small")
    silent = group_settings.get("silent", False)
    def mention_user(user):
        if silent:
            return f"[{user.first_name}](https://t.me/{user.username or 'user?id=' + str(user.id)})"
        else:
            return f"@{user.username}" if user.username else f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    batch_size = 5 if mention_format == "small" else 30
    mentions = [mention_user(u) for u in members]
    for i in range(0, len(mentions), batch_size):
        text = " ".join(mentions[i:i+batch_size])
        try:
            await message.reply(text, parse_mode=ParseMode.MARKDOWN if silent else ParseMode.HTML, disable_notification=silent)
        except Exception:
            continue
    await db["commands.history"].insert_one({
        "command": "mention_admins",
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

def register_mention_handlers(router, db):
    @router.message()
    async def handle_all(message: types.Message):
        if message.text and (message.text.lower().startswith("@all") or message.text.lower().startswith("#all")):
            await mention_all(message, db)

    @router.message()
    async def handle_admin(message: types.Message):
        if message.text and (message.text.lower().startswith("@admin") or message.text.lower().startswith("#admin")):
            await mention_admins(message, db)
