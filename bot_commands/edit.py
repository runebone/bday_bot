from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

def process_edit_step(message, bot, db):
    try:
        pass

    except Exception as e:
        bot.send_message(message.chat.id, FailText.UncaughtError.format(str(e)))

def gen_edit_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Изменить", callback_data="cb_edit"), \
            InlineKeyboardButton("Удалить", callback_data="cb_delete"))
    return markup
