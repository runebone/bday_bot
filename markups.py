from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_commands.common import *

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
            callback_data="cb_add_command"))
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
