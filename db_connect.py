import requests
import json
from collections import defaultdict


def nested_dict():
    return defaultdict(nested_dict)


def back_to_dict(data):
    data = json.loads(json.dumps(data))
    return data


class DbConnection:

    @staticmethod
    def get_data():
        header = {'secret-key': '$2b$10$Y4Lpa7zc2GEhvmrntjESyuhD0AIXuN6uX37wBV4mQFCrURtjwWleG'}
        url = 'https://api.jsonbin.io/b/5e87e7d68841e979d0fd4d82'
        req = requests.get(url, headers=header)
        return req.text


    @staticmethod
    def push_data(single_pos):
        header = {'Content-Type': 'application/json', 'secret-key': '$2b$10$Y4Lpa7zc2GEhvmrntjESyuhD0AIXuN6uX37wBV4mQFCrURtjwWleG'}
        url = 'https://api.jsonbin.io/b/5e87a1d541019a79b61d056f'
        req = requests.put(url, data=single_pos, headers=header)
        if req.status_code == 200:
            return True
        else:
            return False


class LocalDbConnection:
    ADDRESS = r'db.json'

    @staticmethod
    def _laod_db():
        try:
            with open(LocalDbConnection.ADDRESS, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return dict()

    @staticmethod
    def _save_db(db):
        with open(LocalDbConnection.ADDRESS, 'w') as file:
            json.dump(db, file)

    @staticmethod
    def get_data(year_range=(1999, 2050), month_range=(1, 12), day_range=(1, 31), hour_range=(0, 23), raw=False):
        raw_data = LocalDbConnection._laod_db()
        data = nested_dict()
        for year, year_data in raw_data.items():
            if year_range[0] < int(year) < year_range[1]:
                for month, month_data in year_data.items():
                    if month_range[0] < int(month) < month_range[1]:
                        for day, day_data in month_data.items():
                            if day_range[0] < int(day) < day_range[1]:
                                for hour, position in day_data.items():
                                    if hour_range[0] < int(hour) < hour_range[1]:
                                        data[year][month][day][hour] = position
        if raw:
            return data
        return back_to_dict(data)

    @staticmethod
    def put_data(year, month, day, hour, long, lat):
        db = LocalDbConnection.get_data(raw=True)
        try:
            db[str(year)][str(month)][str(day)][str(hour)]["long"].append(long)
            db[str(year)][str(month)][str(day)][str(hour)]["lat"].append(lat)
        except:
            db[str(year)][str(month)][str(day)][str(hour)] = {"long": [str(long)], "lat": [str(lat)]}
        LocalDbConnection._save_db(db)


def put_fakes():
    from pprint import pprint
    pprint(LocalDbConnection.get_data())

    from random import randint
    for _ in range(1000):
        month = randint(3, 4)
        day = randint(1, 30)
        hour = randint(0, 23)
        lng = f"19.94{randint(0, 9000)}"
        lat = f"50.04{randint(0, 9000)}"
        LocalDbConnection.put_data("2020", month, day, hour, lng, lat)

    pprint(LocalDbConnection.get_data())