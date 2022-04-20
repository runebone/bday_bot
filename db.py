from config import *
import json

class Database:
    def __init__(self, file):
        self.file = file
        self.sample_record = Config.Database.sample_record
        self.record_fields = Config.Database.record_fields
        self.users = Config.Database.users
        self.empty = {self.users: [{}]}

    def load(self):
        try:
            with open(self.file) as f:
                database_dict = json.load(f)
        except:
            # Database is not created
            with open(self.file, "w") as f:
                json.dump(self.empty, f, indent=4)
                database_dict = self.empty

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
        else:
            raise RecordAlreadyExists

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
        users = self.get_users_list_from_dict(database)

        if (chat_id in users):
            user_records = self.get_user_records_from_dict(database, chat_id)
        else:
            self.add_new_user_to_dict(database, chat_id)
            raise NewUserHasNoRecords

        return user_records

    def delete_record_by_record(self, chat_id, record):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (user_records == []):
            raise UserHasNoRecords
        else:
            if (record not in user_records):
                raise RecordNotFound
            else:
                database[self.users][0][chat_id].remove(record)
                self.dump(database)

    def update_record_by_index(self, chat_id, new_record, index):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (user_records == []):
            raise UserHasNoRecords
        else:
            database[self.users][0][chat_id][index] = new_record
            self.dump(database)

    def get_record_index_by_record(self, chat_id, record):
        index = None
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (user_records == []):
            raise UserHasNoRecords
        else:
            if (record not in database[self.users][0][chat_id]):
                raise RecordNotFound
            else:
                index = database[self.users][0][chat_id].index(record)

        return index

if __name__ == "__main__":
    pass
