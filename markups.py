from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_commands.common import *

def gen_choose_edit_delete_record_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    IKB = InlineKeyboardButton

    edit = IKB("Изменить", callback_data="cb_edit_record")
    delete = IKB("Удалить", callback_data="cb_delete_record")

    markup.add(edit, delete)

    return markup

def gen_edit_record_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4

    IKB = InlineKeyboardButton

    name = IKB("Имя", callback_data="cb_edit_name")
    date = IKB("Дата", callback_data="cb_edit_date")
    nickname = IKB("Никнейм", callback_data="cb_edit_nickname")
    phone = IKB("Телефон", callback_data="cb_edit_phone")
    cancel = IKB("Отмена", callback_data="cb_cancel")
    input_again = IKB("Ввести заново", callback_data="cb_input_again")

    markup.add(name, date, nickname, phone, cancel, input_again)

    return markup

# TODO: Button names -> config
def gen_add_friend_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    IKB = InlineKeyboardButton

    add_friend = IKB("Добавить друга", callback_data="cb_add_command")

    markup.add(add_friend)

    return markup

def gen_default_actions_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    IKB = InlineKeyboardButton

    add_friend = IKB("Добавить друга", callback_data="cb_add_command")
    show = IKB("Посмотреть список", callback_data="cb_show_command")
    # TODO: rename delete callback command
    edit_delete = IKB("Изменить / Удалить", callback_data="cb_delete_command")

    markup.add(add_friend, show, edit_delete)

    return markup

def gen_confirm_deletion_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    IKB = InlineKeyboardButton

    cancel = IKB("Отмена", callback_data="cb_cancel")
    c_del = IKB("Подтвердить удаление", callback_data="cb_confirm_deletion")

    markup.add(cancel, c_del)

    return markup

def gen_example_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    IKB = InlineKeyboardButton

    cancel = IKB("Отмена", callback_data="cb_cancel")
    example = IKB("Пример", callback_data="cb_example_command")

    markup.add(cancel, example)

    return markup
