import tkinter as tk
import sys
from gui.styles import apply_theme

def on_closing(win):
    try:
        win.root.quit()
        win.root.destroy()
    except Exception:
        pass
    finally:
        sys.exit(0)

class guiWindow:
    def __init__(self):
        self.root = tk.Tk()
        # Override default theme below if desired
        apply_theme(self.root)
        # ----------------------
        self.frames={}
        self.stock_data = {}
        self.stock_tickers = []
        self.main_visuals = {"line_charts": {},
                             "finance_tables": {},
                             "metrics_tables": {},
                             "recommendations_tables": {},
                             }
        self.current_main_frame_name = None # Chart object
        self.current_main_key = None # Chart string/key
        self.current_tab = "chart"
        self.current_frames = {}

        # Additional configuration
        self.root.title("stockr")
        self.root.minsize(255,330)
        self.root.maxsize(2550,3300)
        self.root.geometry("1200x800")
