#!/usr/bin/env python
# coding: utf-8

# In[4]:


import csv

def fetch_and_transform_data(file_path):
    portfolio_options = []
    with open(file_path, 'r') as data_file:
        data_reader = csv.DictReader(data_file)
        next(data_reader)  # Bypassing the first row with USA data
        for record in data_reader:
            area_name = record['RegionName']
            investment_cost = int(record['2020-01'])
            profit_estimate = int(record['2020-01']) - int(record['2019-01'])
            portfolio_options.append((area_name, investment_cost // 1000, profit_estimate))  # Adjusting cost to 'thousands'
    return portfolio_options

def find_optimal_portfolio(data_path, total_funds, scaling_factor):
    portfolio_items = fetch_and_transform_data(data_path)
    adjusted_budget = total_funds // scaling_factor  # Adjusting funds to 'thousands'
    profit_matrix = [[0] * (adjusted_budget + 1) for _ in range(len(portfolio_items) + 1)]

    for item_index in range(1, len(portfolio_items) + 1):
        area, investment, profit = portfolio_items[item_index - 1]
        for budget_point in range(1, adjusted_budget + 1):
            if investment <= budget_point:
                profit_matrix[item_index][budget_point] = max(profit_matrix[item_index - 1][budget_point], 
                                                              profit_matrix[item_index - 1][budget_point - investment] + profit)
            else:
                profit_matrix[item_index][budget_point] = profit_matrix[item_index - 1][budget_point]

    # Tracing back to deduce the chosen investments
    optimal_choices = []
    remaining_funds = adjusted_budget
    for index in range(len(portfolio_items), 0, -1):
        if profit_matrix[index][remaining_funds] != profit_matrix[index - 1][remaining_funds]:
            area_name = portfolio_items[index - 1][0]
            optimal_choices.append(area_name)
            remaining_funds -= portfolio_items[index - 1][1]

    highest_profit = profit_matrix[len(portfolio_items)][adjusted_budget]
    return highest_profit, optimal_choices[::-1]

# Executing the main function
data_file_path = "/Users/pinakshome/Downloads/Metro.csv"
investment_budget = 1000000
scale_value = 1000

peak_profit, best_investments = find_optimal_portfolio(data_file_path, investment_budget, scale_value)
print("Peak ROI:", peak_profit)
print("Optimum Investment Areas:", best_investments)

