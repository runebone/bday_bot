import telebot
from db import Database
from config import * # FIXME: Namespaces are one honking great idea

with open(".API_TOKEN_TEST") as f:
    API_TOKEN = f.readline()[:-1]

# Initialize database
db = Database(Config.Database.file)

# Initialize bot
bot = telebot.TeleBot(API_TOKEN)
