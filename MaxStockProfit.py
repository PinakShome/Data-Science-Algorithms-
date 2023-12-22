#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import warnings
import csv
warnings.filterwarnings('ignore')


# <h2> Hardcoding AAPL for DAC Algorithm work check

# In[109]:


filename = '/Users/pinakshome/Downloads/archive-5/prices-split-adjusted.csv'


def preprocess(filename):
    prices=[]
    dates1=[]
    with open(filename, 'r') as file_object:
        next(file_object)  # Skip the header line
        for line in file_object:
            elements = line.strip().split(',')
            # Extract the data from the current line
            date_str, company_symbol, open_price, close_price, low, high, volume = elements
            # If the symbol is AAPL, add the closing price and date to the lists
            if company_symbol == 'AAPL':
                prices.append(float(close_price))
                dates1.append(date_str)
    return dates1,prices

# This function will convert closing prices to daily changes
def calculate_price_changes(prices):
    changes = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        changes.append(change)
    return changes

dates1,prices=preprocess(filename)
changes=calculate_price_changes(prices)


# In[103]:


changes = [0] + changes
first_day_date = dates1[0]
dates = [first_day_date] + dates


# In[106]:


def find_max_profit(prices, dates, start, end):
    # Base case: only one day, no profit
    if end == start:
        return 0, dates[start], dates[end]

    # Divide step: find the midpoint
    mid = (start + end) // 2

    # Conquer step: recursively find max profit in left and right subarrays
    left_profit, left_start_date, left_end_date = find_max_profit(prices, dates, start, mid)
    right_profit, right_start_date, right_end_date = find_max_profit(prices, dates, mid + 1, end)

    # Combine step: find max profit crossing the midpoint
    max_left2center = 0
    sum_left2center = 0
    min_left_date = dates[mid]  # Assume the latest date at the midpoint is the starting date

    for i in range(mid, start - 1, -1):
        sum_left2center += prices[i]
        if sum_left2center > max_left2center:
            max_left2center = sum_left2center
            min_left_date = dates[i]

    max_right2center = 0
    sum_right2center = 0
    max_right_date = dates[mid + 1]  # Assume the earliest date after the midpoint is the ending date

    for i in range(mid + 1, end + 1):
        sum_right2center += prices[i]
        if sum_right2center > max_right2center:
            max_right2center = sum_right2center
            max_right_date = dates[i]

    cross_profit = max_left2center + max_right2center

    # Determine the maximum of the three profits
    max_profit, buy_date, sell_date = max(
        (left_profit, left_start_date, left_end_date),
        (right_profit, right_start_date, right_end_date),
        (cross_profit, min_left_date, max_right_date),
        key=lambda x: x[0]
    )

    return max_profit, buy_date, sell_date

max_profit, buy_date, sell_date = find_max_profit(changes, dates, 0, len(prices) - 1)
print(f"Buy on date {buy_date}, Sell on date {sell_date}, Maximum Profit: {max_profit}")


# In[107]:


df2=pd.read_csv('/Users/pinakshome/Downloads/archive-5/securities.csv')


# In[108]:


df2.head()


# <h2> Finding Max Stock Profit Across all companies

# In[112]:


def preprocess1(filename, company_symbol):
    prices = []
    dates = []
    with open(filename, 'r') as file_object:
        next(file_object)  # Skip the header line
        for line in file_object:
            elements = line.strip().split(',')
            # Extract the data from the current line
            date_str, symbol, open_price, close_price, low, high, volume = elements
            # If the symbol matches, add the closing price and date to the lists
            if symbol == company_symbol:
                prices.append(float(close_price))
                dates.append(date_str)
    return dates, prices

def calculate_price_changes1(prices):
    changes = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        changes.append(change)
    return changes

# Reading in the securities data
securities_df = pd.read_csv('/Users/pinakshome/Downloads/archive-5/securities.csv')

# This will keep track of the best profit and associated data
best_stock_info = {
    "company_name": "",
    "buy_date": "",
    "sell_date": "",
    "profit": float('-inf')
}

# Iterating over the securities DataFrame
for index, row in securities_df.iterrows():
    ticker = row['Ticker symbol']
    company_name = row['Security']

    # Using the preprocess function to get the dates and prices
    dates, prices = preprocess1('/Users/pinakshome/Downloads/archive-5/prices-split-adjusted.csv', ticker)

    if not prices:
        print(f"No price data for {ticker}. Skipping.")
        continue

    # Calculating price changes
    price_changes = calculate_price_changes1(prices)
    price_changes = [0] + price_changes

    # Ensuring we have at least two days of data to find a profit
    if len(price_changes) > 1:
        # Run your max profit algorithm
        max_profit, buy_date, sell_date = find_max_profit(price_changes, dates, 0, len(price_changes) - 1)
        
        # If the profit for this stock is better than the current best, update best_stock_info
        if max_profit > best_stock_info['profit']:
            best_stock_info.update({
                "company_name": company_name,
                "buy_date": buy_date,
                "sell_date": sell_date,
                "profit": max_profit
            })

# Print out the best stock information
if best_stock_info['profit'] != float('-inf'):
    print(f"Best stock to buy: \"{best_stock_info['company_name']}\" on {best_stock_info['buy_date']} and sell on {best_stock_info['sell_date']} with profit of {best_stock_info['profit']}")
else:
    print("No profitable stock found.")

