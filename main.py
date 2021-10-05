from dotenv import dotenv_values
import requests
from datetime import date, timedelta
from twilio.rest import Client

CRYPTO_CURRENCY = "ETH"
CRYPTO_CURRENCY_NAME = "Ethereum"
THRESHOLD = 0.5
config = dotenv_values(".env")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by N% between yesterday and the day before yesterday then print("Get News").
# N: int

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

def __date_to_string(datetime_object):
  return datetime_object.strftime("%Y-%m-%d")

def __get_info(some_date):
  return data["Time Series (Digital Currency Daily)"][__date_to_string(some_date)]

def __get_closing_price(some_date):
  return __get_info(some_date)["4a. close (USD)"]

def __get_price_diff(some_date, some_other_date):
  return float(__get_closing_price(some_date)) - float(__get_closing_price(some_other_date))

def get_pct_diff(initial, final):
  return (__get_price_diff(initial, final)) / float(__get_closing_price(initial)) * 100

price_difference_pct = get_pct_diff(yesterday, day_before_yesterday)


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the CRYPTO_CURRENCy_NAME. 

news_url = "https://newsapi.org/v2/everything"
querystring_news = {
    "q": CRYPTO_CURRENCY_NAME.lower(),
    "apiKey": config["NEWS_API_KEY"]

}

ARTICLES_NUMBER = 3

def show_news(q):  
  response = requests.get(url=news_url, params=querystring_news)
  response.raise_for_status()

  data = response.json()
  articles = data["articles"]

  title_content = [f"{article['title']} \n {article['content']}" for article in articles[:ARTICLES_NUMBER]]
  return title_content

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_message():
  account_sid=config["TWILIO_ACCOUNT_SID"]
  auth_token=config["TWILIO_AUTH_TOKEN"]
  client = Client(account_sid, auth_token)

  message = client.messages \
                  .create(
                      body=f"{show_news(querystring_news['q'])}",
                      from_=config["from_"],
                      to=config["to"]
                  )
  print(message.status)

if price_difference_pct < -THRESHOLD or price_difference_pct > THRESHOLD:
  send_message()
else:
   print("Negligible difference")


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

