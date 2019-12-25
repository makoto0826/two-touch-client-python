import json


class Information(object):

    def __init__(self):
        self.version = Version()

    def to_json(self):
        return json.dumps({
            'version': {
                'usersVersion': self.version.users_version
            }
        }).encode('utf-8')

    @staticmethod
    def from_json(data):
        json_data = json.loads(data)
        info = Information()
        info.version.users_version = json_data['version']['usersVersion']

        return info


class Version(object):
    def __init__(self):
        self.users_version = None
