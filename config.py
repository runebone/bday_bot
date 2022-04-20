# from enum import Enum
from dev_data import DEVELOPER_CHAT_ID

class Config:
    class Database:
        file = "database.json"
        sample_record = {
            "name": None,
            "date": None,
            "nickname": None,
            "phone": None,
        }
        record_fields = list(sample_record.keys())
        users = "user_data"

class BotText:
    START = "Вас приветствует *Happy Birthday Bot*!\nДавайте приступим!"
    ADD = "*Введите:*\n1. Имя человека\n2. Дату рождения в формате `DD.MM` или `DD.MM.YYYY`\n3. Ник в телеграме через *@* (по желанию)\n4. Номер телефона (по желанию)\n\n*Пример:*\nИван Иванов 1.1.1991\n\nЧтобы получить другой пример правильного сообщения, напишите /example, или нажмите на кнопку ниже."
    SHOW = "Show message example."
    DELETE = "Delete message example."
    EDIT = "Edit message example."

    CHANGED_MIND = "Передумали?"
    CHOOSE_ACTION = "Выберите действие."
    CHOOSE_RECORD = "Выберите запись."
    CHOOSE_FIELD_TO_EDIT = "Выберите поле, которое хотите изменить."
    YOU_HAVE_CHOSEN_TO_DELETE = "*Вы выбрали:*\n\n{}"
    YOU_HAVE_CHOSEN_TO_EDIT = "*Вы выбрали:*\n\n{}"

    NAME_INPUT_OFFER = "Введите новое имя:"
    DATE_INPUT_OFFER = "Введите новую дату:"
    NICKNAME_INPUT_OFFER = "Введите новый ник через *@*:"
    PHONE_INPUT_OFFER = "Введите новый номер телефона:"
    INPUT_AGAIN_OFFER = ADD

    ADD_SUCCESS = "Запись успешно добавлена."
    DELETE_SUCCESS = "Запись успешно удалена."
    EDIT_SUCCESS = "Запись успешно изменена."

    output = {
            "index": "№{}",
            "name": "Имя: {}",
            "date": "Дата рождения: {}",
            "nickname": "Никнейм: @{}",
            "phone": "Номер телефона: {}"
    }

class FailText:
    MessageTooLarge = "Сообщение слишком длинное."
    NoNameInTheBeginning = "Сообщение должно начинаться с имени " \
            "поздравляемого и содержать дату."
    NoDate = "Сообщение должно содержать дату."
    NoNickname = "Сообщение должно содержать ник."
    NoPhone = "Сообщение должно содержать номер телефона."
    InvalidNickname = "Ник должен быть не короче 5 и не длиннее 32 символов."
    UserHasNoRecords = "У вас нет записей. " \
    "Чтобы добавить запись, напишите /add, или нажмите на кнопку."
    NewUserHasNoRecords = "У вас нет записей. " \
    "Чтобы добавить запись, напишите /add, или нажмите на кнопку."
    RecordIndexOutOfRange = "У вас нет такой записи." #TODO: offer SHOW
    RecordAlreadyExists = "У вас уже есть такая запись."
    RecordNotFound = "Запись не найдена."

    UncaughtError = "Непойманная ошибка: {}."

# ==================================================

class Const:
    MAX_MESSAGE_LENGTH = 256

# ==================================================

class Error(Exception): pass
"""Base class for custom exceptions."""
class MessageIsCommand(Error):
    def add(message, process_function, bot, db):
        text = "Вы вышли из режима добавления. Введите команду {} повторно, чтобы исполнить её."
        bot.send_message(message.chat.id, text.format(message.text))
        process_function(message, bot)

class MessageTooLarge(Error):
    text = FailText.MessageTooLarge
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, MessageTooLarge.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class NoNameInTheBeginning(Error):
    text = FailText.NoNameInTheBeginning
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, NoNameInTheBeginning.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class NoDate(Error):
    text = FailText.NoDate
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, NoDate.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class NoNickname(Error):
    text = FailText.NoNickname
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, NoNickname.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class NoPhone(Error):
    text = FailText.NoPhone
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, NoPhone.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class InvalidNickname(Error):
    text = FailText.InvalidNickname
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, InvalidNickname.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class UserHasNoRecords(Error):
    text = FailText.UserHasNoRecords
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, UserHasNoRecords.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class NewUserHasNoRecords(Error):
    text = FailText.NewUserHasNoRecords
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, NewUserHasNoRecords.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class RecordIndexOutOfRange(Error):
    text = FailText.RecordIndexOutOfRange
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, RecordIndexOutOfRange.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class RecordAlreadyExists(Error):
    text = FailText.RecordAlreadyExists
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, RecordAlreadyExists.text)
        bot.register_next_step_handler(message, process_function, bot, db)

class RecordNotFound(Error):
    text = FailText.RecordNotFound
    def default(message, process_function, bot, db):
        bot.send_message(message.chat.id, RecordNotFound.text)
        bot.register_next_step_handler(message, process_function, bot, db)
