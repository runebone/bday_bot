from config import *
import copy
import json

# TODO: divide db fields into 2 categories: searchable and unsearchable
# make func, which will set unsearchable fields to their default values
# searchable - primary (name, date); unsearchable - secondary (notes, notify)
#def set_default_secondary_fields(record)
class Database:
    def __init__(self, file):
        self.file = file
        self.sample_record = Config.Database.sample_record
        self.record_fields = Config.Database.record_fields
        self.users = Config.Database.users
        self.sn = Config.Database.sn
        self.empty = {self.users: [{}], self.sn: []}

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

    def get_users_list_from_dict(self, database_dict):
        users_list = list(database_dict[self.users][0].keys())
        return users_list

    def add_user_record_to_dict(self, database_dict, chat_id_str, record_dict):
        database_records = [self.set_empty_notify_field(x) for x in
                    copy.deepcopy(database_dict[self.users][0][chat_id_str])]
        record = {i: j for i, j in record_dict.items()}
        record["notify_when"] = []
        if (record not in database_records):
            database_dict[self.users][0][chat_id_str].append(record_dict)
        else:
            raise RecordAlreadyExists

    def add_new_user_to_dict(self, database_dict, chat_id_str):
        database_dict[self.users][0][chat_id_str] = []

    def add_new_record(self, chat_id, record_dict):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id in users):
            self.add_user_record_to_dict(database, chat_id, record_dict)
        else:
            self.add_new_user_to_dict(database, chat_id)
            self.add_user_record_to_dict(database, chat_id, record_dict)

        self.dump(database)

    # NOTE: always return deep copies of structure.
    def get_user_records_from_dict(self, database_dict, chat_id_str):
        return copy.deepcopy(database_dict[self.users][0][chat_id_str])

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

    # NOTE: always edit/delete records by index inside; safer.
    def delete_record_by_record(self, chat_id, record):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)
            user_records = list(map(lambda x: self.set_empty_notify_field(x),
                                    user_records))
            record = {i: j for i, j in record.items()}
            record["notify_when"] = []

        if (user_records == []):
            raise UserHasNoRecords
        elif (record not in user_records):
            raise RecordNotFound
        else:
            index = self.get_record_index_by_record(chat_id, record)
            database[self.users][0][chat_id].pop(index)
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
            user_records = list(map(lambda x: self.set_empty_notify_field(x),
                                    user_records))
            record = {i: j for i, j in record.items()}
            record["notify_when"] = []

        if (user_records == []):
            raise UserHasNoRecords
        else:
            #if (record not in database[self.users][0][chat_id]):
            if (record not in user_records):
                raise RecordNotFound
            else:
                #index = database[self.users][0][chat_id].index(record)
                index = user_records.index(record)

        return index

    def get_record_by_index(self, chat_id, index):
        chat_id = str(chat_id)
        database = self.load()
        users = self.get_users_list_from_dict(database)

        if (chat_id not in users):
            raise NewUserHasNoRecords
        else:
            user_records = self.get_user_records_from_dict(database, chat_id)

        if (len(user_records) <= index):
            # raise Error
            pass
        else:
            record = user_records[index]

        return record

    def set_empty_notify_field(self, record):
        record["notify_when"] = []
        return record

    def create_new_single_notification(self, chat_id, date, text):
        database = self.load()

        # FIXME: field names -> config
        record = {
            "chat_id": chat_id,
            "date": date,
            "text": text
        }

        # field_name = "single_notificatoins"
        # if (field_name not in list(database.keys())):
            # database[field_name] = []

        database[self.sn].append(record)

        self.dump(database)

if __name__ == "__main__":
    db = Database(Config.Database.file)
    dbl = db.load()
    print(dbl)
    users = list(dbl[db.users][0].keys())
    for key in users:
        for user in dbl[db.users][0][key]:
            print(user["notify_when"])
