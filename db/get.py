import json

from constants import DATABASE_FILE


def get_all_day(year, month, day):
    year, month, day = [str(i) for i in [year, month, day]]
    with open(DATABASE_FILE, "r") as db:
        data = json.load(db)
        return data[year][month][day]

def get(year, month, day, hour=None):
    all_day = get_all_day(year, month, day)
    if hour is not None:
        return all_day[str(hour)]
    return all_day



if __name__ == "__main__":
    x = get(2020, 4, 3, 21)
    print(x)
    x = get(2020, 4, 3)
    print(x)
