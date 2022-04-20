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

        bot.send_message(message.chat.id, BotText.CHANGED_MIND, \
                reply_markup=gen_cancel_markup())

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords, \
                reply_markup=gen_add_friend_markup())
    except Exception as e:
        uncaught_error(message, bot, e)

def process_confirm_deletion_step(message, bot, db):
    try:
        bot.send_message(message.chat.id, \
                BotText.YOU_HAVE_CHOSEN_TO_DELETE.format(message.text), \
                reply_markup=gen_confirm_deletion_markup(),
                parse_mode="Markdown")
    except Exception as e:
        uncaught_error(message, bot, e)

# TODO: text = BotText... everywhere
def process_edit_record_step(message, bot, db):
    try:
        text = BotText.YOU_HAVE_CHOSEN_TO_EDIT.format(message.text)
        text += "\n\n"
        text += BotText.CHOOSE_FIELD_TO_EDIT
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_edit_record_markup(),
                parse_mode="Markdown")

    except Exception as e:
        uncaught_error(message, bot, e)

# ==================================================
# Process editing fields
# ==================================================

def process_edit_name_step(message, bot, db):
    try:
        text = BotText.NAME_INPUT_OFFER
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_cancel_markup(),
                parse_mode="Markdown")

        record = get_record_from_output_message_text_and_db(message.text, db)
        index = db.get_record_index_by_record(message.chat.id, record)

        bot.register_next_step_handler(message, process_input_name_step, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_input_name_step(message, bot, db, record, index):
    try:
        # TODO: assert message is not too large
        # TODO: assert message has name

        name = message.text
        record["name"] = name

        process_update_name_step(message, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_update_name_step(message, bot, db, record, index):
    try:
        db.update_record_by_index(message.chat.id, record, index)
        text = BotText.EDIT_SUCCESS
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        process_edit_delete_step(message, bot, db)

    except Exception as e:
        uncaught_error(message, bot, e)

# ==================================================

def process_edit_date_step(message, bot, db):
    try:
        text = BotText.DATE_INPUT_OFFER
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_cancel_markup(),
                parse_mode="Markdown")

        record = get_record_from_output_message_text_and_db(message.text, db)
        index = db.get_record_index_by_record(message.chat.id, record)

        bot.register_next_step_handler(message, process_input_date_step, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_input_date_step(message, bot, db, record, index):
    try:
        # TODO: asserts

        date = get_date_from_message(message.text)
        date = normalize_date(date)
        date = normal_date_to_usa_format(date)
        record["date"] = date

        process_update_date_step(message, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_update_date_step(message, bot, db, record, index):
    try:
        db.update_record_by_index(message.chat.id, record, index)
        text = BotText.EDIT_SUCCESS
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        process_edit_delete_step(message, bot, db)

    except Exception as e:
        uncaught_error(message, bot, e)

# ==================================================

def process_edit_nickname_step(message, bot, db):
    try:
        text = BotText.NICKNAME_INPUT_OFFER
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_cancel_markup(),
                parse_mode="Markdown")

        record = get_record_from_output_message_text_and_db(message.text, db)
        index = db.get_record_index_by_record(message.chat.id, record)

        bot.register_next_step_handler(message, process_input_nickname_step, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_input_nickname_step(message, bot, db, record, index):
    try:
        # TODO: asserts

        nickname = get_nickname_from_message(message.text)
        record["nickname"] = nickname[1:] # TODO: regex extract without @; fix main logic

        process_update_nickname_step(message, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_update_nickname_step(message, bot, db, record, index):
    try:
        db.update_record_by_index(message.chat.id, record, index)
        text = BotText.EDIT_SUCCESS
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        process_edit_delete_step(message, bot, db)

    except Exception as e:
        uncaught_error(message, bot, e)

# ==================================================

def process_edit_phone_step(message, bot, db):
    try:
        text = BotText.PHONE_INPUT_OFFER
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_cancel_markup(),
                parse_mode="Markdown")

        record = get_record_from_output_message_text_and_db(message.text, db)
        index = db.get_record_index_by_record(message.chat.id, record)

        bot.register_next_step_handler(message, process_input_phone_step, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_input_phone_step(message, bot, db, record, index):
    try:
        # TODO: asserts

        phone = get_phone_from_message(message.text)
        phone = normalize_phone(phone)
        record["phone"] = phone

        process_update_phone_step(message, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_update_phone_step(message, bot, db, record, index):
    try:
        db.update_record_by_index(message.chat.id, record, index)
        text = BotText.EDIT_SUCCESS
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        process_edit_delete_step(message, bot, db)

    except Exception as e:
        uncaught_error(message, bot, e)

# ==================================================

def process_input_again_step(message, bot, db):
    try:
        text = BotText.INPUT_AGAIN_OFFER
        bot.send_message(message.chat.id, text, \
                reply_markup=gen_cancel_markup(),
                parse_mode="Markdown")

        record = get_record_from_output_message_text_and_db(message.text, db)
        index = db.get_record_index_by_record(message.chat.id, record)

        bot.register_next_step_handler(message, process_input_again_input_step, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

# FIXME: rename these functions
def process_input_again_input_step(message, bot, db, record, index):
    try:
        assert_message_is_not_command(message)
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        record = get_record_from_message_and_db(message, db)

        process_update_record_step(message, bot, db, record, index)

    except Exception as e:
        uncaught_error(message, bot, e)

def process_update_record_step(message, bot, db, record, index):
    try:
        db.update_record_by_index(message.chat.id, record, index)
        text = BotText.EDIT_SUCCESS
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        process_edit_delete_step(message, bot, db)

    except Exception as e:
        uncaught_error(message, bot, e)
