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
    START = "Start message example."
    ADD = "Add message example."
    SHOW = "Show message example."
    DELETE = "Delete message example."
    EDIT = "Edit message example."

    ADD_SUCCESS = "Запись успешно добавлена."
    DELETE_SUCCESS = "Запись успешно удалена."
    EDIT_SUCCESS = "Запись успешно изменена."

class FailText:
    MessageTooLarge = "Сообщение слишком длинное."
    NoNameInTheBeginning = "Сообщение должно начинаться с имени \
            поздравляемого и содержать дату."
    NoDate = "Сообщение должно содержать дату."
    InvalidNickname = "Ник должен быть не короче 5 и не длиннее 32 символов."
    InvalidRecordFields = "InvalidRecordFields."
    UserHasNoRecords = "У вас нет записей." # TODO: offer ADD
    NewUserHasNoRecords = "У вас нет записей. \
            Чтобы добавить запись, напишите /add." # TODO: offer ADD
    RecordIndexOutOfRange = "У вас нет такой записи." #TODO: offer SHOW
    RecordAlreadyExists = "У вас уже есть такая запись."

    UncaughtError = "Непойманная ошибка: {}."

# ==================================================

class Const:
    MAX_MESSAGE_LENGTH = 256

# ==================================================

class Error(Exception): pass
"""Base class for custom exceptions."""
class MessageTooLarge(Error): pass
class NoNameInTheBeginning(Error): pass
class NoDate(Error): pass
class InvalidNickname(Error): pass
class InvalidRecordFields(Error): pass
class UserHasNoRecords(Error): pass
class NewUserHasNoRecords(Error): pass
class RecordIndexOutOfRange(Error): pass
class RecordAlreadyExists(Error): pass
