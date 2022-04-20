from bot_commands.common import *

def process_add_step(message, bot, db):
    try:
        assert_message_is_not_command(message)
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        record = get_record_from_message_and_db(message, db)

        db.add_new_record(message.chat.id, record)

        bot.send_message(message.chat.id, BotText.ADD_SUCCESS, \
                reply_markup=gen_default_actions_markup())

    # FIXME: DRY
    except MessageIsCommand:
        bot.send_message(message.chat.id, "Вы вышли из режима добавления. Введите команду {} повторно, чтобы исполнить её.".format(message.text))
        default(message, bot)
    except MessageTooLarge:
        bot.send_message(message.chat.id, FailText.MessageTooLarge)
        bot.register_next_step_handler(message, process_add_step, bot, db)
    except NoNameInTheBeginning:
        bot.send_message(message.chat.id, FailText.NoNameInTheBeginning)
        bot.register_next_step_handler(message, process_add_step, bot, db)
    except NoDate:
        bot.send_message(message.chat.id, FailText.NoDate)
        bot.register_next_step_handler(message, process_add_step, bot, db)
    except InvalidNickname:
        bot.send_message(message.chat.id, FailText.InvalidNickname)
        bot.register_next_step_handler(message, process_add_step, bot, db)
    except RecordAlreadyExists:
        bot.send_message(message.chat.id, FailText.RecordAlreadyExists)
        bot.register_next_step_handler(message, process_add_step, bot, db)
    except Exception as e:
        uncaught_error(message, bot, e)
