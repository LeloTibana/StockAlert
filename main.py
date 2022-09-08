import requests
from twilio.rest import Client

# Open Weather API
TWILIO_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
TWILIO_API = "fac37b648c07c4c81e112fb8e3bdda07"
TWILIO_SID = "AC1c5f7a6018cc8a778800f5cecb8e8f76"
TWILIO_AUTH_TOKEN = "638213acd9b80fbb9b12ae0917b966a0"
MESSAGE_SID = "MG39088e561d1c9d2e2e5616525cbba421"




STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "DT084IS33BUZQBSU"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "b75082bfe51d4480b1e2852c86be7ad3"


url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=DT084IS33BUZQBSU"
response = requests.get(url)
response.raise_for_status()
data = response.json()
daily_prices = data["Time Series (Daily)"]

# June 29th Closing Price
june_29 = daily_prices["2022-06-29"]
june_29_closing = june_29["4. close"]
yesterday_closing = float(june_29_closing)
# yesterday_price = [new_value for (key, value) in data.items()]

# June 28th Closing Price
june_28 = daily_prices["2022-06-28"]
june_28_closing = june_28["4. close"]
day_bfor_yesterday = float(june_28_closing)

# Positive difference between prices
pos_diff = yesterday_closing - day_bfor_yesterday
up_down = None
if pos_diff > 0:
    up_down = "📈"
else:
    up_down = "📉"

# Percentage Difference
percentage_diff = round((pos_diff / yesterday_closing) * 100)
# print(percentage_diff)

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 


if abs(percentage_diff) >= -5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }

    news_updates = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_updates.json()["articles"]

    first_3_articles = articles[:3]
    print(first_3_articles)
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in first_3_articles]


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in first_3_articles:
        message = client.messages.create(
            messaging_service_sid=MESSAGE_SID,
            body=article,
            to="+26878626766",
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

