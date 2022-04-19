import numpy as np
from datetime import datetime

# TODO: add more funny names and definitions

names = \
"""Миша
Паша
Семён
Игорь
Дима
Егор
Лера
Соня
Катя
Аня
Макс
Степан
Серёга
Джамбулат""".split("\n")

definitions = \
"""школа
работа
сборы
универ
коллега
папа
мама
сестра
брат
математика
физика
программирование
литература
английский
китайский
японский
шахта
дача
пиломатериалы
еда""".split("\n")

date_formats = \
"""{:d} {:d} {:02d}
{:d}.{:d}.{:02d}""".split("\n")

# Generate nicknames
nick_adjectives = \
"""street
mountain
cool
great
awesome
handsome
perfect
ideal
i_love
i_hate
amazing""".split("\n")

nick_nouns = \
"""man
dude
sister
father
racer
king
king_kong
elon_musk
jeff_bezos""".split("\n")

phone_formats = \
"""{:03d}{:03d}{:02d}{:02d}
({:03d}){:03d}-{:02d}-{:02d}
8{:03d}{:03d}{:02d}{:02d}
8({:03d}){:03d}-{:02d}-{:02d}
+7{:03d}{:03d}{:02d}{:02d}
+7({:03d}){:03d}-{:02d}-{:02d}""".split("\n")

def get_example():
    name = np.random.choice(names)

    example = [name]

    if (np.random.randint(100) > 10):
        definition = np.random.choice(definitions)
        example.append(definition)

    date_fmt = np.random.choice(date_formats)

    day = 1 + np.random.randint(31)
    month = 1 + np.random.randint(12)
    year = 1 + np.random.randint(99)

    if (np.random.randint(2)):
        current_year = str(datetime.today().year)[2:]
        if (int(current_year) > year):
            year += 2000
        else:
            year += 1900

    date = date_fmt.format(day, month, year)

    example.append(date)

    if (np.random.randint(100) > 50):
        nick_adj = np.random.choice(nick_adjectives)
        nick_noun = np.random.choice(nick_nouns)
        nickname = "@{}_{}".format(nick_adj, nick_noun)
        example.append(nickname)

    if (np.random.randint(100) > 70):
        phone_fmt = np.random.choice(phone_formats)
        phone = phone_fmt.format(np.random.randint(1000), \
                np.random.randint(1000), \
                np.random.randint(100), \
                np.random.randint(100))

        example.append(phone)

    example = " ".join(example)

    return example

if __name__ == "__main__":
    print(get_example())
