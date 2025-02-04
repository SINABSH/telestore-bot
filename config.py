import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
