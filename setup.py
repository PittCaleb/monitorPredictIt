import sys
import getopt


class Setup:
    def __init__(self, argv):
        self.app_name = argv[0]
        self.args = argv[1:]
        self.short_opts = 'mfuk:l:h:p:i:'
        self.long_opts = ['id=', 'period=', 'monitor', 'key=', 'keyword=', 'low=', 'high=', 'flagged', 'url', 'urls', 'help']

    def print_help(self, e=None):
        if e:
            print(f'\n{e}\n\n')
        print(f'python {self.app_name} --help --monitor --low=[price] --high=[price] --key=[keyword] --u,url')
        print('    -l [price[, --low=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    -h [price], --high=[price] where price in range of 0.00 - 1.00 (optional)')
        print('    -k [keyword], --key=[keyword], --keyword=[keyword] Keyword to search for in contracts')
        print('    -f --flagged  Only show flagged rows')
        print('    -u, --url Show market URL')
        print('    -m, --monitor Monitor for new markets')
        print('    -i, --id id to monitor')
        print('    -p [mins], --period=[mins] Period of time between monitoring cycles')
        print('    --help help')

        sys.exit()

    def get_params(self, predict_it):
        try:
            opts, args = getopt.getopt(self.args, self.short_opts, self.long_opts)
        except getopt.GetoptError:
            self.print_help()

        flag_low = None
        flag_high = None

        for opt, arg in opts:
            if opt == '--help':
                self.print_help()
            elif opt in ['-l', '--low']:
                try:
                    flag_low = float(arg)
                    if not 0 <= flag_low <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
            elif opt in ['-h', '--high']:
                try:
                    flag_high = float(arg)
                    if not 0 <= flag_high <= 1:
                        raise ValueError
                except ValueError:
                    self.print_help()
            elif opt in ('-f', '--flagged'):
                predict_it.flagged_only = True
            elif opt in ('-u', '--url', '--urls'):
                predict_it.show_url = True
            elif opt in ('-k', '--key', '--keyword'):
                predict_it.keyword = arg.lower()
                predict_it.flagged_only = True
            elif opt in ('-m', '--monitor'):
                predict_it.monitor = True
            elif opt in ('-i', '--id'):
                predict_it.monitor_market = arg
            elif opt in ('-p', '--period'):
                try:
                    predict_it.period = int(arg) * 60
                except ValueError:
                    self.print_help(e='Period must be an integer')

        if flag_low or flag_high:
            if (flag_low and not flag_high) or (flag_high and not flag_low):
                self.print_help(e='Must set both LOW and HIGH flag values if setting one')
            predict_it.flag_range = [flag_low, flag_high]
