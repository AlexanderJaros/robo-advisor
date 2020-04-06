# app/robo_advisor.py

import requests
import json
import os 
from dotenv import load_dotenv
import csv

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S

load_dotenv()

#import pandas as pd
#import plotly.express as px 
##https://plot.ly/python/plot-data-from-csv/

from matplotlib import pyplot as plt
from matplotlib import style 
import numpy as np
import csv
import pandas as pd 

import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
# used https://nitratine.net/blog/post/how-to-send-an-email-with-python/

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPs - not working") 

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


def get_response(Symbol):
    while True:
        Symbol = input("Please enter stock symbol here: ")    
        if not any(s.isdigit() for s in Symbol):
            request_url_stock = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Symbol}&apikey={API_KEY}"
            response = requests.get(request_url_stock)
            parsed_response = json.loads(response.text)
            if not "Error Message" in response.text: #Thanks Professor!
                break
            else:
                print("Please ensure that the ticker is valid.")
        else:
            print("Your input should not include a number. Please enter again.")
    request_url_stock = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Symbol}&apikey={API_KEY}"
    response = requests.get(request_url_stock)
    parsed_response = json.loads(response.text)
    return parsed_response
    breakpoint()
    

#
# INFO INPUTS
#
 
Symbol = "X"
parsed_repsonse = get_response(Symbol)
#breakpoint()

#while True:
#    Symbol = input("Please enter stock symbol here: ")    
#    if not any(s.isdigit() for s in Symbol):
#        #https://stackoverflow.com/questions/39613496/is-there-a-way-i-can-prevent-users-from-entering-numbers-with-input
#        request_url_stock = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Symbol}&apikey={API_KEY}"
#        response = requests.get(request_url_stock)
#        #print(type(response))
#        #print(response.status_code)
#        #print(response.text)
#        parsed_response = json.loads(response.text)
#        if not "Error Message" in response.text: #Thanks Professor!
#            break
#        else:
#            print("Please ensure that the ticker is valid.")
#    else:
#        print("Your input should not include a number. Please enter again.")


last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]


dates = list(tsd.keys()) 

latest_day = dates[0] #"2020-02-18" 

latest_close = tsd[latest_day]["4. close"]
#breakpoint()

# get high price from each day
high_prices = []
low_prices = []


for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO INPUTS
#

#
# Recommendation 
#

valid_risk_profiles = ["High", "Low"]
risk_profile = input("Please input your risk tolerance as either High or Low: ")
if risk_profile not in valid_risk_profiles:
    print("Please enter valid risk profile.")
    risk_profile = input("Please input your risk tolerance as either High or Low: ")

Recommendation = 0
Rec_Reason = 0

if risk_profile == "High":
    if (2*recent_low) < recent_high:
        Recommendation = "BUY"
    else:
        Recommendation = "SELL"
    if Recommendation == "BUY":
        Rec_Reason = "There is high volatility in the stock."
    else:
        Rec_Reason = "There is low volatility in the stock."
else: 
    if (2*recent_low) < recent_high:
        Recommendation = "SELL"
    else:
        Recommendation = "BUY"
    if Recommendation == "SELL":
        Rec_Reason = "There is high volatility in the stock."
    else:
        Rec_Reason = "There is low volatility in the stock."

#
# Recommendation 
#

#
# CSV CREATION
#

#csv_file_path = "data/prices.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader() #uses fieldnames set above
        for date in dates:
            daily_prices= tsd[date]
            writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
            })

#
# CSV CREATION
#

#
# FINAL OUTPUTS
#

print("-------------------------")
print(f"SELECTED SYMBOL: {Symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {dt_string}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}") 
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") 
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {Recommendation}!")
print(f"RECOMMENDATION REASON: {Rec_Reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#
# FINAL OUTPUTS
#

#
# LINE PLOT OUTPUT
#

headers = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.read_csv("data\prices.csv")
print(df)

df.plot(x = "timestamp", y = "close")
plt.title(f"{Symbol}'s Recent Price Movement (Reverse Time Display)")
#plt.tight_layout()
plt._show()
#https://www.youtube.com/watch?v=MNLmQJtCCZY
#https://stackoverflow.com/questions/42350381/how-to-plot-data-from-csv-for-specific-date-and-time-using-matplotlib

#
# LINE PLOT OUTPUT
#

#
# EMAIL
#
    
valid_inputs = ["y", "n"]
user_input = input("Would the customer like to be emailed a stock update? [y/n] ")
if user_input not in valid_inputs:
    print("This input is not valid, please try again.")
    user_input = input("Would the customer like to be emailed a stock update? [y/n] ")
if user_input == "y":
     user_input2 = input("Please enter customer's email address: ")
else: 
    print("No update will be emailed.")
    quit()

load_dotenv()

email = os.getenv("email")
password = os.getenv("password")
send_to_email = user_input2
subject = "Here is your update!"
if recent_high > (recent_low*1.1):
    message = f"Thank you for using the Robo Advisor. Note that there has been recent movement of 10% or greater in share price for this stock. Also, your recommendation for {Symbol} is {Recommendation} because: {Rec_Reason}" 
else:
    message = f"Thank you for using the Robo Advisor. Note that there has not been recent movement of 10% or greater in share price for this stock. Also, your recommendation for {Symbol} is {Recommendation} because: {Rec_Reason}" 

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()

#
# EMAIL
#
