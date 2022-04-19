import re
from datetime import datetime

# Date regex
def get_date_regex():
    # There is no not-space symbols before the match
    begin_of_match = "(?<!\S)"
    end_of_match = "(?!\S)" # "(?=\s|$)" # ---||--- after the match
    sep = "[ .,-/]"
    day = "(?:[0]?[1-9]|[12]\d|3[01])"
    month = "(?:[0]?[1-9]|1[0-2])"
    year = "(?:19\d\d|20\d\d|\d\d|\d)"
    date = "(?:" + day + sep + month + sep + year + "|" \
            + day + sep + month + ")"
    date_regex = begin_of_match + date + end_of_match

    return date_regex

# Nickname regex
def get_nickname_regex():
    begin_of_match = "(?<!\S)"
    end_of_match = "(?!\S)"
    # Telegram nickname is from 5 to 32 characters long
    nickname_regex = begin_of_match + "@\S{5,32}" + end_of_match

    return nickname_regex

# Phone number regex
def get_phone_regex():
    begin_of_match = "(?<!\S)"
    end_of_match = "(?!\S)"
    country_code = "(?:[+]?\d{1,4})"
    operator_code = "(?:[ -]?\(\d\d\d\)[ -]?|[ -]?\d\d\d[ -]?)"
    phone_codes = "(?:" + country_code + operator_code + "|" \
            + operator_code + ")"
    phone_number = "(?:\d\d\d[ -]?\d\d[ -]?\d\d)"
    phone_regex = begin_of_match + phone_codes + phone_number + end_of_match

    return phone_regex

# Global regex CONSTANTS
date_regex = get_date_regex()
nickname_regex = get_nickname_regex()
phone_regex = get_phone_regex()

# Functions
def remove_comas_from_message(message_string):
    # FIXME: potential bug
    return " ".join(message_string.split(","))

def get_date_from_message(message_string):
    message_string = remove_comas_from_message(message_string)

    date = re.findall(date_regex, message_string)

    if (date != []):
        # Use first if there are several matches
        date = date[0]
    else:
        date = None

    return date

def get_nickname_from_message(message_string):
    message_string = remove_comas_from_message(message_string)

    nickname = re.findall(nickname_regex, message_string)

    if (nickname != []):
        # Use first if there are several matches
        nickname = nickname[0]
    else:
        nickname = None

    return nickname

def get_phone_from_message(message_string):
    message_string = remove_comas_from_message(message_string)

    phone = re.findall(phone_regex, message_string)

    if (phone != []):
        # Use first if there are several matches
        phone = phone[0]
    else:
        phone = None

    return phone

def get_name_from_message(message_string):
    message_string = remove_comas_from_message(message_string)

    name = None
    date = get_date_from_message(message_string)
    nickname = get_nickname_from_message(message_string)
    phone = get_phone_from_message(message_string)

    # Consider name is everything what comes before
    # first occurance any matched pattern (phone, date etc)
    if (date != None):
        name = message_string.split(date)[0]
        if (nickname != None):
            name = name.split(nickname)[0]
        if (phone != None):
            name = name.split(phone)[0]
        name = name.strip(" .,/")

    # If there is no date in message - message is invalid =>
    # => there is no name => return None.

    if (name == ""):
        name = None

    return name

# XXX
def normalize_date(date_string, sep="."):
    date = date_string

    date = sep.join(date.split(" "))
    date = sep.join(date.split("."))
    date = sep.join(date.split(","))
    date = sep.join(date.split("-"))
    date = sep.join(date.split("/"))

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

def normal_date_to_usa_format(date_normal):
    # DD.MM.YYYY -> MM-DD-YYYY
    date = date_normal.split(".")
    date[0], date[1] = date[1], date[0]
    return "-".join(date)

def us_date_to_ru_format(date):
    date = date.split("-")
    date[0], date[1] = date[1], date[0]
    date = ".".join(date)
    return date

def normalize_phone(phone_string):
    phone_normal = phone_string

    phone_normal = "".join(phone_normal.split(" "))
    phone_normal = "".join(phone_normal.split("+"))
    phone_normal = "".join(phone_normal.split("-"))
    phone_normal = "".join(phone_normal.split("("))
    phone_normal = "".join(phone_normal.split(")"))

    return phone_normal

def beautify_phone(phone_normal_string):
    # ABC1234567890 - phone_normal_string
    phone_beautiful = ""
    phone_beautiful += phone_normal_string[-2:]
    # phone_beautiful is now "90"
    phone_beautiful = "-" + phone_beautiful
    phone_beautiful = phone_normal_string[-4:-2] + phone_beautiful
    # "78-90"
    phone_beautiful = "-" + phone_beautiful
    phone_beautiful = phone_normal_string[-7:-4] + phone_beautiful
    # "456-78-90"
    phone_beautiful = ")" + phone_beautiful
    phone_beautiful = phone_normal_string[-10:-7] + phone_beautiful
    phone_beautiful = "(" + phone_beautiful
    # "(123)456-78-90"
    phone_beautiful = phone_normal_string[:-10] + phone_beautiful
    # "ABC(123)456-78-90"

    # If phone number does not contain country code - use Russia by default
    if (phone_normal_string[:-10] == ""):
        phone_beautiful = "8" + phone_beautiful

    # Substitute 8 by 7 in Russian phone numbers
    if (phone_beautiful[:2] == "8("):
        pass
        # phone_beautiful = list(phone_beautiful)
        # phone_beautiful[0] = "7"
        # phone_beautiful = "".join(phone_beautiful)
    else:
        phone_beautiful = "+" + phone_beautiful
        # "+ABC(123)456-78-90"

    return phone_beautiful

if __name__ == "__main__":
    print("Date regex:\n%s\n" % date_regex)
    print("Nickname regex:\n%s\n" % nickname_regex)
    print("Phone regex:\n%s\n" % phone_regex)
    message = input("Input message: ")
    print("Name: ", get_name_from_message(message))
    print("Date: ", get_date_from_message(message))
    print("Nickname: ", get_nickname_from_message(message))
    print("Phone: ", get_phone_from_message(message))
