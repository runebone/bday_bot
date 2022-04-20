from bot_commands.common import *

def process_edit_delete_step(message, bot, db):
    try:
        assert_user_has_records(message, db)

        bot.send_message(message.chat.id, BotText.CHOOSE_RECORD, \
                parse_mode="Markdown")

        # TODO: make code look more beautiful
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_output_string(records[i], i)
            bot.send_message(message.chat.id, string, \
                    reply_markup=gen_choose_edit_delete_record_markup())

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))
        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)

def process_confirm_deletion_step(message, bot, db):
    try:
        bot.send_message(message.chat.id, \
                BotText.YOU_HAVE_CHOSEN_TO_DELETE.format(message.text), \
                reply_markup=gen_confirm_deletion_markup(),
                parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))
        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)

def process_edit_step(message, bot, db):
    try:
        bot.send_message(message.chat.id, "test", reply_markup=gen_edit_record_markup())

    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))

        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)
