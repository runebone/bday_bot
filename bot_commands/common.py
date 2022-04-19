from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from my_regex import *
from config import *
import sys

def message_text_is_command(message_text):
    commands = [
            "start", "help"
            "add",
            "delete", "cut",
            "show", "see",
            "edit", "change"
            "cancel"
            ]
    commands = map(lambda word: "/" + word, commands)

    if (message_text in commands):
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
