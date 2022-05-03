from init import bot, db
from config import BotText
import date as my_date
import time
import datetime
from markups import gen_notification_markup

# Function which opens db file every time; checks for coming up bdays
# And sends notificatons

def bracketize(string):
    return "".join(["(", string, ")"])

def send_notification_today(bot, chat_id, record):
    person = record["name"]
    nickname = ""
    phone = ""
    sep = ""

    if (record["nickname"]):
        nickname = "@" + record["nickname"]
    if (record["phone"]):
        phone = record["phone"]

    if (nickname and phone):
        nickname = "".join(["(", nickname])
        phone = "".join([phone, ")"])
        sep = ", "
    elif (nickname):
        nickname = bracketize(nickname)
    elif (phone):
        phone = bracketize(phone)

    msg = BotText.NOTIFICATION_TODAY.format(person=person,
                                               nickname=nickname,
                                               sep=sep,
                                               phone=phone)

    bot.send_message(chat_id, msg, reply_markup=gen_notification_markup())

def send_notification_tomorrow(bot, chat_id, record):
    person = record["name"]
    nickname = ""
    phone = ""
    sep = ""

    if (record["nickname"]):
        nickname = "@" + record["nickname"]
    if (record["phone"]):
        phone = record["phone"]

    if (nickname and phone):
        nickname = "".join(["(", nickname])
        phone = "".join([phone, ")"])
        sep = ", "
    elif (nickname):
        nickname = bracketize(nickname)
    elif (phone):
        phone = bracketize(phone)

    msg = BotText.NOTIFICATION_TOMORROW.format(person=person,
                                               nickname=nickname,
                                               sep=sep,
                                               phone=phone)

    bot.send_message(chat_id, msg, reply_markup=gen_notification_markup())

def send_notification_default(bot, chat_id, record, n_days):
    msg = BotText.NOTIFICATION_DEFAULT
    person = record["name"]
    nickname = ""
    phone = ""
    sep = ""

    if (record["nickname"]):
        nickname = "@" + record["nickname"]
    if (record["phone"]):
        phone = record["phone"]

    if (nickname and phone):
        nickname = "".join(["(", nickname])
        phone = "".join([phone, ")"])
        sep = ", "
    elif (nickname):
        nickname = bracketize(nickname)
    elif (phone):
        phone = bracketize(phone)

    word = my_date.get_word_day_in_correct_form(n_days)

    msg = BotText.NOTIFICATION_DEFAULT.format(days_number=n_days,
                                              days_word=word,
                                              person=person,
                                              nickname=nickname,
                                              sep=sep,
                                              phone=phone)

    bot.send_message(chat_id, msg, reply_markup=gen_notification_markup())

def get_hmdmy_from_notify_date(db_notify_date, db_sep="-"):
    date = " ".join(db_notify_date.split(db_sep))
    date = " ".join(date.split(":"))
    month, day, *year, hour, minute = list(map(int, date.split()))
    return (hour, minute, day, month, *year)

def time_to_send(db_notify_date):
    now = datetime.datetime.now()
    date_tuple = get_hmdmy_from_notify_date(db_notify_date)
    hour, minute, day, month, *year = date_tuple

    year = [] if year == [] else year[0]

    if ((year == [] or now.year == year) and
        now.month == month and
        now.day == day):

        if (now.hour == hour and
            now.minute >= minute):
            return True
        elif (now.hour > hour):
            return True

    return False

def check_database_and_send_notifications(bot, db):
    db_dict = db.load()
    users = db.get_users_list_from_dict(db_dict)
    for chat_id in users:
        records = db.get_user_records_from_dict(db_dict, chat_id)
        for record in records:
            # FIXME: db field names -> config
            notify_dates_to_remove = []
            for notify_date in record["notify_when"]:

                if (time_to_send(notify_date)):
                    # XXX: notify date does not contain year !!!
                    notify_date_without_time = notify_date.split()[0]
                    bday_date = record["date"]
                    prev_to_bday_date = my_date.get_previous_date(bday_date)

                    # FIXME: ugly remove-year-from-date
                    bday_is_today = (bday_date
                                     == notify_date_without_time[:5])

                    print(bday_date, notify_date)

                    bday_is_tomorrow = (prev_to_bday_date
                                        == notify_date_without_time[:5])
                    if (bday_is_today):
                        send_notification_today(bot, chat_id, record)
                    elif (bday_is_tomorrow):
                        send_notification_tomorrow(bot, chat_id, record)
                    else:
                        # FIXME: x = get_diff_between_dates; 7 -> x
                        send_notification_default(bot, chat_id, record, 7)

                    notify_dates_to_remove.append(notify_date)

            record_index = db.get_record_index_by_record(chat_id, record)
            new_record = record

            for nd in notify_dates_to_remove:
                new_record["notify_when"].remove(nd)

            db.update_record_by_index(chat_id, new_record, record_index)

def notifications_job(bot, db):
    while True:
        check_database_and_send_notifications(bot, db)
        time.sleep(1)

if __name__ == "__main__":
    check_database_and_send_notifications(bot, db)