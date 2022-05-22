from my_regex import *
from config import *
from markups import *
from date import *
from example import *
import sys
import traceback

# FIXME: copied from main.py to use in add; idk yet how to fix it
def default(message, bot, *args, **kwargs):
    bot.send_message(message.chat.id, BotText.CHOOSE_ACTION,\
            reply_markup=gen_default_actions_markup())

def send_debug_info_to_dev(message, bot):
    dbg = "*Uncaught error from:* {} (@{})\n\n*Message:* {}\n\n{}".format(message.chat.id, message.chat.username, message.text, traceback.format_exc())
    bot.send_message(DEVELOPER_CHAT_ID, dbg, parse_mode="Markdown")

def uncaught_error(message, bot, exception):
    send_debug_info_to_dev(message, bot)
    bot.send_message(message.chat.id, \
            FailText.UncaughtError.format(str(exception)))
    raise_traceback(exception)

def raise_traceback(exception):
    tb = sys.exc_info()[2]
    raise exception.with_traceback(tb)

def message_is_command(message):
    commands = [
            "start", "help",
            "add",
            "delete", "cut",
            "show", "see",
            "edit", "change",
            "cancel", "reset", # XXX
            "example",
            "default", "menu"
            ]
    commands = list(map(lambda word: "/" + word, commands))

    if (message.text in commands):
        return True
    return False

def get_output_string(record, index):
    date = us_date_to_ru_format(record["date"])

    format_string = []
    format_string.append(BotText.output["index"].format(index + 1))
    format_string.append(BotText.output["name"].format(record["name"]))
    format_string.append(BotText.output["date"].format(date))

    if (record["nickname"] != None):
        format_string.append(\
                BotText.output["nickname"].format(record["nickname"]))
    if (record["phone"] != None):
        phone = beautify_phone(record["phone"])
        format_string.append(BotText.output["phone"].format(phone))

    format_string = "\n".join(format_string)

    return format_string

def get_record_string(record, index):
    date = us_date_to_ru_format(record["date"])

    fmt_string = []
    fmt_string.append(f"{index + 1}.")
    fmt_string.append(record["name"])
    fmt_string.append("--")
    fmt_string.append(date)

    if (record["nickname"] != None and record["phone"] != None):
        fmt_string.append(f"(@{record['nickname']}, {record['phone']})")
    elif (record["nickname"] != None):
        fmt_string.append(f"(@{record['nickname']})")
    elif (record["phone"] != None):
        fmt_string.append(f"({record['phone']})")

    fmt_string = " ".join(fmt_string)

    return fmt_string

def assert_user_has_records(message, db):
    records = db.get_user_records(message.chat.id)
    if (len(records) == 0):
        raise UserHasNoRecords

def get_record_from_output_message_text_and_db(message_text, db):
    name = get_name_from_output_message_text(message_text)

    date = get_date_from_output_message_text(message_text)
    date = normal_date_to_usa_format(date)

    nickname = get_nickname_from_output_message_text(message_text)

    phone = get_phone_from_output_message_text(message_text)
    if (phone): phone = normalize_phone(phone) #TODO: normalize <- accept None

    record = dict(db.sample_record)
    record["name"] = name
    record["date"] = date
    record["nickname"] = nickname
    record["phone"] = phone

    return record

def get_name_from_output_message_text(message_text):
    name_header = BotText.output["name"].split("{}")[0]
    pattern = f"(?:{name_header})([^\n]*)"
    name = re.findall(pattern, message_text)
    if (name): name = name[0]
    else: name = None
    return name

def get_date_from_output_message_text(message_text):
    date_header = BotText.output["date"].split("{}")[0]
    pattern = f"(?:{date_header})([^\n]*)"
    date = re.findall(pattern, message_text)
    if (date): date = date[0]
    else: date = None
    return date

def get_nickname_from_output_message_text(message_text):
    nickname_header = BotText.output["nickname"].split("{}")[0]
    pattern = f"(?:{nickname_header})([^\n]*)"
    nickname = re.findall(pattern, message_text)
    if (nickname): nickname = nickname[0]
    else: nickname = None
    return nickname

def get_phone_from_output_message_text(message_text):
    phone_header = BotText.output["phone"].split("{}")[0]
    pattern = f"(?:{phone_header})([^\n]*)"
    phone = re.findall(pattern, message_text)
    if (phone): phone = phone[0]
    else: phone = None
    return phone

# =================================================

def get_record_from_message_and_db(message, db):
    # Don't interpret record and db.sample_record as the same thing
    record = dict(db.sample_record)

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

    return record

def get_list_of_default_notify_dates(db_date):
    time = Config.DEFAULT_NOTIFICATION_TIME

    bday = get_date_with_current_year(db_date)
    day_before_bday = get_previous_date(bday)
    week_before_bday = get_date_x_days_ago(bday, 7)

    notify_dates = list(map(lambda x: " ".join([x, time]),
                            [bday, week_before_bday, day_before_bday]))
    return notify_dates

def assert_message_is_not_command(message):
    if (message_is_command(message)):
        raise MessageIsCommand

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
    return re.sub(r"{data}", "", message_string, count=1)

# =================================================

def assert_message_has_nickname(message):
    nickname = get_nickname_from_message(message.text)
    if (nickname == None):
        raise NoNickname

def assert_message_has_phone(message):
    phone = get_phone_from_message(message.text)
    if (phone == None):
        raise NoPhone
