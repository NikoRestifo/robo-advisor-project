# this is the "app/robo_advisor.py" file

import csv
import json
from dotenv import load_dotenv
import os
import datetime
import seaborn as sns
from pandas import read_csv
import matplotlib.pyplot as plt
import requests

load_dotenv()

#convert numberical values to dollars

def to_usd(my_price):
   return "${0:,.2f}".format(my_price)


#create human friendly timestamp for output

def make_timestamp():
   date = datetime.date.today()
   time = datetime.datetime.now()
   print("REQUEST AT:", date, time.strftime("%I:%M:%S %p"))

#
#INFO INPUTS
#

symbols = []

more_stocks = True
while more_stocks == True:
   symbol = input("Please enter a stock or cryptocurrency symbol, or type 'DONE' if there are more no stocks to enter: ") 
   if symbol.lower() == 'done':
       more_stocks = False
   else:
       symbols.append(symbol)        

for symbol in symbols:
    numeric_symbol = False
    for i in range(len(symbol)):
        if symbol[i].isnumeric():
            print(f"'{symbol.upper()}' is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
            numeric_symbol = True
            break
    if numeric_symbol == True:
        continue
    if len(symbol) > 5:
        print(f"'{symbol.upper()}' is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
        continue
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    if "Error Message" in response.text:
        print(f"Could not find any trading data for '{symbol.upper()}'. Please try again")
        continue
    if "higher API call frequency" in response.text:
        print("You entered too many stocks. Please try again")
        quit()
    parsed_response = json.loads(response.text)
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    latest_day = dates[0]
    latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

# maximum of all high prices

    high_prices = []
    low_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        low_price = tsd[date]["3. low"]        
        high_prices.append(float(high_price))
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

    # buy or sell
    if float(latest_close) <= float(recent_low) * 1.2:
        recommendation = "RECOMMENDATION: BUY"
        recommendation_reason = "The stock's latest closing price is less than 20% above its recent low"
    else:
        recommendation = "RECOMMENDATON: SELL"
        recommendation_reason = "The stock's latest closing price is greater than 20% above its recent low"

#
# INFO OUTPUTS
#

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")

    csv_headers =  ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for date in dates:
            daily_prices = tsd[date]
            writer.writerow({
                "timestamp": date,
                "open": daily_prices["1. open"],
                "high": daily_prices["2. high"],
                "low": daily_prices["3. low"],
                "close": daily_prices["4. close"],
                "volume": daily_prices["5. volume"],
            })
       
    print("-------------------------")
    print("SELECTED SYMBOL:", symbol.upper())
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    make_timestamp()
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {recommendation}")
    print(f"RECOMMENDATION REASON: {recommendation_reason}")
    print("-------------------------")
    print("WRITING DATA TO CSV...")
    print("-------------------------")
    print("PLEASE EXIT THE GRAPH TO PROCEED")

#
# Line graph of csv data (Closing price for past 100 days)
#

    csv_filename = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")
    stocks_df = read_csv(csv_filename)
    plt.figure(num=1, figsize=(10,5))
    sns.lineplot(data= stocks_df, x="timestamp", y= "close").invert_xaxis()
    plt.title(f"Price of {symbol.upper()} stock over past 100 days")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.xticks(rotation=90, fontsize=4)
    plt.show()

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
quit()
