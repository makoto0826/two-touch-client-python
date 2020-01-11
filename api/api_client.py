from model.information import Information
from model.user import User
from model.time_record import TimeRecord
from logging import getLogger
import json
import urllib.parse
import urllib.request

logger = getLogger(__name__)

class ApiClient(object):
    def __init__(self, options):
        self._options = options

    def get_information(self):
        try:
            headers = {
                'X-API-KEY': self._options.api_key
            }

            req = urllib.request.Request(
                self._options.get_information_url, headers=headers)

            with urllib.request.urlopen(req) as res:
                body = res.read()
                result = ApiResult(res.code, Information.from_json(body))

                return result

        except Exception as ex:
            logger.error(ex)
            raise ex

    def get_users(self):
        try:
            headers = {
                'X-API-KEY': self._options.api_key
            }

            req = urllib.request.Request(
                self._options.get_users_url, headers=headers)

            with urllib.request.urlopen(req) as res:
                body = res.read()
                result = ApiResult(res.code, User.from_json(body))

                return result

        except Exception as ex:
            logger.error(ex)
            raise ex

    def add_time_record(self, time_record):
        try:
            body = time_record.to_json()
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': self._options.api_key
            }

            method = 'POST'

            req = urllib.request.Request(
                self._options.add_time_record_url, data=body, method=method, headers=headers)

            with urllib.request.urlopen(req) as res:
                return ApiResult(res.code)

        except urllib.error.HTTPError as ex:
            return ApiResult(ex.code)
        except Exception as ex:
            logger.error(ex)
            raise ex


class ApiOptions(object):

    def __init__(self):
        self.api_key = None
        self.get_information_url = None
        self.get_users_url = None
        self.add_time_record_url = None


class ApiResult(object):

    def __init__(self, code, value=None):
        self.code = code
        self.value = value

    def is_ok(self):
        return self.code == 200

    def is_req_error(self):
        return self.code == 400

    def is_auth_error(self):
        return self.code == 401
    
    def is_server_error(self):
        return self.code == 500
