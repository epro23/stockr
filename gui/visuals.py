import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf

class guiVisuals:
    def __init__(self, guiWindow, type:str, ticker:str, target_frame, tab_name=None):
        self.guiWindow = guiWindow
        self.type = type.lower()
        self.ticker = ticker
        if target_frame is not None and target_frame in guiWindow.frames:
            self.target_frame = guiWindow.frames[target_frame]
        else:
            self.target_frame = guiWindow.root
        self.tab_name = tab_name
        self.stock_data = guiWindow.stock_data[f"{ticker}_data"]
        # self.stock_data.reset_index(inplace=True)
        self.dispatch_type()
    
    def dispatch_type(self):
        # Redirect type parameter to visual call
        method_name = f"create_{self.type}"
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            print(f"[Warning]: Visuals visual type '{self.type}' not yet implemented.")

    def create_finance_table(self):
        self.frame_name = f"{self.ticker}_financials_frame"
        container = tk.Frame(self.target_frame, bg="#1e1e1e")
        self.guiWindow.frames[self.frame_name] = container

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background="#2b2b2b",
                        foreground="#ffffff",
                        fieldbackground="#2b2b2b",
                        font=("Helvetica", 10),
                        rowheight=24)
        style.configure("Dark.Treeview.Heading",
                        background="#333333",
                        foreground="#ffffff",
                        font=("Helvetica", 10, "bold"))
        style.map("Dark.Treeview",
                background=[("selected", "#444444")])

        self.stock_data = self.stock_data.drop(columns=["level_0", "index"], errors="ignore")

        tree = ttk.Treeview(container, style="Dark.Treeview")
        tree["columns"] = list(self.stock_data.columns)
        tree["show"] = "headings"

        tree.tag_configure("evenrow", background="#2b2b2b")
        tree.tag_configure("oddrow", background="#252525")

        for col in self.stock_data.columns:
            width = max(80, min(150, int(self.stock_data[col].astype(str).map(len).mean() * 7)))
            tree.column(col, anchor="center", width=width)
            tree.heading(col, text=col)

        for i, (_, row) in enumerate(self.stock_data.iterrows()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=list(row), tags=(tag,))

        tree.pack(fill="both", expand=True, padx=2, pady=2)

        self.guiWindow.main_visuals["finance_tables"][self.ticker] = self.frame_name

    def create_line_chart(self):
        self.frame_name = f"{self.ticker}_line_chart_frame"
        container = tk.Frame(self.target_frame)
        self.guiWindow.frames[self.frame_name] = container

        df = self.stock_data.copy()
        df["Average Price"] = (df["High"] + df["Low"]) / 2

        with plt.style.context("dark_background"):
            fig, ax = plt.subplots(figsize=(8, 4))

            deep_gray = "#1e1e1e"   
            fig.patch.set_facecolor(deep_gray)   
            ax.set_facecolor(deep_gray)          

            ax.plot(
                df["Date"],
                df["Average Price"],
                label="Average Price",
                color="deepskyblue",
                linewidth=1.5,
                marker="o" if len(df) <= 62 else None,
            )

            ax.set_ylabel("Average Price (USD)", color="white")
            ax.tick_params(axis="both", labelsize=8, colors="white")
            ax.spines["bottom"].set_color("white")
            ax.spines["left"].set_color("white")
            ax.grid(True, color="#444", linestyle="--", linewidth=0.5)

            fig.tight_layout(pad=1.0)     
            fig.subplots_adjust(top=0.95, bottom=0.15, left=0.10, right=0.98)

            fig.autofmt_xdate(rotation=30)
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))
            ax.yaxis.set_major_locator(plt.MaxNLocator(8))

            canvas = FigureCanvasTkAgg(fig, master=container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        self.guiWindow.main_visuals["line_charts"][self.ticker] = self.frame_name


    def create_metrics_table(self):
        self.frame_name = f"{self.ticker}_metrics_frame"
        container = tk.Frame(self.target_frame, bg="#1e1e1e")
        self.guiWindow.frames[self.frame_name] = container

        ticker_ref = yf.Ticker(self.ticker)
        metrics_list = {
            "52 Week Range": ticker_ref.info.get("fiftyTwoWeekRange"),
            "Forward PE": ticker_ref.info.get("forwardPE"),
            "Trailing PE": ticker_ref.info.get("trailingPE"),
            "Profit Margins": ticker_ref.info.get("profitMargins"),
            "Gross Profits": ticker_ref.info.get("grossProfits"),
            "Free Cashflow": ticker_ref.info.get("freeCashflow"),
            "Debt to Equity": ticker_ref.info.get("debtToEquity"),
            "Beta": ticker_ref.info.get("beta"),
        }

        df = pd.DataFrame(list(metrics_list.items()), columns=["Metric", "Value"])

        style = ttk.Style()
        style.configure(
            "Metrics.Treeview",
            background="#1e1e1e",    
            fieldbackground="#1e1e1e",
            foreground="white",   
            rowheight=24,
            borderwidth=0,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Metrics.Treeview.Heading",
            background="#2b2b2b", 
            foreground="white",
            relief="flat",
            font=("Segoe UI", 12, "bold")
        )
        style.map(
            "Metrics.Treeview",
            background=[("selected", "#3a6ea5")],
            foreground=[("selected", "white")]
        )

        tree = ttk.Treeview(container, style="Metrics.Treeview", show="headings")
        tree["columns"] = list(df.columns)

        tree.tag_configure("evenrow", background="#252525")
        tree.tag_configure("oddrow", background="#1e1e1e")

        for col in df.columns:
            width = max(120, int(df[col].astype(str).map(len).mean() * 9))
            tree.column(col, anchor="w", width=width)
            tree.heading(col, text=col)

        for i, (_, row) in enumerate(df.iterrows()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=list(row), tags=(tag,))

        tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.guiWindow.main_visuals["metrics_tables"][self.ticker] = self.frame_name

    def create_recommendations_table(self):
        self.frame_name = f"{self.ticker}_recommendations_frame"
        container = tk.Frame(self.target_frame, bg="#1e1e1e")
        self.guiWindow.frames[self.frame_name] = container

        ticker_ref = yf.Ticker(self.ticker)
        recs = ticker_ref.get_recommendations_summary()
        recs_buy = recs.iloc[0]["strongBuy"] + recs.iloc[0]["buy"]
        recs_hold = recs.iloc[0]["hold"]
        recs_sell = recs.iloc[0]["sell"] + recs.iloc[0]["strongSell"]
        recs_list = {
            "Mean Analyst Price Target": ticker_ref.analyst_price_targets["mean"],
            "No. Buy Recommendations": recs_buy,
            "No. Hold Recommendations": recs_hold,
            "No. Sell Recommendations": recs_sell
        }

        df = pd.DataFrame(list(recs_list.items()), columns=["Metric", "Value"])

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background="#2b2b2b",
                        foreground="#ffffff",
                        fieldbackground="#2b2b2b",
                        font=("Helvetica", 11),
                        rowheight=24)
        style.configure("Dark.Treeview.Heading",
                        background="#333333",
                        foreground="#ffffff",
                        font=("Helvetica", 12, "bold"))
        style.map("Dark.Treeview",
                background=[("selected", "#444444")])

        tree = ttk.Treeview(container, style="Dark.Treeview")
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        tree.tag_configure("evenrow", background="#2b2b2b")
        tree.tag_configure("oddrow", background="#252525")

        for col in df.columns:
            width = max(120, int(df[col].astype(str).map(len).mean() * 10))
            tree.column(col, anchor="w", width=width)
            tree.heading(col, text=col)

        for i, (_, row) in enumerate(df.iterrows()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=list(row), tags=(tag,))

        tree.pack(fill="both", expand=True, padx=2, pady=2)

        self.guiWindow.main_visuals["recommendations_tables"][self.ticker] = self.frame_name