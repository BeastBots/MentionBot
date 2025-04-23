from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from pymongo import MongoClient
import logging
import config
from bot.handlers.mention import mention_all, mention_admins
from bot.handlers.settings import handle_message_format, handle_silent_mention, handle_bot_access
from bot.database import users_collection, groups_collection, commands_history_collection, boot_collection
import platform
import psutil
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# MongoDB setup
client = MongoClient(config.MONGO_URI)
db = client['telegram_bot']
settings_collection = db['settings']

# Log bot boot event
def log_boot():
    boot_collection.insert_one({
        "event": "booted",
        "timestamp": time.time()
    })

# Track users and groups
def track_user_or_group(update):
    if update.effective_user:
        users_collection.update_one(
            {"user_id": update.effective_user.id},
            {"$set": {"username": update.effective_user.username}},
            upsert=True
        )
    if update.effective_chat and update.effective_chat.type in ["group", "supergroup"]:
        groups_collection.update_one(
            {"group_id": update.effective_chat.id},
            {"$set": {"title": update.effective_chat.title}},
            upsert=True
        )

# Command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Telegram Mention Bot! Use /help to see available commands.")

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "/all or #all - Mention all group members\n"
        "/admin or #admin - Mention all group admins\n"
        "/help - Show this help message\n"
        "/cancel - Cancel the running command\n"
        "/settings - Open the settings menu (Admins only)"
    )
    update.message.reply_text(help_text)

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Command cancelled.")

def settings(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat

    # Check if the user is an admin
    if not user.id in [admin.user.id for admin in chat.get_administrators()]:
        update.message.reply_text("Only admins can access the settings menu.")
        return

    # Create settings menu
    keyboard = [
        [InlineKeyboardButton("Message Format", callback_data='message_format')],
        [InlineKeyboardButton("Silent Mention", callback_data='silent_mention')],
        [InlineKeyboardButton("Bot Access", callback_data='bot_access')],
        [InlineKeyboardButton("Close", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Bot Settings", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Handle button clicks
    if query.data == 'message_format':
        handle_message_format(update, context)
    elif query.data == 'silent_mention':
        handle_silent_mention(update, context)
    elif query.data == 'bot_access':
        handle_bot_access(update, context)
    elif query.data == 'close':
        query.delete_message()

# Owner-only commands
def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != config.OWNER_ID:
        update.message.reply_text("This command is restricted to the bot owner.")
        return

    if not context.args:
        update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)

    # Auto-detect format
    if "<" in message and ">" in message:
        parse_mode = "HTML"
    elif "*" in message or "_" in message or "`" in message:
        parse_mode = "MarkdownV2"
    else:
        parse_mode = "Markdown"

    # Broadcast to users
    for user in users_collection.find():
        try:
            context.bot.send_message(
                chat_id=user["user_id"], text=message, parse_mode=parse_mode
            )
        except Exception as e:
            logger.error(f"Failed to send message to user {user['user_id']}: {e}")

    # Broadcast to groups
    for group in groups_collection.find():
        try:
            context.bot.send_message(
                chat_id=group["group_id"], text=message, parse_mode=parse_mode
            )
        except Exception as e:
            logger.error(f"Failed to send message to group {group['group_id']}: {e}")

    update.message.reply_text("Broadcast completed.")

def stats(update: Update, context: CallbackContext):
    if update.effective_user.id != config.OWNER_ID:
        update.message.reply_text("This command is restricted to the bot owner.")
        return

    keyboard = [
        [InlineKeyboardButton("Bot Stats", callback_data='bot_stats')],
        [InlineKeyboardButton("Chats", callback_data='chats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select an option:", reply_markup=reply_markup)

def handle_stats_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'bot_stats':
        uptime = time.time() - psutil.boot_time()
        stats_message = (
            f"OS: {platform.system()} {platform.release()}\n"
            f"Uptime: {uptime // 3600} hours\n"
            f"Free RAM: {psutil.virtual_memory().available // (1024 * 1024)} MB\n"
            f"CPU Usage: {psutil.cpu_percent()}%\n"
            f"Storage: {psutil.disk_usage('/').free // (1024 * 1024)} MB free"
        )
        query.edit_message_text(stats_message)

    elif query.data == 'chats':
        users = users_collection.count_documents({})
        groups = groups_collection.count_documents({})
        query.edit_message_text(f"Users: {users}\nGroups: {groups}")

def main():
    # Initialize the bot
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(CommandHandler("settings", settings))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Register mention commands
    dispatcher.add_handler(CommandHandler(["all", "#all"], mention_all))
    dispatcher.add_handler(CommandHandler(["admin", "#admin"], mention_admins))

    # Register new handlers
    dispatcher.add_handler(CommandHandler("broadcast", broadcast))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CallbackQueryHandler(handle_stats_buttons))

    # Track users and groups in all updates
    dispatcher.add_handler(MessageHandler(Filters.all, track_user_or_group))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    log_boot()
    main()
