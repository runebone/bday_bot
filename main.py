#!/usr/bin/python
import re
import sys
import telebot
import bot_commands as bc
from bot_commands.common import *
from db import Database
from config import *
from my_regex import *
from example import get_example

# Get API token
with open(".API_TOKEN") as f:
    API_TOKEN = f.readline()[:-1]

# Initialize database; global constant
db = Database(Config.Database.file)

# Initialize bot; global constant
bot = telebot.TeleBot(API_TOKEN)

# For callback functions
def get_database():
    return db

def get_bot():
    return bot

# ===============================================

@bot.message_handler(commands=["default", "help"])
@bot.message_handler(func=lambda message: not message_is_command(message))
def default(message):
    bot.send_message(message.chat.id, BotText.CHOOSE_ACTION,\
            reply_markup=gen_default_actions_markup())

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, BotText.START, \
            parse_mode="Markdown", \
            reply_markup=gen_add_friend_markup())

@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(message.chat.id, BotText.ADD, \
            parse_mode="Markdown", \
            reply_markup=gen_example_markup())
    bot.register_next_step_handler(message, bc.add.process_add_step, bot, db)

@bot.message_handler(commands=["delete", "cut", "edit", "change"])
def edit_delete(message):
    bc.edit_delete.process_edit_delete_step(message, bot, db)

@bot.message_handler(commands=["show", "see"])
def show(message):
    bc.show.process_show_step(message, bot, db)

@bot.message_handler(commands=["example"])
def example(message):
    bot.send_message(message.chat.id, "Пример:\n" + get_example())

# Callbacks for all functions
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "cb_cancel":
            default(call.message)
        elif call.data == "cb_add_command":
            add(call.message)
        elif call.data == "cb_show_command":
            show(call.message)
        elif call.data == "cb_edit_delete_command":
            edit_delete(call.message)
        elif call.data == "cb_example_command":
            example(call.message)

        elif call.data == "cb_delete_record":
            db = get_database()
            bc.edit_delete.process_confirm_deletion_step(call.message, bot, db)

        elif call.data == "cb_edit_record":
            db = get_database()
            bc.edit_delete.process_edit_record_step(call.message, bot, db)
        elif call.data == "cb_edit_name":
            db = get_database()
            bc.edit_delete.process_edit_name_step(call.message, bot, db)
        elif call.data == "cb_edit_date":
            db = get_database()
            bc.edit_delete.process_edit_date_step(call.message, bot, db)
        elif call.data == "cb_edit_nickname":
            db = get_database()
            bc.edit_delete.process_edit_phone_step(call.message, bot, db)
        elif call.data == "cb_edit_phone":
            db = get_database()
            bc.edit_delete.process_edit_record_step(call.message, bot, db)
        elif call.data == "cb_input_again":
            db = get_database()
            bc.edit_delete.process_input_again_step(call.message, bot, db)

        elif call.data == "cb_confirm_deletion":
            db = get_database()

            record = get_record_from_output_message_text(call.message.text)

            db.delete_record_by_record(call.message.chat.id, record)
            bot.send_message(call.message.chat.id, BotText.DELETE_SUCCESS)
            default(call.message)
        elif call.data == "cb_edit":
            bot.send_message(call.message.chat.id, "Edit.")
            index = get_index_from_bot_message(call.message)

    except RecordNotFound:
        bot.send_message(call.message.chat.id, FailText.RecordNotFound)
        bot.register_next_step_handler(call.message, \
                bc.edit_delete.process_edit_delete_step, bot, db)
    except Exception as e:
        bot.send_message(call.message.chat.id, \
                FailText.UncaughtError.format(str(e)))

        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)

def get_record_from_output_message_text(message_text):
    db = get_database()

    name = get_name_from_output_message_text(message_text)

    date = get_date_from_message(message_text)
    date = normal_date_to_usa_format(date)

    nickname = get_nickname_from_message(message_text)
    if (nickname != None): nickname = nickname[1:]

    phone = get_phone_from_message(call.message.text)
    if (phone != None): phone = normalize_phone(phone)

    record = dict(db.sample_record)
    record["name"] = name
    record["date"] = date
    record["nickname"] = nickname
    record["phone"] = phone

    return record

def get_name_from_output_message_text(message_text):
    pattern = "(?:Имя: )([^\n]*)"
    name = re.findall(pattern, message_text)[0]
    return name

# ===============================================

bot.infinity_polling()
