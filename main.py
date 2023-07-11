import requests
import math
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_KEY = "IOXDYY9GT799DG9E"
NEWS_KEY = "47c45c5b42674cbeb9c867af94ba9d49"

SEND_TO = '+27711580057'
SEND_FROM = '+12283385024'

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY
}

def send_sms(lst, direction):
    account_sid = "ENTER ACCOUNT SID HERE"
    auth_token = "ENTER TOKEN HERE"

    client = Client(account_sid, auth_token)

    for (headline, desc) in lst:
        print(f"{STOCK_NAME}: {direction} \nHeadline: {headline} \nDescription: {desc}\n\n\n")
        message = client.messages \
            .create(
            body=f"{STOCK_NAME}: {direction} \nHeadline: {headline} \nDescription: {desc}",
            from_=SEND_FROM,
            to=SEND_TO
        )

    print(message.status)

def news_articles(before_yesterday, yesterday):
    news_parameters = {
        "q": COMPANY_NAME,
        "from": before_yesterday,
        "to": yesterday,
        "sortBy": "popularity",
        "apiKey": NEWS_KEY
    }

    url = requests.get(NEWS_ENDPOINT, params=news_parameters)
    data = url.json()
    print(data)

def stock_prices():
    url = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    data = url.json()
    print(data)
    yesterday = [(key, value) for (key, value) in data['Time Series (Daily)'].items()]

    closing_price = float(yesterday[0][1]['4. close'])
    previous_price = float(yesterday[1][1]['4. close'])

    positive_diff = round(math.fabs(closing_price - previous_price),2)
    percentage = round((1-(closing_price/previous_price))*100, 2)

    if positive_diff == 0.00 and percentage == 0.00:
        direction = f"={positive_diff}%"
    elif positive_diff > 0.00 and percentage > 0.00:
        direction = f"🔺{positive_diff}%"
    else:
        direction = f"🔻{positive_diff}%"

    news = news_articles(previous_price, closing_price)

    send_sms(news, direction)

stock_prices()
