from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from my_regex import *
from config import *
import sys

def message_is_command(message):
    commands = [
            "start", "help",
            "add",
            "delete", "cut",
            "show", "see",
            "edit", "change",
            "cancel"
            ]
    commands = list(map(lambda word: "/" + word, commands))

    if (message.text in commands):
        return True
    return False

def get_output_string(record, index):
    date = us_date_to_ru_format(record["date"])

    format_string = []
    format_string.append(BotText.output["index"].format(index + 1))
    format_string.append(BotText.output["name"].format(record["name"]))
    format_string.append(BotText.output["date"].format(date))

    if (record["nickname"] != None):
        format_string.append(\
                BotText.output["nickname"].format(record["nickname"]))
    if (record["phone"] != None):
        phone = beautify_phone(record["phone"])
        format_string.append(BotText.output["phone"].format(phone))

    format_string = "\n".join(format_string)

    return format_string

def gen_edit_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Изменить", callback_data="cb_edit"), \
            InlineKeyboardButton("Удалить", callback_data="cb_delete"))
    return markup

def gen_add_friend_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить друга", \
            callback_data="cb_add_friend"))
    return markup

def gen_default_actions_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавить друга", \
                callback_data="cb_add_command"),
            InlineKeyboardButton("Посмотреть список",
                callback_data="cb_show_command"),
            InlineKeyboardButton("Изменить",
                callback_data="cb_edit_command"),
            InlineKeyboardButton("Удалить",
                callback_data="cb_delete_command"))
    return markup

def assert_user_has_records(message, db):
    records = db.get_user_records(message.chat.id)
    if (len(records) == 0):
        raise UserHasNoRecords
