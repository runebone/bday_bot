from my_regex import *
from config import *
from markups import *
import sys

# FIXME: copied from main.py to use in add; idk yet how to fix it
def default(message, bot):
    bot.send_message(message.chat.id, BotText.CHOOSE_ACTION,\
            reply_markup=gen_default_actions_markup())

def message_is_command(message):
    commands = [
            "start", "help",
            "add",
            "delete", "cut",
            "show", "see",
            "edit", "change",
            "cancel",
            "example"
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

def assert_user_has_records(message, db):
    records = db.get_user_records(message.chat.id)
    if (len(records) == 0):
        raise UserHasNoRecords

def get_record_from_output_message_text(message_text, db):
    name = get_name_from_output_message_text(message_text)

    date = get_date_from_message(message_text)
    date = normal_date_to_usa_format(date)

    nickname = get_nickname_from_message(message_text)
    if (nickname != None): nickname = nickname[1:]

    phone = get_phone_from_message(message_text)
    if (phone != None): phone = normalize_phone(phone)

    record = dict(db.sample_record)
    record["name"] = name
    record["date"] = date
    record["nickname"] = nickname
    record["phone"] = phone

    return record

def get_name_from_output_message_text(message_text):
    pattern = "(?:Имя: )([^\n]*)"
    name = re.findall(pattern, message_text)[0]
    return name
