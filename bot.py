from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext, ConversationHandler
from database import get_product_details, save_order
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Conversation states
ASK_QUANTITY, ASK_NAME, ASK_ADDRESS, ASK_PHONE = range(4)

# Dictionary to store user orders temporarily
user_orders = {}

async def handle_message(update: Update, context: CallbackContext) -> int:
    """Handles product lookup and starts ordering process."""
    product_code = update.message.text.strip()
    product = get_product_details(product_code)

    if product:
        name, price, stock, colors = product
        response = f"🛍 *{name}*\n💰 Price: ${price}\n📦 Stock: {stock}\n🎨 Colors: {colors}\n\n" \
                   f"📌 Reply with the quantity to order."
        user_orders[update.message.chat_id] = {"product_code": product_code}
        await update.message.reply_text(response, parse_mode="Markdown")
        return ASK_QUANTITY  # Move to the next step
    else:
        await update.message.reply_text("❌ Product not found.")
        return ConversationHandler.END  # End conversation if product not found

async def ask_name(update: Update, context: CallbackContext) -> int:
    """Stores quantity and asks for the customer's name."""
    chat_id = update.message.chat_id
    quantity = update.message.text.strip()

    if not quantity.isdigit():
        await update.message.reply_text("❌ Please enter a valid number.")
        return ASK_QUANTITY

    user_orders[chat_id]["quantity"] = int(quantity)
    await update.message.reply_text("📌 Please enter your full name.")
    return ASK_NAME

async def ask_address(update: Update, context: CallbackContext) -> int:
    """Stores name and asks for the customer's address."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["customer_name"] = update.message.text.strip()

    await update.message.reply_text("📌 Enter your delivery address.")
    return ASK_ADDRESS

async def ask_phone(update: Update, context: CallbackContext) -> int:
    """Stores address and asks for the phone number."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["address"] = update.message.text.strip()

    await update.message.reply_text("📌 Enter your phone number.")
    return ASK_PHONE

async def confirm_order(update: Update, context: CallbackContext) -> int:
    """Finalizes order and saves it in the database."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["phone"] = update.message.text.strip()

    # Save the order in the database
    order = user_orders.pop(chat_id)
    order_id = save_order(order["product_code"], order["quantity"], order["customer_name"], order["address"], order["phone"])

    response = f"✅ Order placed successfully!\n🆔 Order ID: {order_id}\n📦 Thank you for your purchase!"
    await update.message.reply_text(response)
    return ConversationHandler.END

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            ASK_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
