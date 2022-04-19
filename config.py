# from enum import Enum

class Config:
    class Database:
        file = "database.json"
        sample_record = {
            "name": None,
            "date": None,
            "nickname": None,
            "phone": None,
            "note": None
        }
        record_fields = list(sample_record.keys())
        users = "user_data"

class BotText:
    START = "Вас приветствует *Happy Birthday Bot*!\nДавайте приступим!"
    ADD = "*Введите:*\n1. Имя человека\n2. Дату рождения в формате `DD.MM` или `DD.MM.YYYY`\n3. Ник в телеграме через *@* (по желанию)\n4. Номер телефона (по желанию)\n\n*Пример:*\nИван Иванов 1.1.1991\n\nЧтобы получить другой пример правильного сообщения, напишите /example, или нажмите на кнопку ниже."
    SHOW = "Show message example."
    DELETE = "Delete message example."
    EDIT = "Edit message example."

    CHOOSE_ACTION = "Выберите действие."
    CHOOSE_RECORD = "Выберите запись."
    YOU_HAVE_CHOSEN_TO_DELETE = "*Вы выбрали:*\n\n{}"

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
    InvalidNickname = "Ник должен быть не короче 5 и не длиннее 32 символов."
    InvalidRecordFields = "InvalidRecordFields."
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
class MessageIsCommand(Error): pass
class MessageTooLarge(Error): pass
class NoNameInTheBeginning(Error): pass
class NoDate(Error): pass
class InvalidNickname(Error): pass
class InvalidRecordFields(Error): pass
class UserHasNoRecords(Error): pass
class NewUserHasNoRecords(Error): pass
class RecordIndexOutOfRange(Error): pass
class RecordAlreadyExists(Error): pass
class RecordNotFound(Error): pass
