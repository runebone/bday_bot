from config import *
from bot_commands.show import get_printable_string_from_record
from bot_commands.edit import gen_edit_markup

def process_delete_step(message, bot, db):
    try:
        # TODO: some asserts (user has records)
        # TODO: get index from user
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_printable_string_from_record(records[i], i)
            bot.send_message(message.chat.id, string, \
                    reply_markup=gen_edit_markup())
    except Exception as e:
        bot.send_message(message.chat.id, e.text)
        bot.register_next_step_handler(message, process_delete_step, bot, db)
