from data import *
import numpy as np
import matplotlib.pyplot as plt
global short_span, long_span, signal_span

# Function to plot data
def makePlot(data, title, xlabel, ylabel):
    plt.plot(data, label=title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    return

# Calculate EMAs
def calculate_ema(data, span):
    ema = np.zeros_like(data)
    alpha = 2 / (span + 1)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema

# Calculate MACD and Signal
# MACD = EMA(12) - EMA(26)
# Signal = EMA(9) of MACD
def calculate_macd_and_signal(data, short_span, long_span, signal_span):
    short_ema = calculate_ema(data, short_span)
    long_ema = calculate_ema(data, long_span)
    macd = short_ema - long_ema
    signal = calculate_ema(macd, signal_span)
    return macd, signal

# Identify crossover points
def identify_crossovers(macd, signal):
    buy_signals = []
    sell_signals = []
    for i in range(1, len(macd)):
        if macd[i-1] < signal[i-1] and macd[i] > signal[i]:
            buy_signals.append(i)
        elif macd[i-1] > signal[i-1] and macd[i] < signal[i]:
            sell_signals.append(i)
    return buy_signals, sell_signals

# Calculate profit or loss for each transaction
def calculate_profit_loss(asset_data, buy_signals, sell_signals):
    profit_losses = []
    for buy, sell in zip(buy_signals, sell_signals):
        buy_price = asset_data[buy]
        sell_price = asset_data[sell]
        profit_loss = sell_price - buy_price
        profit_losses.append(profit_loss)
        if buy>sell:
            print(f"Sell at {sell} (price: {sell_price}), Buy at {buy} (price: {buy_price}), Profit/Loss: {profit_loss}$ per share")
        else:
            print(f"Buy at {buy} (price: {buy_price}), Sell at {sell} (price: {sell_price}), Profit/Loss: {profit_loss}$ per share")
    return profit_losses



# Simulate trading based on MACD signals
def simulate_trading(asset_data, buy_signals, sell_signals, initial_value=1000):
    initial_portfolio = cash = initial_value*asset_data[0]
    one_buy_and_hold = initial_value*asset_data[-1]
    holdings = 0
    portfolio_value = []
    transactions = []

    for i in range(len(asset_data)):
        if i in buy_signals and cash > 0:
            holdings += cash / asset_data[i]
            cash -= holdings * asset_data[i]
            transactions.append(('Buy', i, asset_data[i],cash,holdings))
        elif i in sell_signals and holdings > 0:
            cash += holdings * asset_data[i]
            holdings = 0
            transactions.append(('Sell', i, asset_data[i],cash,holdings))
        portfolio_value.append(cash + holdings * asset_data[i])

    return cash + holdings * asset_data[-1], portfolio_value,initial_portfolio, transactions,one_buy_and_hold


# Analyze an asset
def analyze_asset(get_asset_data, code, asset_name, period):
    global short_span, long_span, signal_span

    # Get asset data
    asset_data = get_asset_data(code, asset_name, period)
    asset_data = asset_data.flatten()

    # Plot asset prices
    plt.figure(figsize=(14, 7))
    plt.title(f"{asset_name} Prices")
    makePlot(asset_data, asset_name, "Days", "Price")
    plt.legend()
    plt.show()

    # Calculate MACD for the asset
    macd, signal = calculate_macd_and_signal(asset_data, short_span, long_span, signal_span)

    # Identify crossovers
    buy_signals, sell_signals = identify_crossovers(macd, signal)

    # Plot MACD and Signal with crossovers
    plt.figure(figsize=(14, 7))
    plt.plot(macd, label=f'{asset_name} MACD')
    plt.plot(signal, label=f'{asset_name} Signal')
    plt.scatter(buy_signals, macd[buy_signals], marker='^', color='g', label='Buy Signal', zorder=5)
    plt.scatter(sell_signals, macd[sell_signals], marker='v', color='r', label='Sell Signal', zorder=5)
    plt.title(f"{asset_name} MACD and Signal")
    plt.xlabel("Days")
    plt.ylabel("Value")
    plt.legend()
    plt.show()

    print("List of all posible transactions:")
    # Calculate profit or loss for each buy/sell share
    profit_losses = calculate_profit_loss(asset_data, buy_signals, sell_signals)

    # Plot profit/loss for each buy/sell share as a scatter plot with values on top
    profit_indices = [i for i, profit_loss in enumerate(profit_losses) if profit_loss > 0] # Get indices of profitable transactions
    loss_indices = [i for i, profit_loss in enumerate(profit_losses) if profit_loss <= 0] # Get indices of loss transactions
    print(f"Number of profitable transactions: {len(profit_indices)}")
    print(f"Number of loss transactions: {len(loss_indices)}")
    plt.figure(figsize=(14, 7))
    plt.axhline(0, color='gray', linestyle='--')  # Add horizontal line at y=0
    plt.scatter(profit_indices, [profit_losses[i] for i in profit_indices], color='g', label='Profit per share in $')
    plt.scatter(loss_indices, [profit_losses[i] for i in loss_indices], color='r', label='Loss per share in $')
    for i, profit_loss in enumerate(profit_losses):
        plt.text(i, profit_loss, f'{profit_loss:.2f}', ha='center', va='bottom')
    plt.title(f"{asset_name} Profit/Loss per Transaction Share")
    plt.xlabel("Transaction Number")
    plt.ylabel("Profit/Loss in $ per Share")
    plt.legend()
    plt.show()

    # Plot pie chart of profit and loss transactions
    plt.figure(figsize=(7, 7))
    labels = ['Profitable Transactions', 'Loss Transactions']
    sizes = [len(profit_indices), len(loss_indices)]
    colors = ['g', 'r']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title(f"{asset_name} Profit vs Loss Transactions")
    plt.show()

    # Simulate trading
    final_value, portfolio_value, initial_portfolio, transactions, one_buy_and_hold = simulate_trading(asset_data, buy_signals, sell_signals)

    # Plot portfolio value over time
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_value, label='Portfolio Value in $')
    plt.title(f"{asset_name} Portfolio Value Over Time")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value in $")
    plt.legend()
    plt.show()

    # Print final portfolio value and transactions
    print("Simulated trading:")
    print(f"Initial share value: {asset_data[0]}$")
    print(f"Initial portfolio value: {initial_portfolio}$")
    print(f"Final portfolio value: {final_value}$")
    print(f"One buy and hold portfolio value: {one_buy_and_hold}$")
    for transaction in transactions:
        print(f"{transaction[0]} at day {transaction[1]} (price: {transaction[2]}$) - Cash: {transaction[3]}$, Holdings: {transaction[4]}")


short_span = 12
long_span = 26
signal_span = 9

#list of assets and ther codes:
#https://finance.yahoo.com/lookup/

# examples::
# getAnyAssetByCode('AAPL', 'apple', '4y')
# getAnyAssetByCode('BTC-USD', 'bitcoin', '4y')
# getAnyAssetByCode('ETH-USD', 'ethereum', '4y')
# getAnyAssetByCode('TSLA', 'tesla', '4y')
# getAnyAssetByCode('AMZN', 'amazon', '4y')
# getAnyAssetByCode('GOOGL', 'google', '4y')
# getAnyAssetByCode('MSFT', 'microsoft', '4y')
# getAnyAssetByCode('FB', 'facebook', '4y')
# getAnyAssetByCode('NFLX', 'netflix', '4y')
# getAnyAssetByCode('NVDA', 'nvidia', '4y')
# getAnyAssetByCode('AMD', 'amd', '4y')
# getAnyAssetByCode('INTC', 'intel', '4y')

#example of how to use the function analyze_asset
# analyze_asset(getAnyAssetByCode, code , asset_name, period)


# Analyze Etherum
analyze_asset(getAnyAssetByCode, "ETH-USD", "4y","Etherum")
