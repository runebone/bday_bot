from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_commands.common import *

def gen_edit_record_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Изменить", \
            callback_data="cb_edit_record"), \
            InlineKeyboardButton("Удалить", \
            callback_data="cb_delete_record"))
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
            InlineKeyboardButton("Изменить / Удалить",
                callback_data="cb_delete_command"))
    return markup

def gen_confirm_deletion_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Отмена", \
                callback_data="cb_cancel"),
            InlineKeyboardButton("Подтвердить удаление",
                callback_data="cb_confirm_deletion"))
    return markup

def gen_example_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Пример", \
            callback_data="cb_example_command"))
    return markup
