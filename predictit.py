import requests
import json
import sys
import getopt


class Setup:
    def __init__(self, argv):
        self.app_name = argv[0]
        self.args = argv[1:]
        self.predict_it = PredictIt()
        self.short_opts = 'fuk:l:h:'
        self.long_opts = ['key=', 'keyword=', 'low=', 'high=', 'flagged', 'url', 'urls', 'help']

    def print_help(self):
        print(f'python {self.app_name} -h --low=[price] --high=[price] --key=[keyword] --u,url')
        print('    -l [price[, --low=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    -h [price], --high=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    -k [keyword], --key=[keyword], --keyword=[keyword] Keyword to search for in contracts')
        print('    -f --flagged  Only show flagged rows')
        print('    -u, --url Show market URL')
        print('    --help help')

    def get_params(self):
        try:
            opts, args = getopt.getopt(self.args, self.short_opts, self.long_opts)
        except getopt.GetoptError:
            self.print_help()
            sys.exit(2)

        flag_low = None
        flag_high = None

        for opt, arg in opts:
            if opt == '--help':
                self.print_help()
                sys.exit()
            elif opt in ['-l', '--low']:
                try:
                    flag_low = float(arg)
                    if not 0 <= flag_low <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
                    sys.exit(2)
            elif opt in ['-h', '--high']:
                try:
                    flag_high = float(arg)
                    if not 0 <= flag_high <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
                    sys.exit(2)
            elif opt in ('-f', '--flagged'):
                self.predict_it.flagged_only = True
            elif opt in ('-u', '--url', '--urls'):
                self.predict_it.show_url = True
            elif opt in ('-k', '--key', '--keyword'):
                self.predict_it.keyword = arg.lower()
                self.predict_it.flagged_only = True

        if flag_low or flag_high:
            if (flag_low and not flag_high) or (flag_high and not flag_low):
                print('Must set both LOW and HIGH flag values if setting one')
                self.print_help()
                sys.exit(2)
            self.predict_it.flag_range = [flag_low, flag_high]

        return self.predict_it


class PredictIt:
    def __init__(self):
        self.base_url = 'https://www.predictit.org/api'
        self.all_endpoint = 'marketdata/all/'
        self.indiv_endpoint = 'markets/'
        self.flag = '*****'

        self.flag_range = None
        self.flagged_only = False
        self.show_url = False
        self.keyword = None

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

    def display(self, markets):
        for market in markets:
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

    def show_all_markets(self):
        all_markets = self.get(self.all_endpoint)
        self.display(all_markets['markets'])
        print('\nAll data sourced from http://www.PredictIt.org/    and is for non-commercial use.')


predict_it = Setup(sys.argv).get_params()
predict_it.show_all_markets()
