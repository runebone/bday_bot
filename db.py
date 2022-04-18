import pandas as pd
import json
from errors import *

file = "database.json"

record_fields = list({
    "name": None,
    "date": None,
    "nickname": None,
    "phone": None,
    "note": None
}.keys())

users = "user_data"

class Database:
    def __init__(self):
        self.file = file
        self.record_fields = record_fields
        self.users = users

    # FIXME: load and dump funcs logic
    # TODO: check your notes
    def load(self):
        with open(self.file) as f:
            database_dict = json.load(f)
        return database_dict

    def dump(self, updated_database_dict):
        with open(self.file, "r+") as f:
            json.dump(updated_database_dict, f, indent=4)

    def assert_valid_record_fields(self, record_dict):
        if (list(record_dict.keys()) != self.record_fields):
            raise InvalidRecordFields

    def get_users_list(self, database_dict):
        users = list(database_dict[self.users][0].keys())
        return users

    def add_user_record(self, database_dict, chat_id_str, record_dict):
        if (record_dict not in database_dict[self.users][0][chat_id_str]):
            database_dict[self.users][0][chat_id_str].append(record_dict)

    def add_new_user(self, database_dict, chat_id_str):
        database_dict[self.users][0][chat_id_str] = []

    def save_new_record(self, chat_id, record_dict):
        self.assert_valid_record_fields(record_dict)

        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list(database)

        if (chat_id in users):
            self.add_user_record(database, chat_id, record_dict)
        else:
            self.add_new_user(database, chat_id)
            self.add_user_record(database, chat_id, record_dict)

        self.dump(database)

    def get_user_records(self, database_dict, chat_id_str):
        return database_dict[self.users][0][chat_id_str]

    def delete_record_by_index(self, chat_id, record_index):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        elif (self.get_user_records(database, chat_id) == []):
            raise UserHasNoRecords
        else:
            records_df = pd.DataFrame(self.get_user_records(database, chat_id))
            print(records_df)

    # TODO: sort by field without loading. sort by table keys (indexes).
    # TODO: load single record without loading whole db.

if __name__ == "__main__":
    db = Database()

    record = {
        "name": "human",
        "date": "12.12.1212",
        "nickname": None,
        "phone": "lskj",
        "note": None
    }

    db.delete_record_by_index(317823738, "asdf")
