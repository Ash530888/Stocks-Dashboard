import pandas as pd
import yfinance as yf
from datetime import datetime

# Define the time period
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)

# Define the list of companies
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
stock_data = {}

# Download data for each company
for comp in companies:
    stock_data[comp] = yf.download(comp, start, end)
    
    # Save each DataFrame to a CSV file
    stock_data[comp].to_csv(f"{comp}_stock_data.csv")

# Optional: Display information to confirm
print(stock_data["AAPL"].describe())
print(stock_data["AAPL"].info())
print(stock_data["AAPL"].head(5))