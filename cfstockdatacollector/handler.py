import yfinance as yf
import json
#import socket


# TODO these are some debugging lines that can be used when developing. If moving to a stable version we can remove this
#req = '{"tickersymbol": "oRcL"}'
#req = '{"tickersymbol": "oRcL", "tickerperiod" : "1m"}'
#req = '{"tickersymbol": "oRcL", "tickerperiod" : "1d", "tickerinterval" : "15m"}'


def errorResponse(errorMessage):
    '''
    Standard response message for an error to ensure that all the error messages are returned to the calling application
    in a generic manner. This will ensure all the calling applications can handle an error return message also in a
    unified and standard manner.

    :param errorMessage:
    :return: errorResponse
    '''
    errorResponse = {
                     "status": "error",
                     "status_message": errorMessage,
	                 "response": "none"
                     }
    return errorResponse


def handle(req):
    '''
    the way OpenFaas will call the function and provides the request payload is always calling the "handle" function. In
    this implementation we do some basic checking in "handle" to make sure we have a JSON based request payload and we
    will return an error response message in a JSON format when the provided input from the calling application is not
    a valid JSON request payload. In case where we have a proper formatted JSON request payload we will provide this to
    the logicMainHandler and leave all other actions to the logicMainHandler (including the generation of any other
    potential errorResponse return payloads.
    :param req:
    :return:
    '''

    try:
        json.loads(req)
        print(socket.gethostname())

      #  responseMessage = '{
      #      "status": "error",
      #      "status_message": errorMessage,
      #      "response": (logicMainHandler(req))
      #  }'

        return logicMainHandler(req)
        #return responseMessage



    except ValueError as err:
        return(errorResponse(format(err)))
    except:
        return (errorResponse("Unexpected error"))


def logicMainHandler(req):
    '''

    :param req:
    :return: res
    '''

    # Parse the req payload into a JSON format
    req = json.loads(req)

    # Extract the values needed from the req payload JSON
    try:
        # try to extract the ticker symbol. We do need a ticker symbol, in case it is not provided we will gently fail.
        try:
            tickerSymbol = req["tickersymbol"]
        except:
            return (errorResponse("unable to find valid tickersymbol key value pair in request JSON in logicModule"))

        # Try to extract the period, if no period is provided we will set this to the value "max" and we will not fail.
        # Valid periods are 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. If an invalid value is provided we will default to
        # max.
        try:
            tickerPeriod = req["tickerperiod"]
            validtickerPeriods = ['1d' , '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
            if tickerPeriod not in validtickerPeriods:
                tickerPeriod = "max"
        except:
            tickerPeriod = "max"

        # Try to extract the interval for reporting. fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo. (optional, default is '1d')
        try:
            tickerInterval = req["tickerinterval"]
            validTickerInterval = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
            if tickerInterval not in validTickerInterval:
                tickerInterval = "1d"
        except:
            tickerInterval = "1d"

        # we have to take a provision for cases where tickerPeriod = 1d and tickerInterval = 1d. In those cases we have
        # to change the tickerInterval to 1m to prevent a "DataFrame index must be unique for orient='index" error from
        # being raised.
        try:
            if tickerPeriod == "1d" and tickerInterval == "1d":
                tickerInterval = "1m"
        except:
            return (errorResponse("unexpected issue related to combination of tickerperiod and tickerinterval "))

    except:
        return (errorResponse("unexpected error while parsing request JSON in logicModule"))

    # call the logic and return the outcome.
    return stockDataGrabber(tickerSymbol, tickerPeriod, tickerInterval)


def stockDataGrabber(tickerSymbol, tickerPeriod, tickerInterval):
    tickerSymbol = (tickerSymbol).upper()
    ticker = yf.Ticker(tickerSymbol)
    tickerData = ticker.history(period=tickerPeriod, interval=tickerInterval)
    tickerData['ticker'] = tickerSymbol

    tickerData = tickerData.to_json(orient='index')

    return tickerData
