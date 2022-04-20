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
        bot.send_message(message.chat.id, FailText.UserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except Exception as e:
        uncaught_error(message, bot, e)
