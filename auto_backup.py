from time import sleep
from copy import deepcopy
import os
import json
import datetime

BOT_DIR = "bot_dir"
BOT_DB_FILE = "database.json"

DATE_FMT = "%y%m%d-%H%M%S"
BACKUP_DIR = "backup_dir"
BACKUP_FILE = f"db_{DATE_FMT}.json"

def gen_backup_filename():
    return datetime.datetime.now().strftime(BACKUP_FILE)

def get_latest_backup_filename():
    return os.popen(f"ls {BACKUP_DIR} | tail -n 1").read()[:-1]


class BdayBotDB:
    def __init__(self, database: dict):
        self.init_db = database
        self.db = self.init_db["user_data"][0]
        self.users = list(self.db.keys())
        # XXX: self.sn = self.init_db["single_notifications"]

    def get_user_records(self, user_id: str) -> list:
        return self.db[user_id]


def merge(db_merge_in: BdayBotDB, db_merge_from: BdayBotDB) -> BdayBotDB:
    db_merged = deepcopy(db_merge_in)

    for user, records in db_merge_from.db.items():

        USER_IS_NEW = (user not in db_merge_in.users)

        if (USER_IS_NEW):
            db_merged.db[user] = records
        else:
            # XXX: consider user hasn't deleted any records manually
            # (we merge only if database erased itself anyway)
            USER_HAS_SAME_RECORDS = all(x in db_merge_in.get_user_records(user) for x in records)

            if (not USER_HAS_SAME_RECORDS):
                new_records = [r for r in records if r not in db_merge_in.get_user_records(user)]
                db_merged.db[user] += new_records

    return db_merged


MINUTE = 60
HOUR = 60 * 60

DB_CURRENT = f"{BOT_DIR}/{BOT_DB_FILE}"

print("Auto-backup job has started.")

while True:
    DB_LATEST_BACKUP = BACKUP_DIR + "/" + get_latest_backup_filename()

    with open(DB_CURRENT) as current, open(DB_LATEST_BACKUP) as latest_backup:
        db_current_dict = json.load(current)
        db_latest_backup_dict = json.load(latest_backup)

    db_current = BdayBotDB(db_current_dict)
    db_latest_backup = BdayBotDB(db_latest_backup_dict)

    DATABASE_ERASED_ITSELF = not all(user in db_current.users for user in db_latest_backup.users)
    DATABASES_ARE_DIFFERENT = (db_current.db != db_latest_backup.db)

    if (DATABASES_ARE_DIFFERENT):
        if (DATABASE_ERASED_ITSELF):
            # print("Database erased itself!")
            db_merged = merge(db_latest_backup, db_current)
            with open(DB_CURRENT, "w") as file:
                json.dump(db_merged.init_db, file, indent=4)
            db_current = db_merged
            # print("Databases have been merged together.")

        backup_file = BACKUP_DIR + "/" + gen_backup_filename()
        with open(backup_file, "w") as file:
            json.dump(db_current.init_db, file, indent=4)
        # print("Backup file has been created.")

    sleep(1 * MINUTE)
