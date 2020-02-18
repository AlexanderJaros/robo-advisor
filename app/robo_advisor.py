# app/robo_advisor.py

import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", defaults="OOPS")

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# INFO INPUTS
#

Symbol = "TSLA" #TODO: ask for user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Symbol}&apikey={API_KEY}"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #TODO: sort to ensure latest day is first
#assumes first day is on top, but consider sorting

latest_day = dates[0] #"2020-02-18" 

latest_close = tsd[latest_day]["4. close"]
#breakpoint()

# get high price from each day
high_prices = []


for date in dates:
    print(date)


# maximum of all high prices
recent_high = max(high_prices)

#
# INFO INPUTS
#

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}") #maybe include time as well, 24m into vid, use of datetime module 25m in
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") #format to usd
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")