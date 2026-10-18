#REST api over the scanner: same signals as main.py, returned as json instead of printed
#run in docker, then open http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException

from data.fetch import fetch_stock_data
from core.indicators import add_indicators
from core.scanner import check_signal
from core.watchlist import WATCHLIST

app = FastAPI(
    title="financeEngine",
    description="Long-term uptrend (close above SMA200) + short-term dip (RSI14 <= 35) signals",
)


def scan(ticker: str):
    df = fetch_stock_data(ticker)
    if df.empty: #bad ticker or yahoo down, nothing to score
        return None
    return check_signal(add_indicators(df), ticker)


@app.get("/health")
def health():
    #quick check the service is up without hitting yahoo
    return {"status": "ok"}


@app.get("/signals")
def all_signals(only_signals: bool = False):
    #whole watchlist, ?only_signals=true filters down to buy signals
    results = [r for r in (scan(t) for t in WATCHLIST) if r is not None]
    if only_signals:
        results = [r for r in results if r["signal"]]
    return {"count": len(results), "results": results}


@app.get("/signals/{ticker}")
def one_signal(ticker: str):
    result = scan(ticker.upper())
    if result is None:
        raise HTTPException(status_code=404, detail=f"No data for {ticker.upper()}")
    return result