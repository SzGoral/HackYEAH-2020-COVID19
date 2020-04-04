import json

from constants import DATABASE_PATH, LAT_KEY, LONG_KEY, DATETIME_KEY


def load_database():
    with open(DATABASE_PATH, "r") as f:
        data = json.load(f)
    return json2db(data)


def json2db(data):
    db = dict()
    for entry in data:
        lat, long, datetime = get_fixed_vals(entry)
        date, time = datetime.split("T")
        time = time[:2]
        all_day_loc = db.setdefault(date, dict())
        loc = all_day_loc.setdefault(time, set())
        loc.add((lat, long))
    return db


def get_fixed_vals(entry):
    return entry[LAT_KEY], entry[LONG_KEY], entry[DATETIME_KEY]


def get_all_day(year, month, day):
    year = str(year)
    month, day = [str(i).zfill(2) for i in [month, day]]
    db = load_database()
    return db[f"{year}{month}{day}"]


def get(year, month, day, hour=None):
    all_day = get_all_day(year, month, day)
    if hour is not None:
        return all_day[str(hour).zfill(2)]
    return all_day


def add_record(entry):
    with open(DATABASE_PATH, "r") as f:
        db = json.load(f)
    db.append(entry)
    with open(f"{DATABASE_PATH}.new", "w") as f:
        json.dump(db, f)
