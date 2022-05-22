from bot_commands.common import *
from date import (get_previous_date,
                  get_date_x_days_ago,
                  get_date_with_current_year)

def process_add_step(message, bot, db):
    try:
        assert_message_is_not_command(message)
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        record = get_record_from_message_and_db(message, db)

        # FIXME: get field name from config
        notify_dates = get_list_of_default_notify_dates(record["date"])
        record["notify_when"] = notify_dates

        db.add_new_record(message.chat.id, record)

        bot.send_message(message.chat.id, BotText.ADD_SUCCESS)#, \
                #reply_markup=gen_default_actions_markup())

        bot.send_message(message.chat.id, BotText.ADD_MORE)#, \
                #reply_markup=gen_default_actions_markup())

        bot.register_next_step_handler(message, process_add_step, bot, db)

    except MessageIsCommand:
        if (message.text == "/example"):
            # FIXME: DRY; same func as in main
            bot.send_message(message.chat.id, "Пример:\n" + get_example())
            bot.register_next_step_handler(message, process_add_step, bot, db)
        elif (message.text == "/cancel"):
            MessageIsCommand.cancel_add(message, default, bot, db)
        elif (message.text == "/show" or message.text == "/see"): # FIXME
            show(message, bot, db)
            bot.register_next_step_handler(message, process_add_step, bot, db)
        else:
            MessageIsCommand.add(message, default, bot, db)
    except MessageTooLarge:
        MessageTooLarge.default(message, process_add_step, bot, db)
    except NoNameInTheBeginning:
        NoNameInTheBeginning.default(message, process_add_step, bot, db)
    except NoDate:
        NoDate.default(message, process_add_step, bot, db)
    except InvalidNickname:
        InvalidNickname.default(message, process_add_step, bot, db)
    except RecordAlreadyExists:
        RecordAlreadyExists.default(message, process_add_step, bot, db)
    except Exception as e:
        uncaught_error(message, bot, e)

def show(message, bot, db):
    try:
        assert_user_has_records(message, db)

        records = db.get_user_records(message.chat.id)

        msg = []

        for i in range(len(records)):
            string = get_record_string(records[i], i)

            msg.append(string)

            if ((i + 1) > 0 and (i + 1) % 10 == 0 or i == (len(records) - 1)):
                bot.send_message(message.chat.id, "\n".join(msg))
                msg = []

    except UserHasNoRecords:
        UserHasNoRecords.default(message, bot, db)
    except NewUserHasNoRecords:
        NewUserHasNoRecords.default(message, bot, db)
    except Exception as e:
        uncaught_error(message, bot, e)
