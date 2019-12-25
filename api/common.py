import os
import json
from api.api_client import ApiOptions

API_PATH = './data/api.json'

def get_options():
    file = open(API_PATH)
    text = ''
    
    for line in file.readlines():
        text += line

    data = json.loads(text)

    opitons = ApiOptions()
    opitons.api_key = data['api_key']
    opitons.get_users_url = data['get_users_url']
    opitons.get_information_url = data['get_information_url']
    opitons.add_time_record_url = data['add_time_record_url']

    return opitons

