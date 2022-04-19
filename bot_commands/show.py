from bot_commands.common import *

def process_show_step(message, bot, db):
    try:
        assert_user_has_records(message, db)

        records = db.get_user_records(message.chat.id)

        for i in range(len(records)):
            string = get_output_string(records[i], i)
            bot.send_message(message.chat.id, string)

        # Choose action
        bot.send_message(message.chat.id, BotText.CHOOSE_ACTION, \
                reply_markup=gen_default_actions_markup())

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords)
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords)
    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))

        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)
