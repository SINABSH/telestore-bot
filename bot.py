from telegram import Update
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
    print(f"Received product code: {product_code}")  # Debug message

    product = get_product_details(product_code)
    if product:
        name, price, stock, colors = product
        response = (f"🛍 *{name}*\n💰 Price: ${price}\n📦 Stock: {stock}\n🎨 Colors: {colors}\n\n"
                    f"📌 Reply with the quantity to order.")
        chat_id = update.message.chat_id
        user_orders[chat_id] = {"product_code": product_code}
        print(f"Stored product code in user_orders for chat_id {chat_id}")  # Debug message
        
        await update.message.reply_text(response, parse_mode="Markdown")
        return ASK_QUANTITY  # Move to the next step
    else:
        print("Product not found")  # Debug message
        await update.message.reply_text("❌ Product not found.")
        return ConversationHandler.END

async def ask_name(update: Update, context: CallbackContext) -> int:
    """Stores quantity and asks for the customer's name."""
    chat_id = update.message.chat_id
    quantity = update.message.text.strip()
    print(f"Received quantity: {quantity} for chat_id {chat_id}")  # Debug message

    if not quantity.isdigit():
        print("Invalid quantity received")  # Debug message
        await update.message.reply_text("❌ Please enter a valid number.")
        return ASK_QUANTITY
    
    user_orders[chat_id]["quantity"] = int(quantity)
    print(f"Stored quantity in user_orders for chat_id {chat_id}")  # Debug message
    
    await update.message.reply_text("📌 Please enter your full name.")
    return ASK_NAME

async def ask_address(update: Update, context: CallbackContext) -> int:
    """Stores name and asks for the customer's address."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["customer_name"] = update.message.text.strip()
    print(f"Stored customer name in user_orders for chat_id {chat_id}")  # Debug message

    await update.message.reply_text("📌 Enter your delivery address.")
    return ASK_ADDRESS

async def ask_phone(update: Update, context: CallbackContext) -> int:
    """Stores address and asks for the phone number."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["address"] = update.message.text.strip()
    print(f"Stored address in user_orders for chat_id {chat_id}")  # Debug message

    await update.message.reply_text("📌 Enter your phone number.")
    return ASK_PHONE

async def confirm_order(update: Update, context: CallbackContext) -> int:
    """Finalizes order and saves it in the database."""
    chat_id = update.message.chat_id
    user_orders[chat_id]["phone"] = update.message.text.strip()
    print(f"Stored phone number in user_orders for chat_id {chat_id}")  # Debug message

    # Save the order in the database
    order = user_orders.pop(chat_id)
    print(f"Saving order: {order}")  # Debug message
    
    try:
        order_id = save_order(order["product_code"], order["quantity"], order["customer_name"], order["address"], order["phone"])
        response = f"✅ Order placed successfully!\n🆔 Order ID: {order_id}\n📦 Thank you for your purchase!"
        print(f"Order saved successfully with ID: {order_id}")  # Debug message
    except Exception as e:
        response = f"❌ Error saving order: {e}"
        print(f"Error saving order: {e}")  # Debug message
    
    await update.message.reply_text(response)
    return ConversationHandler.END

def main():
    """Start the bot."""
    print("Starting bot...")  # Debug message
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
    print("Bot is polling...")  # Debug message
    application.run_polling()

if __name__ == "__main__":
    main()
