from bot_commands.common import *

def process_show_step(message, bot, db):
    try:
        # TODO: some asserts (user has records)
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_output_string(records[i], i)
            bot.send_message(message.chat.id, string)

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords)
        bot.register_next_step_handler(message, process_show_step, bot, db)
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords)
        bot.register_next_step_handler(message, process_show_step, bot, db)
    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))

        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)
