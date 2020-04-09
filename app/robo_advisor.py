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


def get_response(symbol):
    request_url_stock = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url_stock)
    parsed_response = json.loads(response.text)
    if "Error Message" in response.text:
        return "Invalid input"
    return parsed_response

def transform_response(parsed_response):
    # parsed_response should be a dictionary representing the original JSON response
    # it should have keys: "Meta Data" and "Time Series Daily"
    tsd = parsed_response["Time Series (Daily)"]

    rows = []
    for date, daily_prices in tsd.items(): # see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        rows.append(row)

    return rows

def write_to_csv(rows, csv_filepath):
    # rows should be a list of dictionaries
    # csv_filepath should be a string filepath pointing to where the data should be written

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)

    return True

#
# INFO INPUTS
# 

if __name__ == "__main__":

    time_now = datetime.now() #> datetime.datetime(2019, 3, 3, 14, 44, 57, 139564)
 
    while True:
        symbol = input("Please enter stock symbol here: ")    
        if not any(s.isdigit() for s in symbol):
            get_response(symbol)
            if get_response(symbol) == "Invalid input":
                print("Please ensure that the ticker is valid.")
            else:
                break
        else:
            print("Your input should not include a number. Please enter again.")
    
    parsed_response = get_response(symbol)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    rows = transform_response(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes!
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes!
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

    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    write_to_csv(rows, csv_filepath)

    #
    # CSV CREATION
    #

    #
    # FINAL OUTPUTS
    #


    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
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
    print(f"WRITING DATA TO CSV: {csv_filepath}...")
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
    plt.title(f"{symbol}'s Recent Price Movement (Reverse Time Display)")
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
