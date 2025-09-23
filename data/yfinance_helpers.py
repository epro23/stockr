import yfinance as yf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
# import guiWindow how???
from gui.window import guiWindow
class dataOperations:
    def __init__(self, guiWindow, ticker=None, start_date=None, end_date=None, interval="1d"):
        self.ticker = ticker
        today = date.today()
        self.start_date = start_date if start_date is not None else today - relativedelta(months=6)
        self.end_date = end_date if end_date is not None else today
        self.end_date = today
        self.interval = interval if interval is not None else "60m"
        self.stock_data = guiWindow.stock_data

    def fetch_stock_data(self):
        """
        Note: plucked from old project, modified as needed.
        """
        data = yf.download(
            self.ticker, start=self.start_date, end=self.end_date, interval=self.interval, rounding=True)
        # storing financials 
        self.stock_data[f"{self.ticker}_data"] = data
        # running list of tickers found in stock_data["tickers"]
        if "tickers" not in self.stock_data:
            self.stock_data["tickers"] = []
        if self.ticker not in self.stock_data["tickers"]:
            self.stock_data["tickers"].append(self.ticker)

        guiWindow.stock_data = self.stock_data  # Update the stock_data in guiWindow
        return self.stock_data
    
    def correct_stock_data(self):
        """
        Clean and standardize stock data:
        - Flattens multi-index if needed
        - Renames the index column to 'Date'
        - Formats date to exclude seconds
        - Drops time entirely if it's midnight (daily interval)
        """
        ticker_key = f"{self.ticker}_data"
        df = self.stock_data[ticker_key]

        if isinstance(df.columns, pd.MultiIndex):
            df = df.droplevel("Ticker", axis=1)

        df = df.reset_index()
        df.rename(columns={df.columns[0]: "Date"}, inplace=True)

        # Format 'Date' column depending on time presence
        if pd.api.types.is_datetime64_any_dtype(df["Date"]):
            if (df["Date"].dt.time == pd.Timestamp("00:00").time()).all():
                df["Date"] = df["Date"].dt.strftime('%Y-%m-%d')  # Drop time if it's all midnight (daily/monthly data)
            else:
                df["Date"] = df["Date"].dt.strftime('%Y-%m-%d %H:%M')  # Keep hours + minutes

        df.columns.name = "Data Index"
        self.stock_data[ticker_key] = df

        return self.stock_data
