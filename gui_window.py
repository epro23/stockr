import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

class MainWindow(QMainWindow):
    """Create a class for the main window(s) of the app."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("stockr")
        self.setGeometry(100, 100, 1024, 640)
        
        # Create an instance of the Widgets class
        widgets = Widgets()
        self.setCentralWidget(widgets)

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
        return fig

class Widgets(QWidget):
    """Create a class for the widgets of the app."""
    def __init__(self):
        super().__init__()

        # Create an instance of the StockGraph class
        graph_instance = StockGraph(ticker)
        self.graph = graph_instance.fetch_and_plot()
        self.graph_widget = FigureCanvas(self.graph)
        
        # Customize graph widget
        graph_widget_layout = QVBoxLayout(self)
        graph_widget_layout.addWidget(self.graph_widget)  # Add graph to the layout
        self.setLayout(graph_widget_layout)  # Set the layout (dimensions) for widget
        self.setContentsMargins(250, 200, 5, 5)

        # Create combobox for searchable tickers
        stock_select_layout = QComboBox(self)
        stock_select_layout.addItems(tickers)


ticker = "AAPL"
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'MA']

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
