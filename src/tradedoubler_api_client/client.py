import requests
import base64
import json
from os import path
from sys import argv
from tradedoubler_api_client.pending_sales import Pending_Sales
from tradedoubler_api_client.reporting import Reporting
# https://advertiserwip.docs.apiary.io/
# dokumentacja tego gówna
# luźno powiązana z rzeczywostością


class Tradedoubler:
    def __init__(self, credentials_path):
        credentials = self.__open_credentials(credentials_path)
        self.td_secret = credentials['td_secret']
        self.td_id = credentials['td_id']
        self.td_user_name = credentials['td_user_name']
        self.td_userpassword = credentials['td_userpassword']
        self.athu = self.__get_auth_token()

    @staticmethod
    def __open_credentials(credentials_path):
        source = path.dirname(path.abspath(argv[0]))
        with open(source + '\\' + credentials_path) as f:
            return json.load(f)

    def __get_auth_token(self):
        auth_bytes = f'{self.td_id}:{self.td_secret}'.encode('ascii')
        auth_code = base64.b64encode(auth_bytes)
        return auth_code.decode('ascii')

    def __get_bearer(self):
        values = f'start&grant_type=password&username={self.td_user_name}&password={self.td_userpassword}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.athu}'
        }
        r = requests.post('https://connect.tradedoubler.com/uaa/oauth/token', data=values, headers=headers)
        if r.status_code != 200:
            raise ConnectionError(f'{r.text}')
        return r.json()["access_token"]

    def get_request_header(self, content_type='application/json'):
        return {
            'Content-Type': content_type,
            'Authorization': f'Bearer {self.__get_bearer()}'
        }

    def get_my_user_details(self):
        r = requests.get('https://connect.tradedoubler.com/usermanagement/users/me', headers=self.get_request_header())
        if r.status_code != 200:
            raise ConnectionError(f'{r.text}')
        return r.json()

    def pending_sales(self):
        return Pending_Sales(self)

    def reporting(self):
        return Reporting(self)