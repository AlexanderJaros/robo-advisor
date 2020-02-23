## Welcome to Alex's Python Robo-Advisor

Below you will find all setup and installation requirements.

## Setup

First, make sure to clone this repository to your own Github desktop. Once done, create a virtual enviroment with following code in the command line:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file from within the repository: 

```sh
pip install -r requirements.txt
```

## How this application works

This robo advisor, when run with the command:

```sh
python app/robo_advisor.py
```

will prompt the user to enter a valid stock ticker and their risk tolerance, which can be either "High" or "Low". 

An output of recent trading information will be generated, along with a "BUY" or "SELL" recommendation and its reasoning. Volatility is calculated simply, by viewing the relationship between the stock's recent high and recent low. If the recent low multiplied by 2 is lower than the recent high, the stock is judged to have high volatility. 

A recent days line plot of closing prices is as well displayed, along with the option of having a stock update with certain information sent to the client. 

This email is sent via a gmail account made for a past grocery receipt project. This can be updated to a new email by setting the .env file variables "email" and "password" to those of the desired new email address. Do ensure that other apps have been allowed access via Google's settings. 

In a similar vein, this app gets its data from  AlphaVantage API and uses a private user API Key, stored in the .env file, for authentication. Please secure your own API Key from the provider website and store it as a variable in the app .env file you create. 

https://www.alphavantage.co/

And, of course, remember to create .gitignore files to hide your .env! 
