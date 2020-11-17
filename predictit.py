import requests
import json
import sys

from copy import copy
from time import sleep
from datetime import datetime

from setup import Setup
from sms import SMS


class PredictIt:
    def __init__(self):
        self.base_url = 'https://www.predictit.org/api/marketdata/'
        self.all_endpoint = 'all/'
        self.indiv_endpoint = 'markets/'
        self.flag = '*****'

        self.sms_api_key = None

        self.flag_range = None
        self.flagged_only = False

        self.show_url = False
        self.keyword = None

        self.monitor = False
        self.monitor_market = None
        self.period = 30 * 60
        self.alert_sms_number = None

    def get(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        response = requests.request("GET", url, headers=None, data=None)
        if response.status_code == 200:
            return json.loads(response.content)

        return None

    def in_range(self, yes_price, no_price):
        return True if (self.flag_range is None or (self.flag_range is not None and (
                (self.flag_range[0] <= yes_price <= self.flag_range[1]) or (
                self.flag_range[0] <= no_price <= self.flag_range[1])))) else False

    def in_search(self, phrase):
        return True if self.keyword is None or (self.keyword and self.keyword in phrase.lower()) else False

    def display_single_market(self, market):
        if market['status'] == 'Open':
            url = f"\n{' ':6}{market['url']}" if self.show_url else ''
            header = f"{market['shortName']:70} ({market['id']}){url}"

            header_printed = False
            if not self.flagged_only and self.keyword is None:
                print(header)

            for contract in market['contracts']:
                if contract['status'] == 'Open':
                    yes_price = contract['bestBuyYesCost'] if contract['bestBuyYesCost'] else float(0)
                    no_price = contract['bestBuyNoCost'] if contract['bestBuyNoCost'] else float(0)
                    if not self.flagged_only or (
                            self.in_range(yes_price, no_price) and self.in_search(contract['shortName'])) or (
                            self.in_range(yes_price, no_price) and self.in_search(market['shortName'])):
                        if self.flagged_only and not header_printed:
                            print(header)
                            header_printed = True
                        flag = self.flag if not self.flagged_only and self.in_range(yes_price, no_price) else ''
                        print(
                            f"{' ':6}{contract['shortName']:40}  Yes: {yes_price:5.2f} No: {no_price:5.2f} {flag}")

    def display(self, markets):
        for market in markets:
            self.display_single_market(market)

    def show_all_markets(self):
        all_markets = self.get(self.all_endpoint)
        self.display(all_markets['markets'])
        print('\nAll data sourced from http://www.PredictIt.org/    and is for non-commercial use.')

    def get_single_market(self, market_id):
        market = self.get(f'{self.indiv_endpoint}{market_id}')
        return market

    def get_market_ids(self):
        markets = self.get(self.all_endpoint)
        return [market['id'] for market in markets['markets']]

    def contracts_different(self, last, current):
        # ToDo: Compare only contract values, not extranous information, such as date
        # ToDo: Major issue, monitoring a market does not work until this is done!
        if last != current:
            return True

        return False

    def compare_market_data(self, last, current):
        now = datetime.now().strftime("%I:%M:%S")
        if self.contracts_different(last, current):
            if last:
                print(f'\n{self.flag} Change in contracts found at {now} {self.flag}\n')
                SMS(predict_it.sms_api_key).sendSMS(predict_it.alert_sms_number,
                                                    f"PredictIt Contract change found for {current['shortName']}")
            else:
                print(f'\nInitial contracts found at {now} {self.flag}\n')

            self.display_single_market(current)
        else:
            print(f'{now} Contract data unchanged for market')

        return copy(current)

    def flag_new_ids(self, last, current):
        now = datetime.now().strftime("%I:%M:%S")
        if last and last != current:
            new_markets = list(set(current).difference(last))
            plural = 's' if len(new_markets) > 1 else ''
            print(f'\n{self.flag} New market{plural} found at {now} {self.flag}\n')
            for market_id in new_markets:
                market_data = self.get_single_market(market_id)
                SMS(predict_it.sms_api_key).sendSMS(predict_it.alert_sms_number,
                                                    f"New PredictIt Market found: {market_data['shortName']}")
                self.display_single_market(market_data)
        else:
            print(f'{now} No new markets found')

        return copy(current)

    def monitor_markets(self):
        last_market_ids = None
        last_market_data = None
        while 1:
            if self.monitor_market:
                # Monitor for single market for contract changes
                curr_market_data = self.get_single_market(self.monitor_market)
                last_market_data = self.compare_market_data(last_market_data, curr_market_data)
            else:
                # Monitor for NEW markets coming on-boar
                curr_market_ids = self.get_market_ids()
                last_market_ids = self.flag_new_ids(last_market_ids, curr_market_ids)

            sleep(self.period)


predict_it = PredictIt()
Setup(sys.argv).get_params(predict_it)

if predict_it.monitor:
    predict_it.monitor_markets()
else:
    predict_it.show_all_markets()
