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

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords)
        bot.register_next_step_handler(message, process_delete_step, bot, db)
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords)
        bot.register_next_step_handler(message, process_delete_step, bot, db)
    except RecordIndexOutOfRange:
        bot.send_message(message.chat.id, FailText.RecordIndexOutOfRange)
        bot.register_next_step_handler(message, process_delete_step, bot, db)
    except Exception as e:
        bot.send_message(message.chat.id, FailText.UncaughtError.format(str(e)))
