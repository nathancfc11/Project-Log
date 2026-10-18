import pandas as pd


def to_number(value):
    #json cant hold NaN (e.g. sma200 for a stock with <200 days of data), so send None instead
    return None if pd.isna(value) else round(float(value), 2)


def check_signal(df, ticker):

    if df.empty: #error handling
        print(f"No data for {ticker}, skipping signal check.")
        return None

    latest = df.iloc[-1] #grab last row of df, today's most recent close

    close = latest["Close"]
    sma200 = latest["SMA200"]
    rsi14 = latest["RSI14"]

    above_sma = close > sma200 #boolean 4 todays price over 200 day sma (average)
    oversold = rsi14 <= 35 #is rsi beaten down enuf
    signal = bool(above_sma and oversold) #plain python bool so it can go into json

    print(f"{'BUY SIGNAL' if signal else 'NO SIGNAL'}: {ticker}")
    print(f"price: $ {close:.2f}")
    print(f"SMA200: $ {sma200:.2f}")
    print(f"RSI14: {rsi14:.2f}")

    #same result as a dict, so main.py can print it and api.py can send it as json
    return {
        "ticker": ticker,
        "date": str(latest.name.date()),
        "close": to_number(close),
        "sma200": to_number(sma200),
        "rsi14": to_number(rsi14),
        "signal": signal,
    }