#!/usr/bin/python
import re
import telebot
import bot_commands as bc
from db import Database
from config import *

# Initialize database; global constant
db = Database(Config.Database.file)

# For callback functions
def get_database():
    return db

# Get API token
with open(".API_TOKEN") as f:
    API_TOKEN = f.readline()[:-1]

bot = telebot.TeleBot(API_TOKEN)

# ===============================================

@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, BotText.START)
    bot.send_message(message.chat.id, message.chat.id)
    bot.send_message(message.chat.id, type(message.chat.id))

@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(message.chat.id, BotText.ADD)
    bot.register_next_step_handler(message, bc.add.process_add_step, bot, db)

@bot.message_handler(commands=["delete", "cut"])
def delete(message):
    bc.delete.process_delete_step(message, bot, db)

@bot.message_handler(commands=["show", "see"])
def show(message):
    bc.show.process_show_step(message, bot, db)

@bot.message_handler(commands=["edit", "change"])
def edit(message):
    bc.edit.process_edit_step(message, bot, db)

# Callbacks for all functions
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "cb_edit":
            bot.send_message(call.message.chat.id, "Edit.")
            index = get_index_from_bot_message(call.message)
        elif call.data == "cb_delete":
            index = get_index_from_bot_message(call.message)
            db = get_database()
            db.delete_record_by_index(call.message.chat.id, index)
            bot.send_message(call.message.chat.id, "Deleted.")
    except RecordIndexOutOfRange:
        bot.send_message(call.message.chat.id, FailText.RecordIndexOutOfRange)
        bot.register_next_step_handler(call.message, process_delete_step, bot, db)
    except Exception as e:
        bot.send_message(call.message.chat.id, FailText.UncaughtError.format(str(e)))

# FIXME: kill it
def get_index_from_bot_message(message):
    # Extracts index from: [ № index_number ]
    index = int(re.findall("\d", message.text)[0]) - 1
    return index

# ===============================================

bot.infinity_polling()
