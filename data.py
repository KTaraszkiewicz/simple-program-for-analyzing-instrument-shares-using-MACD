import yfinance as yf
import pandas as pd

# Function to get any asset
def getAnyAssetByCode(code, name, period):
    asset = yf.Ticker(code)
    data = asset.history(period=period)  # Period to get data
    # Save the data to a CSV file using pandas
    data.to_csv(f'{name}.csv', index=True)  # Saving with index (date)
    print(f"{name} data has been saved to '{name}.csv'")
    data = pd.read_csv(f'{name}.csv', usecols=['Close'])
    return data.to_numpy()

