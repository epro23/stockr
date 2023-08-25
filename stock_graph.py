import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

class StockGraph:
    def __init__(self, ticker, start_date="1900-01-01", end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = None  # Initialize price_data attribute

    def stock_prices(self):
        if self.end_date is None:
            self.end_date = datetime.now()
        self.price_data = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval="1d")
        
    def plot_data(self, ax):
        ax.plot(self.price_data['Close'], label=f'{self.ticker} Close Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title(f'{self.ticker} Stock Price Over Time')
        ax.legend()
        ax.grid(True)
        
    def fetch_and_plot(self):
        self.stock_prices()
        fig, ax = plt.subplots(figsize=(10, 6))
        self.plot_data(ax)
        plt.show()

# Usage
ticker = "AAPL"
generate_stock_data = StockGraph(ticker)
generate_stock_data.fetch_and_plot()

