#!/usr/bin/python
import re
import sys
import telebot
import bot_commands as bc
from bot_commands.common import *
from config import *
from my_regex import *
from example import get_example
from init import bot, db
import threading
from notifications import notifications_job

# For callback functions
def get_database():
    return db

def get_bot():
    return bot

# ===============================================

@bot.message_handler(commands=["default", "help", "menu", "reset"])
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
            #reply_markup=gen_example_markup()
            )
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
            bot.edit_message_text(call.message.text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)

        elif call.data == "cb_edit_record":
            db = get_database()
            bc.edit_delete.process_edit_record_step(call.message, bot, db)
            bot.edit_message_text(call.message.text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)
        elif call.data == "cb_edit_name":
            db = get_database()
            bc.edit_delete.process_edit_name_step(call.message, bot, db)
            edited_message = re.sub(BotText.CHOOSE_FIELD_TO_EDIT, "",
                                    call.message.text)
            bot.edit_message_text(edited_message,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)
        elif call.data == "cb_edit_date":
            db = get_database()
            bc.edit_delete.process_edit_date_step(call.message, bot, db)
            edited_message = re.sub(BotText.CHOOSE_FIELD_TO_EDIT, "",
                                    call.message.text)
            bot.edit_message_text(edited_message,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)
        elif call.data == "cb_edit_nickname":
            db = get_database()
            bc.edit_delete.process_edit_nickname_step(call.message, bot, db)
            edited_message = re.sub(BotText.CHOOSE_FIELD_TO_EDIT, "",
                                    call.message.text)
            bot.edit_message_text(edited_message,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)
        elif call.data == "cb_edit_phone":
            db = get_database()
            bc.edit_delete.process_edit_phone_step(call.message, bot, db)
            edited_message = re.sub(BotText.CHOOSE_FIELD_TO_EDIT, "",
                                    call.message.text)
            bot.edit_message_text(edited_message,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)
        elif call.data == "cb_input_again":
            db = get_database()
            bc.edit_delete.process_input_again_step(call.message, bot, db)
            edited_message = re.sub(BotText.CHOOSE_FIELD_TO_EDIT, "",
                                    call.message.text)
            bot.edit_message_text(edited_message,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=None)

        elif call.data == "cb_confirm_deletion":
            db = get_database()

            record = get_record_from_output_message_text_and_db(call.message.text, db)

            db.delete_record_by_record(call.message.chat.id, record)
            bot.send_message(call.message.chat.id, BotText.DELETE_SUCCESS)
            default(call.message)
        elif call.data == "cb_edit":
            bot.send_message(call.message.chat.id, "Edit.")
            index = get_index_from_bot_message(call.message)

        elif call.data == "cb_thanks":
            bot.edit_message_text(call.message.text,
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=None)
            bot.send_message(call.message.chat.id, "Пожалуйста. 😊")

        # XXX
        elif call.data == "cb_remind_later":
            bot.edit_message_text(call.message.text,
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=None)

            x_hours = 3

            db = get_database()

            date = get_current_date_in_x_hours(x_hours)

            db.create_new_single_notification(call.message.chat.id,
                                              date, call.message.text)

            bot.send_message(call.message.chat.id, "Напомню через 3 часа. 👌")

    except RecordNotFound:
        bot.send_message(call.message.chat.id, FailText.RecordNotFound)
        bot.register_next_step_handler(call.message, \
                bc.edit_delete.process_edit_delete_step, bot, db)
    except Exception as e:
        uncaught_error(call.message, bot, e)

# ===============================================

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("menu", "вызвать интерактивное меню"),
        telebot.types.BotCommand("add", "добавить новую запись"),
        telebot.types.BotCommand("show", "показать текущие записи"),
        telebot.types.BotCommand("edit", "вызвать меню изменения/удаления записей"),
        telebot.types.BotCommand("example", "получить пример правильной записи")
    ],
    scope=telebot.types.BotCommandScopeAllPrivateChats()
)

notification_thread = threading.Thread(target=notifications_job,
                                       args=[bot, db])
notification_thread.start()

bot.infinity_polling()
