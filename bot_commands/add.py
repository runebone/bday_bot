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

        time = Config.DEFAULT_NOTIFICATION_TIME

        # FIXME: get field name from config
        bday = get_date_with_current_year(record["date"])

        day_before_bday = get_previous_date(bday)
        week_before_bday = get_date_x_days_ago(bday, 7)

        notify_dates = list(map(lambda x: " ".join([x, time]),
                                [bday, week_before_bday, day_before_bday]))

        # FIXME: get field name from config
        record["notify_when"] = notify_dates

        db.add_new_record(message.chat.id, record)

        bot.send_message(message.chat.id, BotText.ADD_SUCCESS, \
                reply_markup=gen_default_actions_markup())

    except MessageIsCommand:
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
