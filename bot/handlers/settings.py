from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from pymongo import MongoClient
import config

# MongoDB setup
client = MongoClient(config.MONGO_URI)
db = client['telegram_bot']
settings_collection = db['settings']

def update_settings(chat_id, key, value):
    settings_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )

def get_settings(chat_id):
    return settings_collection.find_one({"chat_id": chat_id}) or {}

def handle_message_format(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    settings = get_settings(chat_id)
    current_setting = settings.get("message_format", "Small")

    keyboard = [
        [InlineKeyboardButton("Small", callback_data='message_format_small')],
        [InlineKeyboardButton("Big", callback_data='message_format_big')],
        [InlineKeyboardButton("Back", callback_data='settings_back')],
        [InlineKeyboardButton("Close", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.edit_message_text(
        f"Message Format\n\nCurrent Setting: {current_setting}\n\nExplanation:\n- Small: Sends mentions in batches of 5.\n- Big: Sends mentions up to Telegram's message limit.",
        reply_markup=reply_markup
    )

def handle_silent_mention(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    settings = get_settings(chat_id)
    current_setting = settings.get("silent_mention", "Off")

    keyboard = [
        [InlineKeyboardButton("Off", callback_data='silent_mention_off')],
        [InlineKeyboardButton("On", callback_data='silent_mention_on')],
        [InlineKeyboardButton("Back", callback_data='settings_back')],
        [InlineKeyboardButton("Close", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.edit_message_text(
        f"Silent Mention\n\nCurrent Setting: {current_setting}\n\nExplanation:\n- Off: Mentions normally with @username.\n- On: Mentions silently with [username](https://t.me/username).",
        reply_markup=reply_markup
    )

def handle_bot_access(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    settings = get_settings(chat_id)
    current_setting = settings.get("bot_access", "Admins Only")

    keyboard = [
        [InlineKeyboardButton("Admins Only", callback_data='bot_access_admins')],
        [InlineKeyboardButton("All Users", callback_data='bot_access_all')],
        [InlineKeyboardButton("Back", callback_data='settings_back')],
        [InlineKeyboardButton("Close", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.edit_message_text(
        f"Bot Access\n\nCurrent Setting: {current_setting}\n\nExplanation:\n- Admins Only: Commands can only be used by admins.\n- All Users: Commands can be used by all group members.",
        reply_markup=reply_markup
    )
