import os
import json
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Log setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
ADMIN_IDS_RAW = os.environ.get("ADMIN_IDS", "YOUR_ADMIN_IDS_HERE")
ADMIN_IDS = set(int(x.strip()) for x in ADMIN_IDS_RAW.split(",") if x.strip())

DATA_DIR = "data"
MASTER_FILE = os.path.join(DATA_DIR, "master_lists.json")
VAULT_FILE = os.path.join(DATA_DIR, "vault_lists.json")

os.makedirs(DATA_DIR, exist_ok=True)

# Categories and data helpers
CATEGORIES = [...]
# [Include all other configuration, data helper functions, conversation states, and keyboard definitions from the original script]

# Welcome message
WELCOME_TEXT = "..."  # [Include the original welcome text]

# Original Handlers and Admin Stats Function
# [Include all original handlers and admin_stats function from the given script]

# New Handlers for Spammer Search
async def set_spammer_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide the spammer's channel username or ID.")
        return

    # Save the spammer's channel
    spammer_channel = context.args[0]
    context.user_data['spammer_channel'] = spammer_channel
    await update.message.reply_text(f"Spammer's channel set to: {spammer_channel}")

async def fetch_bin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spammer_channel = context.user_data.get('spammer_channel')
    if not spammer_channel:
        await update.message.reply_text("Spammer's channel is not set. Use /spammer_channel to set it.")
        return

    # Fetch the latest message from the spammer's channel
    try:
        message = await context.bot.get_chat(chat_id=spammer_channel).get_messages()
        bin_list = message[-1].text  # Get the text of the latest message
        if not bin_list:
            await update.message.reply_text("No bin list found in the latest message.")
            return

        # Extract 6-digit bins from the message
        bins = re.findall(r'\b\d{6}\b', bin_list, re.MULTILINE)
        if not bins:
            await update.message.reply_text("No 6-digit bins found in the message.")
            return

        # Save the bins to user data
        context.user_data['bins'] = bins
        await update.message.reply_text(f"Fetched {len(bins)} bins from the spammer's channel.")
    except Exception as e:
        logger.error(f"An error occurred while fetching the bin list: {e}")
        await update.message.reply_text("An error occurred while fetching the bin list. Please try again later.")

async def check_bin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bins = context.user_data.get('bins')
    if not bins:
        await update.message.reply_text("No bins found. Use /fetch_bins to fetch the bin list first.")
        return

    user_id = update.effective_user.id
    vault = get_vault_lists().get(str(user_id), [])
    vault_set = set(vault)

    master_lists = get_master_lists()
    hits = []
    misses = []

    for bin in bins:
        if bin in vault_set or any(bin in master_list for master_list in master_lists.values()):
            hits.append(bin)
        else:
            misses.append(bin)

    result = (
        f"🔐 *Bin List Check Results*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📥 Bins checked: *{len(bins)}*\n"
        f"✅ In vault or master lists: *{len(hits)}*\n"
        f"❌ Not found: *{len(misses)}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
    )
    if hits:
        result += f"\n✅ *Matches:*\n`{'  '.join(hits)}`\n"
    if misses:
        result += f"\n❌ *Not found:*\n`{'  '.join(misses)}`"

    await update.message.reply_text(
        result,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    scheduler = AsyncIOScheduler()

    # Add all handlers (original + new)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("spammer_channel", set_spammer_channel))
    app.add_handler(CommandHandler("fetch_bins", fetch_bin_list))
    app.add_handler(CommandHandler("check_bins", check_bin_list))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Schedule the periodic task (if any)
    # scheduler.add_job(check_channel_for_bin, 'interval', minutes=5, args=[app])
    # scheduler.start()

    logger.info("OxBoys Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()