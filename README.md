# monitorPredictIt
Monitor the Predict It political wagering markets

## Usage
```bash
python predictit.py

python predictit.py --low .75 --high .85
python predictit.py --low .75 --high .85 --flagged

python predictit.py --keyword=pence
python predictit.py --keyword=pence --low=.6 --high=.8

python predictit.py --low .8 --high .9 --url

```

## Requirements
You may need to install the following packages to your virtual environment:  
`response` 

## Description
Pulls live market data from PredictIt.org

Will optionally flag contracts with prices within your range (low, high)

Will optionally only output markets and contracts within your range

Will optionally only output markets with contracts with your search term

Will optionally only output markets with contracts with your search term and requested range

Will optionally output the PredictIt.org URL for the shown market

## ToDo List
* ~~--urls - make display of URLS off by default, flag to turn on~~
* ~~Keyword searching for contracts~~
  * ~~Combined with range searching~~
* Keyword searching for markets
  * Combined with range searching
* Monitor specific market/contracts over time
  * Alert for price change
  * Integrate with SMS capabilities 
* Monitor for new markets coming online
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


  