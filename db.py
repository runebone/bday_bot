import pandas as pd
import json
from errors import *

file = "database.json"

# XXX: Date is stored in MM-DD-YYYY (USA) format.

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
        with open(self.file, "w") as f:
            json.dump(updated_database_dict, f, indent=4)

    def assert_valid_record_fields(self, record_dict):
        if (list(record_dict.keys()) != self.record_fields):
            raise InvalidRecordFields

    def get_users_list_from_dict(self, database_dict):
        users_list = list(database_dict[self.users][0].keys())
        return users_list

    def add_user_record_to_dict(self, database_dict, chat_id_str, record_dict):
        if (record_dict not in database_dict[self.users][0][chat_id_str]):
            database_dict[self.users][0][chat_id_str].append(record_dict)

    def add_new_user_to_dict(self, database_dict, chat_id_str):
        database_dict[self.users][0][chat_id_str] = []

    def add_new_record(self, chat_id, record_dict):
        self.assert_valid_record_fields(record_dict)

        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id in users):
            self.add_user_record_to_dict(database, chat_id, record_dict)
        else:
            self.add_new_user_to_dict(database, chat_id)
            self.add_user_record_to_dict(database, chat_id, record_dict)

        self.dump(database)

    def get_user_records_from_dict(self, database_dict, chat_id_str):
        return database_dict[self.users][0][chat_id_str]

    def get_user_records(self, chat_id):
        chat_id = str(chat_id)
        database = self.load()
        user_records = self.get_user_records_from_dict(database, chat_id)

        return user_records

    def delete_record_by_index(self, chat_id, record_index):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (user_records == []):
            raise UserHasNoRecords
        elif (len(user_records) <= record_index):
            raise RecordIndexOutOfRange
        else:
            # df - user records dataframe
            df = pd.DataFrame(self.get_user_records_from_dict(database, \
                                                                chat_id))
            df = df.sort_values(by="date").reset_index(drop=True)
            df = df.drop(labels=record_index, axis=0) # Delete record
            df = df.to_dict(orient="records")

            database[self.users][0][chat_id] = df

            self.dump(database)

    def get_record_by_index(self, chat_id, record_index):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (user_records == []):
            raise UserHasNoRecords
        elif (len(user_records) <= record_index):
            raise RecordIndexOutOfRange
        else:
            # df - user records dataframe
            df = pd.DataFrame(self.get_user_records_from_dict(database, \
                                                                chat_id))
            df = df.sort_values(by="date").reset_index(drop=True)
            df = df.loc[[record_index]] # Get record
            df = df.to_dict(orient="records")

            return df

    # TODO: sort by field without loading. sort by table keys (indexes).
    # TODO: load single record without loading whole db.

if __name__ == "__main__":
    db = Database()

    record = {
        "name": "humanoid",
        "date": "12.12.1212",
        "nickname": None,
        "phone": "lskj",
        "note": None
    }

    #db.add_new_record(317823738, record)
    #db.delete_record_by_index(317823738, 1)
    print(db.get_record_by_index(440058642, 1))
