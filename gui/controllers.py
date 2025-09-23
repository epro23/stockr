from gui.visuals import guiVisuals
from data.yfinance_helpers import dataOperations

def add_ticker(window, stock_history_widget, value):
    ticker = (value or "").strip().upper()
    if not (ticker and 1 <= len(ticker) <= 6):
        return

    if ticker in window.stock_tickers:
        # already exists, just show it
        show_visual_for_ticker(window, "finance_tables", ticker)
        show_visual_for_ticker(window, "line_charts", ticker)
        return
    
    window.stock_tickers.insert(0, ticker)
    stock_history_widget.combobox['values'] = window.stock_tickers

    ops = dataOperations(guiWindow=window, ticker=ticker)
    ops.fetch_stock_data()
    ops.correct_stock_data()

    ensure_visual_for_tab(window, "line_charts", ticker)
    ensure_visual_for_tab(window, "finance_tables", ticker)
    
    # Load supplementary table
    if ticker not in window.main_visuals.get("metrics_tables", {}):
        guiVisuals(window, type="metrics_table", ticker=ticker, target_frame="main_supplementary_frame")
        metrics_frame_name = f"{ticker}_metrics_frame"
        metrics_table = window.frames[metrics_frame_name]
        metrics_table.place(in_=window.frames["main_supplementary_frame"],
                            relx=0, rely=0, relwidth=1, relheight=1)
        window.current_frames["metrics_tables"] = metrics_frame_name

    # Load recommendations table
    if ticker not in window.main_visuals.get("recommendations_tables", {}):
        guiVisuals(window, type="recommendations_table", ticker=ticker, target_frame="main_recommendations_frame")
        rec_frame_name = f"{ticker}_recommendations_frame"
        recommendations_table = window.frames[rec_frame_name]
        recommendations_table.place(in_=window.frames["main_recommendations_frame"],
                                    relx=0, rely=0, relwidth=1, relheight=1)
        window.current_frames["recommendations_tables"] = rec_frame_name

    show_visual_for_ticker(window, "finance_tables", ticker)
    show_visual_for_ticker(window, "line_charts", ticker)

    # Stock history
def switch_ticker(window, value):
    ticker = (value or "").strip().upper()
    if not ticker:
        return

    # Static visuals
    switch_static_visual(window, "metrics_tables", "main_supplementary_frame", ticker)
    switch_static_visual(window, "recommendations_tables", "main_recommendations_frame", ticker)

    # Notebook visuals - line chart last to set as the default visual loaded
    ensure_visual_for_tab(window, "line_charts", ticker)
    ensure_visual_for_tab(window, "finance_tables", ticker)
    show_visual_for_ticker(window, "finance_tables", ticker)
    show_visual_for_ticker(window, "line_charts", ticker)

def switch_static_visual(window, visual_type: str, parent_name: str, ticker: str):
    new_name = window.main_visuals.get(visual_type, {}).get(ticker)
    if not new_name:
        return

    prev_name = window.current_frames.get(visual_type)
    if prev_name and prev_name != new_name:
        prev_frame = window.frames.get(prev_name)
        if prev_frame:
            prev_frame.place_forget()

    new_frame = window.frames.get(new_name)
    if new_frame:
        new_frame.place(in_=window.frames[parent_name],
                        relx=0, rely=0, relwidth=1, relheight=1)
        window.current_frames[visual_type] = new_name

    # Data display ------------------------------------------------------------------------------------------
def ensure_visual_for_tab(window, visual_type: str, ticker: str):
    ticker = (ticker or "").strip().upper()
    if not ticker:
        return None

    if ticker in window.main_visuals.get(visual_type, {}):
        return window.main_visuals[visual_type][ticker]

    # create visual
    if visual_type == "line_charts":
        guiVisuals(window, type="line_chart", ticker=ticker, target_frame="chart_tab", tab_name="chart")
    elif visual_type == "finance_tables":
        guiVisuals(window, type="finance_table", ticker=ticker, target_frame="financials_tab", tab_name="financials")
    else:
        return None

    return window.main_visuals.get(visual_type, {}).get(ticker)

def show_visual_for_ticker(window, visual_type: str, ticker: str) -> bool:
    ticker = (ticker or "").strip().upper()
    if not ticker:
        return False

    frame_name = window.main_visuals.get(visual_type, {}).get(ticker)
    if not frame_name:
        return False

    frame_obj = window.frames.get(frame_name)
    if not frame_obj:
        return False

    prev_frame_name = window.current_frames.get(visual_type)
    if prev_frame_name and prev_frame_name != frame_name:
        prev_frame = window.frames.get(prev_frame_name)
        prev_frame.place_forget()

    if visual_type == "line_charts":
        parent_tab = window.frames.get("chart_tab")
    elif visual_type == "finance_tables":
        parent_tab = window.frames.get("financials_tab")
    else:
        return False

    frame_obj.place(in_=parent_tab, relx=0, rely=0, relwidth=1, relheight=1)

    window.current_frames[visual_type] = frame_name
    window.current_main_frame_name = frame_name     
    window.current_main_key = ticker
    window.current_tab = visual_type

    stock_history_widget = window.controllers_stock_history_widget
    stock_history_widget.combobox.set(ticker)

    return True