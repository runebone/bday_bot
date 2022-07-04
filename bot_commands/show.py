from bot_commands.common import *

def process_show_step(message, bot, db):
    try:
        assert_user_has_records(message, db)

        records = db.get_user_records(message.chat.id)

        msg = []

        for i in range(len(records)):
            string = get_record_string(records[i], i)

            msg.append(string)

            if ((i + 1) > 0 and (i + 1) % 100 == 0 or i == (len(records) - 1)):
                bot.send_message(message.chat.id, "\n".join(msg))
                msg = []

        # Choose action
        bot.send_message(message.chat.id, BotText.CHOOSE_ACTION, \
                reply_markup=gen_default_actions_markup())

    except UserHasNoRecords:
        UserHasNoRecords.default(message, bot, db)
    except NewUserHasNoRecords:
        NewUserHasNoRecords.default(message, bot, db)
    except Exception as e:
        uncaught_error(message, bot, e)
