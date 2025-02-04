from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from database import get_product_details
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to handle user messages (search product)
async def handle_message(update: Update, context: CallbackContext) -> None:
    product_code = update.message.text.strip()
    product = get_product_details(product_code)

    if product:
        name, price, stock, colors = product
        response = f"🛍 *{name}*\n💰 قیمت: ${price}\n📦 موجودی: {stock}\n🎨 رنگ ها: {colors}"
    else:
        response = "❌ Product not found."

    await update.message.reply_text(response, parse_mode="Markdown")

# Start the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Message handler for product lookup
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
