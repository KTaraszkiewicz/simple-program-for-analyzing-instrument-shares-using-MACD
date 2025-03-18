# simple-program-for-analyzing-instrument-shares-using-MACD
## university project - its utility is low but project is made for educational purposes.

# How to use:
list of assets and ther codes:
```
https://finance.yahoo.com/lookup/
```
## examples:
getAnyAssetByCode('AAPL', 'apple', '4y')  
getAnyAssetByCode('BTC-USD', 'bitcoin', '4y')  
getAnyAssetByCode('ETH-USD', 'ethereum', '4y')  
getAnyAssetByCode('TSLA', 'tesla', '4y')  
getAnyAssetByCode('AMZN', 'amazon', '4y')  
getAnyAssetByCode('GOOGL', 'google', '4y')  
getAnyAssetByCode('MSFT', 'microsoft', '4y')  
getAnyAssetByCode('FB', 'facebook', '4y')  
getAnyAssetByCode('NFLX', 'netflix', '4y')  
getAnyAssetByCode('NVDA', 'nvidia', '4y')  
getAnyAssetByCode('AMD', 'amd', '4y')  
getAnyAssetByCode('INTC', 'intel', '4y')  

## example of how to use the function analyze_asset
analyze_asset(getAnyAssetByCode, code , asset_name, period)

## Example of use for Apple in period of 4years:
```
analyze_asset(getAnyAssetByCode, 'AAPL', 'apple', '4y')
```
