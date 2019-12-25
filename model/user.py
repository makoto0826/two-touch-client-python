import json


class User(object):

    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.cards = []
        self.current_card_id = None

    @staticmethod
    def from_json(data):
        json_dataList = json.loads(data)

        users = []

        for json_data in json_dataList:
            user = User()
            user.user_id = json_data['userId']
            user.user_name = json_data['userName']
            user.cards = json_data['cards']

            users.append(user)

        return users
