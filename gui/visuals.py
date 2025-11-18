import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
from data.functions import adjust_large_metrics

class guiVisuals:
    def __init__(self, guiWindow, type: str, ticker: str, target_frame, tab_name=None):
        self.guiWindow = guiWindow
        self.type = type.lower()
        self.ticker = ticker

        # Parent or child frame?
        if target_frame is not None and target_frame in guiWindow.frames:
            self.target_frame = guiWindow.frames[target_frame]
        else:
            self.target_frame = guiWindow.root

        # verify
        self.tab_name = tab_name
        self.stock_data = guiWindow.stock_data.get(f"{ticker}_data", pd.DataFrame())

        # dispatch visual type
        self.dispatch_type()
    
    def dispatch_type(self):
        """
        Redirect type parameter to the appropriate visual method.
        """
        method_name = f"create_{self.type}"
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            print(f"[Warning]: Visual type '{self.type}' not yet implemented.")

    # -----------------------------
    def build_treeview(
        self,
        parent,
        df,
        style="Base.Treeview",
        row_colors=("#2b2b2b", "#252525"),
        anchor="center",
        padding=(2, 2),):
        """
        Helper to create a styled Treeview with alternating row colors.
        """
        tree = ttk.Treeview(parent, style=style, show="headings")
        tree["columns"] = list(df.columns)
        tree.tag_configure("evenrow", background=row_colors[0])
        tree.tag_configure("oddrow", background=row_colors[1])

        # Dynamic(ish) column sizing
        for col in df.columns:
            width = max(80, min(150, int(df[col].astype(str).map(len).mean() * 7)))
            tree.column(col, anchor=anchor, width=width)
            tree.heading(col, text=col)

        # alternate row colours
        for i, (_, row) in enumerate(df.iterrows()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=list(row), tags=(tag,))

        tree.pack(fill="both", expand=True, padx=padding[0], pady=padding[1])
        return tree

    # -----------------------------
    # Visual types below
    def create_finance_table(self):
        self.frame_name = f"{self.ticker}_financials_frame"
        container = tk.Frame(self.target_frame, bg="#1e1e1e")
        self.guiWindow.frames[self.frame_name] = container

        # Clean up any extra index columns
        df = self.stock_data.drop(columns=["level_0", "index"], errors="ignore")
        df["Volume"] = df["Volume"].apply(adjust_large_metrics)
        self.build_treeview(container, df, style="Base.Treeview")

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

        try:
            ticker_ref = yf.Ticker(self.ticker)
            info = ticker_ref.info
        except Exception as e:
            print(f"[Error]: Failed to fetch metrics for {self.ticker}: {e}")
            return

        metrics_list = {
            "52 Week Range": info.get("fiftyTwoWeekRange"),
            "Forward PE": info.get("forwardPE"),
            "Trailing PE": info.get("trailingPE"),
            "Profit Margins": info.get("profitMargins"),
            "Gross Profits": info.get("grossProfits"),
            "Free Cashflow": info.get("freeCashflow"),
            "Debt to Equity Ratio": info.get("debtToEquity"),
            "Beta": info.get("beta"),
        }

        for i in metrics_list.values():
            if isinstance(i, (int, float)):
                metrics_list = {k: adjust_large_metrics(v) if isinstance(v, (int, float)) else v for k, v in metrics_list.items()}

        df = pd.DataFrame(list(metrics_list.items()), columns=["Metric", "Value"])
        self.build_treeview(container, df, style="Metrics.Treeview", anchor="w", padding=(5, 5))

        self.guiWindow.main_visuals["metrics_tables"][self.ticker] = self.frame_name

    def create_recommendations_table(self):
        self.frame_name = f"{self.ticker}_recommendations_frame"
        container = tk.Frame(self.target_frame, bg="#1e1e1e")
        self.guiWindow.frames[self.frame_name] = container

        try:
            ticker_ref = yf.Ticker(self.ticker)
            recs = ticker_ref.get_recommendations_summary()
            recs_buy = recs.iloc[0]["strongBuy"] + recs.iloc[0]["buy"]
            recs_hold = recs.iloc[0]["hold"]
            recs_sell = recs.iloc[0]["sell"] + recs.iloc[0]["strongSell"]
            mean_target = ticker_ref.analyst_price_targets["mean"]
        except Exception as e:
            print(f"[Error]: Failed to fetch recommendations for {self.ticker}: {e}")
            return

        recs_list = {
            "Mean Analyst Price Target": mean_target,
            "No. Buy Recommendations": recs_buy,
            "No. Hold Recommendations": recs_hold,
            "No. Sell Recommendations": recs_sell,
        }

        df = pd.DataFrame(list(recs_list.items()), columns=["Metric", "Value"])
        self.build_treeview(container, df, style="Base.Treeview", anchor="w", padding=(2, 2))

        self.guiWindow.main_visuals["recommendations_tables"][self.ticker] = self.frame_name
