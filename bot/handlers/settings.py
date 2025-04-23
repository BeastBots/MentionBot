from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from datetime import datetime

SETTINGS_MENU = InlineKeyboardMarkup(row_width=2)
SETTINGS_MENU.add(
    InlineKeyboardButton("Message Format", callback_data="settings_format"),
    InlineKeyboardButton("Silent Mention", callback_data="settings_silent"),
    InlineKeyboardButton("Bot Access", callback_data="settings_access"),
    InlineKeyboardButton("Close", callback_data="settings_close")
)

async def settings_menu(message: Message, db):
    # Only admins can access
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin():
        return await message.reply("Only group admins can access settings.")
    await message.reply("Bot Settings", reply_markup=SETTINGS_MENU)
    await db["commands.history"].insert_one({
        "command": "settings",
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "date": datetime.utcnow(),
        "status": "completed"
    })

def register_settings_handlers(dp: Dispatcher, db):
    @dp.message_handler(commands=["settings"])
    async def handle_settings(message: Message):
        await settings_menu(message, db)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("settings_"))
    async def handle_settings_callback(call: CallbackQuery):
        group_id = call.message.chat.id
        group_settings = await db["groups"].find_one({"_id": group_id}) or {}
        if call.data == "settings_format":
            current = group_settings.get("mention_format", "small")
            text = f"Bot Settings -> Message Format\n\nCurrent Setting: <b>{current.capitalize()}</b>\n\n- Small: Mentions in batches of 5.\n- Big: Mentions up to Telegram's max limit."
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(
                InlineKeyboardButton("Small", callback_data="format_small"),
                InlineKeyboardButton("Big", callback_data="format_big"),
                InlineKeyboardButton("Back", callback_data="settings_back"),
                InlineKeyboardButton("Close", callback_data="settings_close")
            )
            await call.message.edit_text(text, reply_markup=kb, parse_mode=types.ParseMode.HTML)
        elif call.data == "settings_silent":
            current = group_settings.get("silent", False)
            text = f"Bot Settings -> Silent Mention\n\nCurrent Setting: <b>{'On' if current else 'Off'}</b>\n\n- Off: Normal @user mention.\n- On: Silent [user](https://t.me/user) mention."
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(
                InlineKeyboardButton("Off", callback_data="silent_off"),
                InlineKeyboardButton("On", callback_data="silent_on"),
                InlineKeyboardButton("Back", callback_data="settings_back"),
                InlineKeyboardButton("Close", callback_data="settings_close")
            )
            await call.message.edit_text(text, reply_markup=kb, parse_mode=types.ParseMode.HTML)
        elif call.data == "settings_access":
            current = group_settings.get("access", "admins")
            text = f"Bot Settings -> Bot Access\n\nCurrent Setting: <b>{'Admins Only' if current == 'admins' else 'All Users'}</b>\n\n- Admins Only: Only admins can use mention commands.\n- All Users: Anyone can use mention commands."
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(
                InlineKeyboardButton("Admins Only", callback_data="access_admins"),
                InlineKeyboardButton("All User", callback_data="access_all"),
                InlineKeyboardButton("Back", callback_data="settings_back"),
                InlineKeyboardButton("Close", callback_data="settings_close")
            )
            await call.message.edit_text(text, reply_markup=kb, parse_mode=types.ParseMode.HTML)
        elif call.data == "settings_back":
            await call.message.edit_text("Bot Settings", reply_markup=SETTINGS_MENU)
        elif call.data == "settings_close":
            await call.message.delete()
        await call.answer()

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("format_"))
    async def handle_format_change(call: CallbackQuery):
        value = call.data.split("_")[1]
        await db["groups"].update_one({"_id": call.message.chat.id}, {"$set": {"mention_format": value}})
        await call.answer("Message format updated.", show_alert=True)
        await call.message.delete()

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("silent_"))
    async def handle_silent_change(call: CallbackQuery):
        value = call.data.split("_")[1] == "on"
        await db["groups"].update_one({"_id": call.message.chat.id}, {"$set": {"silent": value}})
        await call.answer("Silent mention updated.", show_alert=True)
        await call.message.delete()

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("access_"))
    async def handle_access_change(call: CallbackQuery):
        value = "admins" if call.data.endswith("admins") else "all"
        await db["groups"].update_one({"_id": call.message.chat.id}, {"$set": {"access": value}})
        await call.answer("Bot access updated.", show_alert=True)
        await call.message.delete()
