#!/usr/bin/python
import telebot
import pandas as pd
from my_regex import *
from config import *
from db import Database
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize database
db = Database()

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
    bot.send_message(message.chat.id, BotText.START)
    bot.send_message(message.chat.id, message.chat.id)
    bot.send_message(message.chat.id, type(message.chat.id))

@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(message.chat.id, BotText.ADD)
    bot.register_next_step_handler(message, process_add_step)

@bot.message_handler(commands=["delete", "cut"])
def delete(message):
    #bot.send_message(message.chat.id, BotText.DELETE)
    process_delete_step(message)
    #bot.register_next_step_handler(message, process_delete_step)

@bot.message_handler(commands=["show", "see"])
def show(message):
    process_show_step(message)

@bot.message_handler(commands=["edit", "change"])
def edit(message):
    bot.send_message(message.chat.id, BotText.EDIT)
    #bot.register_next_step_handler(message, process_edit_step)

# === PROCESS_ADD_STEP
def process_add_step(message):
    try:
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        record = db.sample_record

        name = get_name_from_message(message.text)
        msg = remove_parsed_data_from_message(message.text, name)
        record["name"] = name

        date = get_date_from_message(msg)
        msg = remove_parsed_data_from_message(msg, date)
        date = normalize_date(date)
        date = normal_date_to_usa_format(date)
        record["date"] = date

        if (message_has_at_sign(message)):
            if (message_has_nickname(message)):
                nickname = get_nickname_from_message(msg)
                msg = remove_parsed_data_from_message(msg, nickname)
                record["nickname"] = nickname[1:] # Store nickname without @
            else:
                raise InvalidNickname

        if (message_has_phone(message)):
            phone = get_phone_from_message(msg)
            msg = remove_parsed_data_from_message(msg, phone)
            phone = normalize_phone(phone)
            record["phone"] = phone

        db.add_new_record(message.chat.id, record)

        bot.send_message(message.chat.id, BotText.ADD_SUCCESS)

    except Exception as e:
        bot.send_message(message.chat.id, e.text)
        bot.register_next_step_handler(message, process_add_step)

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

def remove_parsed_data_from_message(message_string, data):
    return "".join(message_string.split(data))

# === END OF PROCESS_ADD_STEP

# === PROCESS_DELETE_STEP XXX
def process_delete_step(message):
    try:
        # TODO: some asserts (user has records)
        # TODO: get index from user
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_printable_string_from_record(records[i], i)
            bot.send_message(message.chat.id, string, reply_markup=gen_edit_markup())
    except Exception as e:
        bot.send_message(message.chat.id, e.text)
        bot.register_next_step_handler(message, process_delete_step)

def gen_edit_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Изменить", callback_data="cb_edit"), InlineKeyboardButton("Удалить", callback_data="cb_delete"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_edit":
        bot.send_message(call.message.chat.id, "Edit.")
        index = get_index_from_bot_message(call.message)
    elif call.data == "cb_delete":
        index = get_index_from_bot_message(call.message)
        db.delete_record_by_index(call.message.chat.id, index)
        bot.send_message(call.message.chat.id, "Deleted.")

def get_index_from_bot_message(message):
    # Extracts index from: [ № index_number ]
    index = int(re.findall("\d", message.text)[0]) - 1
    return index

# === END OF PROCESS_DELETE_STEP

# === PROCESS_SHOW_STEP
# FIXME: clean-up this shit
def process_show_step(message):
    try:
        # TODO: some asserts (user has records)
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_printable_string_from_record(records[i], i)
            bot.send_message(message.chat.id, string)

    except Exception as e:
        bot.send_message(message.chat.id, e.text)
        bot.register_next_step_handler(message, process_show_step)

def get_printable_string_from_record(record, index):
    date = us_date_to_ru_format(record["date"])

    format_string = f"[ №{index + 1} ]\n"
    format_string += f"Имя: {record['name']}\n"
    format_string += f"Дата рождения: {date}\n"

    if (record["nickname"] != None):
        format_string += f"Никнейм: @{record['nickname']}\n"
    if (record["phone"] != None):
        phone = beautify_phone(record["phone"])
        format_string += f"Номер телефона: {phone}"

    return format_string

def us_date_to_ru_format(date):
    date = date.split("-")
    date[0], date[1] = date[1], date[0]
    date = ".".join(date)
    return date

# === END OF PROCESS_SHOW_STEP

# === PROCESS_EDIT_STEP
def process_edit_step(message):
    try:
        pass
    except Exception as e:
        bot.send_message(message.chat.id, e.text)
        bot.register_next_step_handler(message, process_edit_step)
# === END OF PROCESS_EDIT_STEP

# ===============================================
bot.infinity_polling() # Keeps checking for messages
