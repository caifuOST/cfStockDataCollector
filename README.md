# cfStockDataCollector
cfStockDataCollector is the default collector for stock data into the CaifuOST grid. The cfStockDataCollector is based upon an OpenFaas function


## request payload
The function expects a JSON formated request payload. 

```
{
	"tickersymbol": "ORCL"
}
```
