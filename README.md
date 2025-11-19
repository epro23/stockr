# stockr
-----------------------------------------------------------------------------------------------------------------
### Overview
A new GUI application building upon older methodology, acting as a resource to collect and visualize accessible stock data information to beginner or curious investors.

`stockr` scrapes historical stock data, once per user input, via a yfinance API call. The data is stored in the session to generate a series of tables and figures via custom `pandas`, `Matplotlib`, and `tkinter` API calls which are subsequently displayed on the tkinter GUI interface.

`stockr` provides a simple GUI front-end that fetches historical stock data (via `yfinance`), processes it with `pandas`, and visualizes it with `matplotlib` (and optional seaborn). The application was built as a lightweight, distributable desktop tool so non-technical users can explore stock price history and basic technical indicators.

![alt text](https://github.com/epro23/stockr/blob/main/images/chart_screen.png "Chart Tab")

### Accessing stockr
The easiest way to access stockr (without me paying for a developer license!) is by cloning the repo and establishing a virtual environment.

In your working folder:
```
git clone https://github.com/epro23/stockr
cd stockr
```

(Recommended) Use a virtual environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Then, running main.py inside the venv should launch the GUI application.

![alt text](https://github.com/epro23/stockr/blob/main/images/launch_screen.png "Launch Screen")

### Project Status
Functional prototype displayed here. A path forward is clear with future updates to come, prioritizing customizing date and graph interactivity via more GUI interactables in the toggle frame.

If you'd like to contribute, contact me on GitHub!


