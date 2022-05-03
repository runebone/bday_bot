from datetime import datetime

#FIXME: rename module
#FIXME: 1-1-2022 -> 01-01-2022 db fmt

# Considerations:
# Normal date format (date_normal): DD.MM.YYYY (DD.MM)
# Database date format (db_date): MM-DD-YYYY (MM-DD)

def get_word_day_in_correct_form(number_of_days):
    day_word = "дней"
    n = number_of_days % 100

    if (n < 10 or n > 20):
        n %= 10
        if (n == 1):
            day_word = "день"
        elif (n in [2, 3, 4]):
            day_word = "дня"

    return day_word

def get_notification_message(record):
    pass

month_number_to_ru_name_dict = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
        }

month_ru_name_to_number_dict = {j: i for i, j in \
        month_number_to_ru_name_dict.items()}

days_in_months_dict = {
        12: 31, 1: 31, 2: 28,
        3: 31, 4: 30, 5: 31,
        6: 30, 7: 31, 8: 31,
        9: 30, 10: 31, 11: 30
        }

def normalize_date(date_string, sep="."):
    date = date_string

    separators = [" ", ".", ",", "-", "/"]

    # TODO: test it out
    for s in separators:
        if (s in date):
            date = sep.join(date.split(s))

    date = date.split(sep)
    date = list(map(lambda word: "{:02d}".format(int(word)), date))

    if (len(date) == 3 and len(date[2]) < 3):
        current_year = str(datetime.today().year)[2:]
        year = date[2]
        if (int(current_year) > int(year)):
            date[2] = "20" + date[2]
        else:
            date[2] = "19" + date[2]

    date = sep.join(date)

    return date

def date_is_valid(date_normal, sep="."):
    day, month, *year = list(map(int, date_normal.split(sep)))

    if (day <= days_in_months_dict[month]):
        return True
    elif (day == 29 and month == 2):
        if (year and not is_leap_year(*year)):
            return False
        return True

    return False

def is_leap_year(year):
    if (year % 400 == 0):
        return True
    elif (year % 100 == 0):
        return False
    elif (year % 4 == 0):
        return True

    return False

# TODO: rename functions DONE
#def normal_date_to_usa_format(date_normal):
def normal_date_to_db_fmt(date_normal, sep=".", db_sep="-"):
    # DD.MM.YYYY -> MM-DD-YYYY
    date = date_normal.split(sep)
    day, month, *year = date
    date = db_sep.join([month, day, *year])
    return date

#def us_date_to_ru_format(date):
def db_date_to_normal_fmt(db_date, sep=".", db_sep="-"):
    date = date.split(db_sep)
    month, day, *year = date
    date = sep.join([day, month, *year])
    return date

def get_date_in_db_fmt(day, month, *year, db_sep="-"):
    date = db_sep.join(list(map(lambda x: "{:02d}".format(x),
                                [month, day, *year])))
    return date

# FIXME: remove from_date_in_db_fmt in func names
def get_dmy_from_date_in_db_fmt(db_date, db_sep="-"):
    date = list(map(int, db_date.split(db_sep)))
    month, day, *year = date
    return (day, month, *year)

def get_date_with_current_year(db_date, db_sep="-"):
    date = list(map(int, db_date.split(db_sep)))
    month, day, *year = date
    year = datetime.now().year
    month, day, year = list(map(lambda x: "{:02d}".format(x),
                                [month, day, year]))
    date = db_sep.join([month, day, year])
    return date

def get_previous_month(month):
    # Consider month is integer from 1 to 12
    month_index = month #- 1 # Depends on order the of months in dict
    previous_month = list(days_in_months_dict.keys())[month_index - 1]
    return previous_month

def get_previous_date(db_date):
    # Consider db_date is mm-dd-yyyy
    # Consider date is correct
    day, month, *year = get_dmy_from_date_in_db_fmt(db_date)

    if (day != 1):
        day -= 1
    else:
        day = days_in_months_dict[get_previous_month(month)]

        if (month == 1):
            month = 12
            # year = [] => year = []
            # year = [x] => year = [(x-1)]
            year = year if not year else [year[0] - 1]
        elif (month == 3 and year and is_leap_year(*year)):
            day += 1
            month -= 1
        else:
            month -= 1

    previous_date = get_date_in_db_fmt(day, month, *year)

    return previous_date

def get_date_x_days_ago(db_date, x):
    # Consider db_date is mm-dd-yyyy
    # Consider date is correct
    day, month, *year = get_dmy_from_date_in_db_fmt(db_date)

    while (x > 0):
        if (day != 1):
            days_to_subtract = day - 1
            if (x < days_to_subtract):
                day -= x
                x = 0
            else:
                day -= days_to_subtract
                x -= days_to_subtract
        else:
            date = get_date_in_db_fmt(day, month, *year)
            date = get_previous_date(date)
            day, month, *year = get_dmy_from_date_in_db_fmt(date)
            x -= 1

    # Returns date in db_date format
    date_x_days_ago = get_date_in_db_fmt(day, month, *year)

    return date_x_days_ago

# FIXME: list(map(... -> map(... everywhere in project
def get_days_until_bday(notify_date, bday_date, sep="-"):
    notify_month, notify_day, notify_year = map(int, notify_date.split(sep))
    bday_month, bday_day, *bday_year = map(int, bday_date.split(sep))

    bday_year = notify_year
    cond1 = (bday_month < notify_month)
    cond2 = (bday_month == notify_month)
    cond3 = (bday_day < notify_day)
    if (cond1 or (cond2 and cond3)):
        bday_year += 1

    days = 0
    for month in range(notify_month - 1,
                       bday_month + 12 * (bday_year - notify_year) - 1):
        # Adds days from all in-between months including
        # notify_month and excluding bday_month
        days += days_in_months_dict[1 + month % 12]

    # days -= (notify_day - 1) # v1
    days -= notify_day # Equivalent to v1
    days += bday_day

    # Account 29th February
    cond1 = is_leap_year(notify_year)
    cond2 = (notify_month <= 2)
    cond3 = (bday_month > 2)
    if (cond1 and cond2 and cond3):
        days += 1

    cond1 = (notify_year < bday_year)
    cond2 = (is_leap_year(bday_year))
    cond3 = (bday_month > 2)
    if (cond1 and cond2 and cond3):
        days += 1

    # days -= 1 # v1

    return days

if __name__ == "__main__":
    print(get_date_x_days_ago("01-02-2021", 84365))
    print(get_previous_date("03-01-2024"))
    print(get_previous_date("05-01-2022"))
    print(get_previous_date("05-01"))
    print(is_leap_year(2020))
    #for i in range(100): print(f"{i}", get_word_day_in_correct_form(i))
    print(get_date_with_current_year("03-01-2020"))
    print(get_date_with_current_year("03-01"))

    print(get_days_until_bday("01-01-2020", "03-01-2020")) # 60
    print(get_days_until_bday("02-27-2020", "03-01-2020")) # 3
    print(get_days_until_bday("02-29-2020", "03-01-2020")) # 1
    print(get_days_until_bday("02-27-2020", "02-29-2020")) # 2
    print(get_days_until_bday("02-27-2020", "02-27-2020")) # 0
    print(get_days_until_bday("02-27-2020", "02-28-2020")) # 1
    print()
    print(get_days_until_bday("04-27-2020", "03-27")) # 334 (365 - 31)
    print(get_days_until_bday("04-01-2020", "03-01")) # 334 (365 - 31)
    print(get_days_until_bday("04-01-2019", "03-01")) # 335 (366 - 31)
    print(get_days_until_bday("04-01-2020", "04-01")) # 0
    print(get_days_until_bday("06-01-2020", "12-01")) # 183
    print(get_days_until_bday("12-01-2020", "12-31")) # 30
    print(get_days_until_bday("12-01-2020", "01-01")) # 31
