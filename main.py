#!/usr/bin/python
import telebot
from my_regex import *
from config import BotText
from errors import *
from db import Database

# TODO: Сделать клаву с командами, чтобы бабки могли пользоваться

# Get API token
with open(".API_TOKEN") as f:
    API_TOKEN = f.readline()[:-1]

bot = telebot.TeleBot(API_TOKEN)

# const.py ===============================================
class Const: # TODO: from const.py import *; remove Const class
    MAX_MESSAGE_LENGTH = 256

# ===============================================

@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, BotText.START.value)
    bot.send_message(message.chat.id, message.chat.id)
    bot.send_message(message.chat.id, type(message.chat.id))

@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(message.chat.id, BotText.ADD.value)
    #bot.register_next_step_handler(message, process_add_step)

@bot.message_handler(commands=["delete", "cut"])
def delete(message):
    bot.send_message(message.chat.id, BotText.DELETE.value)
    #bot.register_next_step_handler(message, process_delete_step)

@bot.message_handler(commands=["show", "see"])
def show(message):
    bot.send_message(message.chat.id, BotText.SHOW.value)
    #bot.register_next_step_handler(message, process_show_step)

@bot.message_handler(commands=["edit", "change"])
def edit(message):
    bot.send_message(message.chat.id, BotText.EDIT.value)
    #bot.register_next_step_handler(message, process_edit_step)

# === PROCESS_ADD_STEP
def process_add_step(message):
    try:
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        # name -> database
        # date -> normalize -> database

        if (message_has_at_sign(message)):
            if (message_has_nickname(message)):
                pass
                # nickname -> database
            else:
                raise InvalidNickname

        if (message_has_phone(message)):
            pass
            # phone -> normalize -> beautify -> database

    except Exception as e:
        bot.send_message(message.chat.id, e.text)

def assert_message_has_valid_length(message):
    if (len(message.text) > Const.MAX_MESSAGE_LENGTH):
        raise MessageTooLarge

def assert_message_has_name_in_the_beginning(message):
    name = get_name_from_message(message.text)
    if (name == None):
        raise NoNameInTheBeginning

def assert_message_has_date(message):
    date = get_date_from_message(message.text)
    if (date == None):
        raise NoDate

def message_has_at_sign(message):
    if (re.findall("@", message.text) == []):
        return False
    return True

def message_has_nickname(message):
    nickname = get_nickname_from_message(message.text)
    if (nickname == None):
        return False
    return True

def message_has_phone(message):
    phone = get_phone_from_message(message.text)
    if (phone == None):
        return False
    return True
# === END OF PROCESS_ADD_STEP

def process_delete_step(message):
    pass

def process_show_step(message):
    pass

def process_edit_step(message):
    pass

# ===============================================
bot.polling() # Keeps checking for messages
