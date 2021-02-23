import requests
from twilio.rest import Client

# Twilio API
ACCOUNT_SID = ""
AUTH_TOKEN = ""
PHONE_NUMBER_TWILLIO = ""
PHONE_NUMBER = ""

# Stock API
COMPANY_NAME = "Tesla Inc"
STOCK = "TSLA"
STOCK_API = ""
STOCK_URL = "https://www.alphavantage.co/query"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API,
}

# News API
NEWS_API = ""
NEWS_URL = "https://newsapi.org/v2/everything"

news_parameters = {
    "qInTitle": COMPANY_NAME,
    "language": "en",
    "apiKey": NEWS_API,
    "sortBy": "publishedAt",
    "pageSize": 3
}


def stock_price_fluctuation():
    """
    :return:  The net change from yesterday close price stock and before yesterday
    """
    response = requests.get(url=STOCK_URL, params=stock_parameters)
    response.raise_for_status()
    stock_data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in stock_data.items()]
    stock_yesterday = float(data_list[0]["4. close"])
    stock_before_yesterday = float(data_list[1]["4. close"])

    net_change_percent = ((stock_yesterday - stock_before_yesterday) / stock_before_yesterday) * 100

    return net_change_percent


def get_news():
    """
    :return: A nested list news[[title, description]]
    """
    response = requests.get(url=NEWS_URL, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    news = []

    for article in news_data["articles"]:
        news.append([article["title"], article["description"]])

    return news


stock_prices = stock_price_fluctuation()

if stock_prices >= 5.0 or stock_prices <= -5.0:
    interesting_news = get_news()

    # Sending SMS
    up_down_emoji = "🔺" if stock_prices >= 0 else "🔻"
    for new in interesting_news:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages\
            .create(body=f"TSLA: {up_down_emoji}{round(stock_prices,2)}%\n"
                         f"Headline: {new[0]}.\n"
                         f"Brief: {new[1]}",
                    from_=PHONE_NUMBER_TWILLIO,
                    to=PHONE_NUMBER
                    )
        print(message.status)
