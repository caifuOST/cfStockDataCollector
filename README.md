# cfStockDataCollector
cfStockDataCollector is the default collector for stock data into the CaifuOST grid. The cfStockDataCollector is based upon an OpenFaas function


## Request payload
The function expects a JSON formated request payload. The most basic payload will only contain the ticker symbol to indentify which stick we do require to be collected. The value of tickersymbol is not case sensitive.

```
{
	"tickersymbol": "ORCL"
}
```

A number of additional options can be provided as part of the JSON request payload. 

### Request payload - tickerPeriod
When adding tickerperiod you can control the periode (backwards from current day) which will be collected. When tickerperiod is not provided it will be defaulted to "max". Valid values are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd and max(default)
```
{
	"tickersymbol": "ORCL",
	"tickerperiod": "1d"
}
```


## Response message
