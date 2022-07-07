from dev_data import DEVELOPER_CHAT_ID
from markups import *

BOT_DIR = "."
BACKUP_DIR = "backup"

BOT_DB_FILE = "database.json"

DATE_FMT = "%y%m%d-%H%M%S"
BACKUP_FILE = f"db_{DATE_FMT}.json"

class Config:
    DEFAULT_NOTIFICATION_TIME = "12:00"

    class Database:
        file = "database.json"
        sample_record = {
            "name": None,
            "date": None,
            "nickname": None,
            "phone": None,
            "notify_when": [], # Dates to notify at; DD.MM HH:mm
            # Message sent - pop
            # TODO: every sunday 00:00 check for empty notify_when and
            # set it to default / user custom; make sure user custom does not
            # interfere with "sunday 00:00"
        }
        record_fields = list(sample_record.keys())
        users = "user_data"
        sn = "single_notifications"

# TODO: rename BotText -> Messages
# TODO: check configs of other programs
class BotText:
    START = "Вас приветствует *Happy Birthday Bot*!\nДавайте приступим! 🎉🎈"
    # RECORD_EXAMPLE = "*Введите:*\n1. Имя человека\n2. Дату рождения в формате `DD.MM` или `DD.MM.YYYY`\n3. Ник в телеграме через *@* (по желанию)\n4. Номер телефона (по желанию)\n\n*Пример:*\nИван Иванов 1.1.1991\n\nЧтобы получить другой пример правильного сообщения, напишите /example."
    RECORD_EXAMPLE = "Напиши имя и дату рождения для создания напоминания вот так, по-простому:\n\nМарина 25 9 1986\n\nили с дополнительной информацией (можно указать ник и/или телефон, чтобы они отображались в уведомлении, если тебе так удобнее):\n\nМарина 25 9 1986 @marina +79991234567"
    EXIT_ADD = "Чтобы выйти из режима добавления записи, нажми: /cancel."
    ADD = "\n\n".join([RECORD_EXAMPLE, EXIT_ADD])
    ADD_MORE = "Добавьте ещё, либо напишите /cancel для выхода из режима добавления записи."

    CHANGED_MIND = "Передумали?"
    CHOOSE_ACTION = "Выберите действие."
    CHOOSE_RECORD = "Выберите запись."
    CHOOSE_FIELD_TO_EDIT = "Выберите поле, которое хотите изменить."
    YOU_HAVE_CHOSEN_TO_DELETE = "Вы выбрали:\n\n{}" # XXX: rm **
    YOU_HAVE_CHOSEN_TO_EDIT = "Вы выбрали:\n\n{}" # XXX: rm **

    NAME_INPUT_OFFER = "Введите новое имя, или напишите:\n/example - для получения примера,\n/cancel - для отмены."
    DATE_INPUT_OFFER = "Введите новую дату, или напишите:\n/example - для получения примера,\n/cancel - для отмены."
    NICKNAME_INPUT_OFFER = "Введите новый ник через *@*, или напишите:\n/example - для получения примера,\n/cancel - для отмены,\n/reset - для сброса ника."
    PHONE_INPUT_OFFER = "Введите новый номер телефона, или напишите:\n/example - для получения примера,\n/cancel - для отмены,\n/reset - для сброса номера телефона."
    EXIT_INPUT_AGAIN = "Чтобы выйти из режима повторного ввода записи, напишите /cancel."
    INPUT_AGAIN_OFFER = "\n\n".join([RECORD_EXAMPLE, EXIT_INPUT_AGAIN])

    ADD_SUCCESS = "✅ Запись успешно добавлена.\n\nВам придёт напоминание в сам День Рождения, а также за неделю и за день до него."
    DELETE_SUCCESS = "✅ Запись успешно удалена."
    EDIT_SUCCESS = "✅ Запись успешно изменена."

    NOTIFICATION_DEFAULT = "Через {days_number} {days_word} День Рождения у {person}{space}{nickname}{sep}{phone}. 🎉"
    NOTIFICATION_TOMORROW = "Завтра День Рождения у {person}{space}{nickname}{sep}{phone}. 🎉🎂"
    NOTIFICATION_TODAY = "Сегодня День Рождения у {person}{space}{nickname}{sep}{phone}. 🎉🎂🎈"

    output = {
            "index": "№{}",
            "name": "Имя: {}",
            "date": "Дата рождения: {}",
            "nickname": "Никнейм: @{}",
            "phone": "Номер телефона: {}"
    }

# TODO: FailText -> Messages
class FailText:
    MessageTooLarge = "❗ Сообщение слишком длинное."
    NoNameInTheBeginning = "❗ Сообщение должно начинаться с имени " \
            "поздравляемого и содержать дату."
    NoDate = "❗ Сообщение должно содержать дату."
    NoNickname = "❗ Сообщение должно содержать ник."
    NoPhone = "❗ Сообщение должно содержать номер телефона."
    InvalidNickname = "❗ Ник должен быть не короче 5 и не длиннее 32 символов."
    UserHasNoRecords = "❗ У вас нет записей. " \
    "Чтобы добавить запись, напишите /add, или нажмите на кнопку."
    NewUserHasNoRecords = "❗ У вас нет записей. " \
    "Чтобы добавить запись, напишите /add, или нажмите на кнопку."
    RecordIndexOutOfRange = "❗ У вас нет такой записи." #TODO: offer SHOW
    RecordAlreadyExists = "❗ У вас уже есть такая запись."
    RecordNotFound = "❗ Запись не найдена."

    UncaughtError = "❗❗❗ Непойманная ошибка: {}."

# ==================================================

class Const:
    MAX_MESSAGE_LENGTH = 256

# ==================================================

# FIXME: DRY!!!!!

class Error(Exception): pass
"""Base class for custom exceptions."""
class MessageIsCommand(Error):
    def add(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима добавления. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def input_name(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения имени. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def input_date(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения даты. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def input_nickname(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения ника. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def input_phone(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения номера телефона. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def input_again(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима повторного введения записи. Введите команду {} заново, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot, db, *args, **kwargs)

    def cancel_add(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима добавления."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

    def cancel_input_name(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения имени."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

    def cancel_input_date(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения даты."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

    def cancel_input_nickname(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения ника."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

    def cancel_input_phone(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима изменения номера телефона."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

    def cancel_input_again(message, process_function, bot, db, *args, **kwargs):
        text = "Вы вышли из режима повторного введения записи."
        bot.send_message(message.chat.id, text)
        process_function(message, bot, db, *args, **kwargs)

# TODO: __class__.__name__ to get class name; create single func
class MessageTooLarge(Error):
    text = FailText.MessageTooLarge
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, MessageTooLarge.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class NoNameInTheBeginning(Error):
    text = FailText.NoNameInTheBeginning
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, NoNameInTheBeginning.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class NoDate(Error):
    text = FailText.NoDate
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, NoDate.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class NoNickname(Error):
    text = FailText.NoNickname
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, NoNickname.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class NoPhone(Error):
    text = FailText.NoPhone
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, NoPhone.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class InvalidNickname(Error):
    text = FailText.InvalidNickname
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, InvalidNickname.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class UserHasNoRecords(Error):
    text = FailText.UserHasNoRecords
    def default(message, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, UserHasNoRecords.text, reply_markup=gen_add_friend_markup())
        #bot.register_next_step_handler(message, process_function, bot, db)

class NewUserHasNoRecords(Error):
    text = FailText.NewUserHasNoRecords
    def default(message, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, NewUserHasNoRecords.text, reply_markup=gen_add_friend_markup())
        #bot.register_next_step_handler(message, process_function, bot, db)

class RecordIndexOutOfRange(Error):
    text = FailText.RecordIndexOutOfRange
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, RecordIndexOutOfRange.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class RecordAlreadyExists(Error):
    text = FailText.RecordAlreadyExists
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, RecordAlreadyExists.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)

class RecordNotFound(Error):
    text = FailText.RecordNotFound
    def default(message, process_function, bot, db, *args, **kwargs):
        bot.send_message(message.chat.id, RecordNotFound.text)
        bot.register_next_step_handler(message, process_function, bot, db, *args, **kwargs)
