from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from database import get_product_details
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

ASK_QUANTITY, ASK_NAME, ASK_ADDRESS, ASK_PHONE = range(4)

user_orders = {}

# Function to handle user messages (search product)
async def handle_message(update: Update, context: CallbackContext) -> int:
    
    product_code = update.message.text.strip()
    product = get_product_details(product_code)

    if product:
        name, price, stock, colors = product
        response = f"🛍 *{name}*\n💰 قیمت: ${price}\n📦 موجودی: {stock}\n🎨 رنگ ها: {colors}" \
                   f"📌 لطفا تعداد مورد نظر خود را وارد کنید."
        user_orders[update.message.chat_id] = {"product_code"}
        await update.message.reply_text(response, parse_mode="Markdown")
        return ASK_QUANTITY
    else:
        await update.message.reply_text("❌ محصول یافت نشد.")
        return ConversationHandler.END
    
async def ask_name(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    quantity = update.message.text.strip()

    if not quantity.isdigit():
        await update.message.reply_text("❌ لطفا یک عدد وارد کنید.")
        return ASK_QUANTITY
    
    user_orders[chat_id]["quantity"] = int(quantity)
    await update.message.reply_text("📌 لطفا نام خود را وارد کنید.")
    return ASK_NAME

async def ask_adress(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_orders[chat_id]["name"] = update.message.text.strip()

    await update.message.reply_text("📌 لطفا آدرس خود را وارد کنید.")
    return ASK_ADDRESS

async def ask_phone(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_orders[chat_id]["address"] = update.message.text.strip()

    await update.message.reply_text("📌 لطفا شماره تماس خود را وارد کنید.")
    return ASK_PHONE