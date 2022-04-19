from my_regex import *
from config import *

def process_add_step(message, bot, db):
    try:
        assert_message_has_valid_length(message)
        assert_message_has_name_in_the_beginning(message)
        assert_message_has_date(message)

        record = db.sample_record

        name = get_name_from_message(message.text)
        msg = remove_parsed_data_from_message(message.text, name)
        record["name"] = name

        date = get_date_from_message(msg)
        msg = remove_parsed_data_from_message(msg, date)
        date = normalize_date(date)
        date = normal_date_to_usa_format(date)
        record["date"] = date

        if (message_has_at_sign(message)):
            if (message_has_nickname(message)):
                nickname = get_nickname_from_message(msg)
                msg = remove_parsed_data_from_message(msg, nickname)
                record["nickname"] = nickname[1:] # Store nickname without @
            else:
                raise InvalidNickname

        if (message_has_phone(message)):
            phone = get_phone_from_message(msg)
            msg = remove_parsed_data_from_message(msg, phone)
            phone = normalize_phone(phone)
            record["phone"] = phone

        db.add_new_record(message.chat.id, record)

        bot.send_message(message.chat.id, BotText.ADD_SUCCESS)

    # FIXME: DRY
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
        bot.send_message(message.chat.id, FailText.UncaughtError.format(str(e)))

def assert_message_has_valid_length(message):
    if (len(message.text) > Const.MAX_MESSAGE_LENGTH):
        raise MessageTooLarge

def assert_message_has_name_in_the_beginning(message):
    name = get_name_from_message(message.text)
    if (name == None):
        raise NoNameInTheBeginning

def assert_message_has_date(message):
    date = get_date_from_message(message.text)
    if (date == None):
        raise NoDate

def message_has_at_sign(message):
    if (re.findall("@", message.text) == []):
        return False
    return True

def message_has_nickname(message):
    nickname = get_nickname_from_message(message.text)
    if (nickname == None):
        return False
    return True

def message_has_phone(message):
    phone = get_phone_from_message(message.text)
    if (phone == None):
        return False
    return True

def remove_parsed_data_from_message(message_string, data):
    return re.sub(data, "", message_string, count=1)
    # return "".join(message_string.split(data)) # BUG: 1 12-12-2001; replaces 1s in date
