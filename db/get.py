import json

from constant import DATABASE_FILE

# and from package core we call
# from db import get
# now we don care about how the get function get the data from anywhere
def get():
    with open(DATABASE_FILE, "r") as db:
        data = json.load(db)
        return data[0]["long"]


