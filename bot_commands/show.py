from my_regex import *
from config import *

def process_show_step(message, bot, db):
    try:
        # TODO: some asserts (user has records)
        records = db.get_user_records(message.chat.id)
        for i in range(len(records)):
            string = get_printable_string_from_record(records[i], i)
            bot.send_message(message.chat.id, string)

    # FIXME: DRY
    except UserHasNoRecords:
        bot.send_message(message.chat.id, FailText.UserHasNoRecords)
        bot.register_next_step_handler(message, process_show_step, bot, db)
    except NewUserHasNoRecords:
        bot.send_message(message.chat.id, FailText.NewUserHasNoRecords)
        bot.register_next_step_handler(message, process_show_step, bot, db)
    except Exception as e:
        bot.send_message(message.chat.id, FailText.UncaughtError.format(str(e)))

def get_printable_string_from_record(record, index):
    date = us_date_to_ru_format(record["date"])

    format_string = f"[ №{index + 1} ]\n"
    format_string += f"Имя: {record['name']}\n"
    format_string += f"Дата рождения: {date}\n"

    if (record["nickname"] != None):
        format_string += f"Никнейм: @{record['nickname']}\n"
    if (record["phone"] != None):
        phone = beautify_phone(record["phone"])
        format_string += f"Номер телефона: {phone}"

    return format_string

def us_date_to_ru_format(date):
    date = date.split("-")
    date[0], date[1] = date[1], date[0]
    date = ".".join(date)
    return date
