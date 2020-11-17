import urllib.request
import urllib.parse
from os import environ
import requests
import json


class SMS:
    def __init__(self, sms_api_key):
        self.base_url = 'https://rest-api.d7networks.com/'
        self.endpoint = 'secure/send'

        if sms_api_key:
            self.apikey = sms_api_key
        elif environ.get('D7_API_KEY') is not None:
            self.apikey = environ.get('D7_API_KEY')
        else:
            self.apikey = None

        self.sms_recipient = None
        if environ.get('SMS_RECIPIENT') is not None:
            self.sms_recipient = environ.get('SMS_RECIPIENT')

        self.sender = "PredictIt Monitor Service"

    def sendSMS(self, number, message):
        if self.apikey and (number or self.sms_recipient) and message:
            url = f'{self.base_url}{self.endpoint}'

            number = number if number else self.sms_recipient

            payload = json.dumps({"to": number, "content": message, "from": self.sender})
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic ' + self.apikey}
            response = requests.request("POST", url, headers=headers, data=payload)
            if 'Success' in json.loads(response.content)['data']:
                return True

        return False
