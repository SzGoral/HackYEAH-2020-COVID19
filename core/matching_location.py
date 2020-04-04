from math import sqrt

from constants import GEOLOCATION_THRESHOLD
from core.manage_data import json2db, load_database


def get_distance(x1, y1, x2, y2):
    x1, y1, x2, y2 = [float(i) for i in [x1, y1, x2, y2]]
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def is_near(x1, y1, x2, y2):
    return get_distance(x1, y1, x2, y2) < GEOLOCATION_THRESHOLD


def get_match(user_data, data):
    matched = list()
    for user_point in user_data:
        for point in data:
            if is_near(x1=user_point[0],
                       y1=user_point[1],
                       x2=point[0],
                       y2=point[1]):
                matched.append(user_point)
    return matched


def get_matching_locations(data):
    user_db = json2db(data)
    db = load_database()
    matched_loc = list()
    for date in user_db.keys():
        date_db = db.get(date, None)
        if date_db is None:
            continue
        for hour in user_db[date].keys():
            hour_db = date_db.get(hour, None)
            if hour_db is None:
                continue
            match = get_match(user_db[date][hour], hour_db)
            if bool(match):
                matched_loc.append({date: {hour: set(match)}})
    return matched_loc
