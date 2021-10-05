from dotenv import dotenv_values
import requests
from datetime import date, timedelta

CRYPTO_CURRENCY = "ETH"
CRYPTO_CURRENCY_NAME = "Ethereum"
config = dotenv_values(".env")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

url = "https://alpha-vantage.p.rapidapi.com/query"
querystring = {"function":"DIGITAL_CURRENCY_DAILY","symbol":CRYPTO_CURRENCY, "market":"USD"}
headers = {
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
    'x-rapidapi-key': config['X_RAPIDAPI_KEY']
    }
response = requests.get(url=url, headers=headers, params=querystring)
response.raise_for_status()
data = response.json()

today = date.today()
time_interval = timedelta(days=1)
yesterday = today - time_interval
day_before_yesterday = yesterday - time_interval

yesterday_string = yesterday.strftime("%Y-%m-%d")
day_before_yesterday_string = day_before_yesterday.strftime("%Y-%m-%d")
info_yesterday = data["Time Series (Digital Currency Daily)"][yesterday_string]
price_yesterday = info_yesterday["4a. close (USD)"]

info_day_before_yesterday = data["Time Series (Digital Currency Daily)"][day_before_yesterday_string]
price_day_before_yesterday = info_day_before_yesterday["4a. close (USD)"]
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
