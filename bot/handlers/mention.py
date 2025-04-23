from telegram import Update, ParseMode
from telegram.ext import CallbackContext

def mention_all(update: Update, context: CallbackContext):
    chat = update.effective_chat
    members = chat.get_members()

    mentions = []
    for member in members:
        if not member.user.is_bot:
            mentions.append(f"@{member.user.username}")

    # Send mentions in batches of 5
    for i in range(0, len(mentions), 5):
        update.message.reply_text(" ".join(mentions[i:i+5]), parse_mode=ParseMode.HTML)

def mention_admins(update: Update, context: CallbackContext):
    chat = update.effective_chat
    admins = chat.get_administrators()

    mentions = []
    for admin in admins:
        if not admin.user.is_bot:
            mentions.append(f"@{admin.user.username}")

    update.message.reply_text(" ".join(mentions), parse_mode=ParseMode.HTML)
