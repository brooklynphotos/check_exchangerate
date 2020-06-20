# check exchangerate
Checks the exchange rate and notify if things are interesting

## test runs
`python check_xchange_rates.py <exchange_rate_api_url>`

## URLs
### test
`{"exchange_url": "http://gzmockendpoints.s3-website-eu-west-1.amazonaws.com/exchange_rate.json"}`
### real
`{"exchange_url": "https://openexchangerates.org/api/latest.json?app_id=eb33250b17004cce8de61e6d6e331e6c&symbols=CHF"}`