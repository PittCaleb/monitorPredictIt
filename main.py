import requests
import json
import sys
import getopt


class PredictIt:
    def __init__(self):
        self.base_url = 'https://www.predictit.org/api'
        self.all_endpoint = 'marketdata/all/'
        self.invid_endpoint = 'markets/'
        self.flag_range = None
        self.flagged_only = False
        self.flag = '*****'
        self.show_url = False

    def get(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        response = requests.request("GET", url, headers=None, data=None)
        if response.status_code == 200:
            return json.loads(response.content)

        return None

    def in_range(self, yes_price, no_price):
        return True if self.flag_range and yes_price in self.flag_range or no_price in self.flag_range else False

    def display(self, markets):
        for market in markets:
            if market['status'] == 'Open':
                url = f"\n{' ':6}{market['url']}" if self.show_url else ''
                header = f"{market['shortName']:70} ({market['id']}){url}"
                header_printed = False
                if not self.flagged_only:
                    print(header)

                for contract in market['contracts']:
                    if contract['status'] == 'Open':
                        yes_price = contract['bestBuyYesCost'] if contract['bestBuyYesCost'] else float(0)
                        no_price = contract['bestBuyNoCost'] if contract['bestBuyNoCost'] else float(0)
                        if not self.flagged_only or self.in_range(yes_price, no_price):
                            if self.flagged_only and not header_printed:
                                print(header)
                                header_printed = True
                            flag = self.flag if not self.flagged_only and self.in_range(yes_price, no_price) else ''
                            print(
                                f"{' ':6}{contract['shortName']:40}  Yes: {yes_price:5.2f} No: {no_price:5.2f} {flag}")

    def show_all_markets(self):
        all_markets = pi.get(pi.all_endpoint)
        pi.display(all_markets['markets'])
        print('\nAll data sourced from http://www.PredictIt.org/ and is for non-commercial use.')

    def print_help(self):
        print('main.py -h --low=[price] --high=[price] --u,url')
        print('    -h help')
        print('    --low=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    --high=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    -f --flagged  Only show flagged rows')
        print('    -u, --url Show market URL')

    def get_params(self, argv):
        try:
            opts, args = getopt.getopt(argv, 'hfu', ['low=', 'high=', 'flagged', 'url', 'urls'])
        except getopt.GetoptError:
            self.print_help()
            sys.exit(2)

        flag_low = None
        flag_high = None

        for opt, arg in opts:
            if opt == '-h':
                self.print_help()
                sys.exit()
            elif opt == '--low':
                try:
                    flag_low = float(arg)
                    if not 0 <= flag_low <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
                    sys.exit(2)
            elif opt == '--high':
                try:
                    flag_high = float(arg)
                    if not 0 <= flag_high <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
                    sys.exit(2)
            elif opt in ('-f', '--flagged'):
                self.flagged_only = True
            elif opt in ('-u', '--url', '--urls'):
                self.show_url = True

        if flag_low or flag_high:
            if (flag_low and not flag_high) or (flag_high and not flag_low):
                print('Must set both LOW and HIGH flag values if setting one')
                self.print_help()
                sys.exit(2)
            self.flag_range = [flag_low, flag_high]


pi = PredictIt()
pi.get_params(sys.argv[1:])
pi.show_all_markets()
