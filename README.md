# monitorPredictIt
Monitor the Predict It political wagering markets

## Usage
```bash
python main.py
python main.py --low .75 --high .85 --flagged
python main.py --low .8 --high .9
```

## Requirements
You may need to install the following packages to your virtual environment:  
`response` 

## Description
Pulls live market data from PredictIt.org
Will optionally flag contracts with prices within your range (low, high)
Will optionally only output markets and contracts within your range

## ToDo List
* --urls - make display of URLS off by default, flag to turn on
* Monitor specific market/contracts over time
  * alert for price change
  * integrate with SMS capabilities 
* Different interface, i.e. non-command-line

## Notes
This is a work in progress.  It was done merely as an academic exercise to have fun.
PredictIt.org is not meant to be a gambling / money making site

If you have any ideas for new features, pls let me know, would be open to integrating

## Contact
Caleb Cohen  
Caleb@Hail2Pitt.org  
https://github.com/PittCaleb  
Twitter: [@PittCaleb](https://www.twitter.com/PittCaleb)


  