class Error(Exception):
    """Base class for custom exceptions."""
    pass

class MessageTooLarge(Error):
    text = "Message is too large."
class NoNameInTheBeginning(Error):
    text = "Message should start with name."
class NoDate(Error):
    text = "Message should contain date."
class InvalidNickname(Error):
    text = "Nickname should be from 5 to 32 characters long."
class InvalidRecordFields(Error):
    text = "db.py: Invalid record fields"
class UserHasNoRecords(Error):
    text = "User has no records."
class NewUserHasNoRecords(Error):
    text = "New user has no records."
