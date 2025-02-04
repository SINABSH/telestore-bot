from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from database import get_product_details
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to handle user messages (search product)
def handle_message(update: Update, context: CallbackContext) -> None:
    product_code = update.message.text.strip()
    product = get_product_details(product_code)

    if product:
        name, price, stock, colors = product
        response = f"🛍 *{name}*\n💰 Price: ${price}\n📦 Stock: {stock}\n🎨 Colors: {colors}"
    else:
        response = "❌ Product not found."

    update.message.reply_text(response, parse_mode="Markdown")

# Start the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Message handler for product lookup
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
