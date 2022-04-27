from datetime import datetime

# Considerations:
# Normal date format (date_normal): DD.MM.YYYY (DD.MM)
# Database date format (db_date): MM-DD-YYYY (MM-DD)

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
    date = db_sep.join(list(map(str, [month, day, *year])))
    return date

def get_dmy_from_date_in_db_fmt(db_date, db_sep="-"):
    date = list(map(int, db_date.split(db_sep)))
    month, day, *year = date
    return (day, month, *year)

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

if __name__ == "__main__":
    print(get_date_x_days_ago("01-02-2021", 84365))
    print(get_previous_date("03-01-2024"))
