import requests
import json


class DbConnection:

    @staticmethod
    def get_data():
        header = {'secret-key': '$2b$10$Y4Lpa7zc2GEhvmrntjESyuhD0AIXuN6uX37wBV4mQFCrURtjwWleG'}
        url = 'https://api.jsonbin.io/b/5e87a1d541019a79b61d056f'
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


print(DbConnection.get_data())


