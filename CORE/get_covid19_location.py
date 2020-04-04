import json
from pprint import pprint
path_to_json = r"C:\HackYEAH_2020\test_db.json"

with open(path_to_json, 'r') as file:
    parsed_json :dict= json.load(file)

pprint(parsed_json)

year = '2020'
month = '04'
day = '03'
hour = '21'

for key_year, value_year in parsed_json.items():
    if str(key_year) == year:
        for key_month, value_month in value_year.items():
            pass