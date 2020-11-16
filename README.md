# monitorPredictIt
Monitor the Predict It political wagering markets

## Usage
```bash
python predictit.py -h --low=[price] --high=[price] --key=[keyword] --u,url
    -l [price[, --low=[price] where price in range of 0.00 - 1.00 (optional)
    -h [price], --high=[price] where price in range of 0.00 - 1.00 (optional)
    -k [keyword], --key=[keyword], --keyword=[keyword] Keyword to search for in contracts
    -f --flagged  Only show flagged rows
    -u, --url Show market URL
    -m, --monitor Monitor for new markets
    -i, --id id to monitor
    -p [mins], --period=[mins] Period of time between monitoring cycles
    --help help
```

## Examples
Pull live market data from PredictIt.org
```bash
python predictit.py
```
...flagging data that meets range criteria
```bash
python predictit.py --low .75 --high .85
```
...and only output those lines
```bash
python predictit.py --low .75 --high .85 --flagged
```
...that includes a specific keyword in the contract name
```bash
python predictit.py --keyword=pence
```
...and falls withing your range criteria
```bash
python predictit.py --keyword=pence --low=.6 --high=.8
```
...that includes a specific keyword in the market name
```bash
python predictit.py -k interior
```
...and also falls within your range criteria
```bash
python predictit.py -k interior -l .2 -h .3
```
Output the PredictIt.org URL for the given market
```bash
python predictit.py --low .8 --high .9 --url
```
Monitor for newly added markets
```bash
--monitor
```
... every [xxx] minutes
```bash
--monitor -period 60
```
Monitor single market for updated contract values
```bash
--monitor --id=6976
```



## Requirements
You may need to install the following packages to your virtual environment:  
`response` 


## ToDo List
* ~~--urls - make display of URLS off by default, flag to turn on~~
* ~~Keyword searching for contracts~~
  * ~~Combined with range searching~~
* ~~Keyword searching for markets~~
  * ~~Combined with range searching~~
* ~~Monitor specific market/contracts over time~~
  * ~~Alert for price change~~
  * BUG: Only compare values we care about, not entire market record
  * Integrate with SMS/Email capabilities 
* ~~Monitor for new markets coming online~~
  * Integrate with SMS/Email capabilities
* Better user interface, i.e. non-command-line, potentially interactive

## Notes
This is a work in progress.  It was done merely as an academic exercise to have fun.
PredictIt.org is not meant to be a gambling / money making site

If you have any ideas for new features, pls let me know, would be open to integrating

## Contact
Caleb Cohen  
Caleb@Hail2Pitt.org  
https://github.com/PittCaleb  
Twitter: [@PittCaleb](https://www.twitter.com/PittCaleb)


  