from gui.styles import apply_theme
from gui.visuals import guiVisuals
from gui.window import guiWindow
from gui.frames import guiFrames
from gui.interactables import guiInteractables
from data.yfinance_helpers import dataOperations
from gui.window import guiWindow, on_closing
from gui.controllers import (
    add_ticker,
    switch_ticker,
    switch_static_visual,
    ensure_visual_for_tab,
    show_visual_for_ticker,
)
import sys
from tkinter import ttk
# Program setup and execution ----------------------------------------------------------------------
window = guiWindow()
window.root.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

# Frame Setup
        # Parent frames -> sum = 1135 (old)
main_notebook_frame = guiFrames(window, "main_notebook_frame", width=900, height=510, 
                                use_place=True, relx=1, rely=0, anchor='ne', x=-10, y=20)
main_toggle_frame = guiFrames(window, "main_toggle_frame", width=260, height=503,
                              use_place=True, relx=0, rely=0, anchor='nw', x=20, y=20,)
main_supplementary_frame = guiFrames(window, "main_supplementary_frame", width=740, height = 240, 
                                    use_place = True, relx=0, rely=1, x=20, y=-20, anchor='sw')
main_recommendations_frame = guiFrames(window, "main_recommendations_frame", width=395, height=240,
                            use_place=True, relx=1, rely=1, x=-20, y=-20, anchor='se')
        # Nested frames
toggle_frame = guiFrames(window, "toggle_frame", width=250, height=490, 
                         parent_frame=main_toggle_frame.frame_name, use_place=True,
                        anchor='center', relx=0.5, rely=0.5)
        # Notebook creation for main_frame
notebook = ttk.Notebook(window.frames['main_notebook_frame'])
notebook.pack(fill="both", expand=True)
chart_tab = ttk.Frame(notebook)
financials_tab = ttk.Frame(notebook)
# add further tabs?
notebook.add(chart_tab, text="Chart")
notebook.add(financials_tab, text="Financials")
window.frames['main_notebook'] = notebook
window.frames['chart_tab'] = chart_tab
window.frames['financials_tab'] = financials_tab
# ----------------------------------------------------------------------------------------------------------
# Interactables setup
stock_history_widget = guiInteractables(
    window, type="combobox", target_frame=toggle_frame.frame_name, padx=10, pady=10, side="top", fill="x", 
    entry_text="Select from History", function=lambda value: switch_ticker(window, value), on_submit=None)

stock_selection_widget = guiInteractables(
    window, type="entry", target_frame=toggle_frame.frame_name, padx=10, pady=10, side="top", fill="x", 
    entry_text="Input (e.g. AAPL)", function=lambda value: add_ticker(window, stock_history_widget, value), on_submit=None)

window.controllers_stock_history_widget = stock_history_widget
# ----------------------------------------------------------------------------------------------------------
# Go!
try:
    window.root.mainloop()
finally:
    try:
        window.root.destroy()
    except Exception:
        pass
    sys.exit(0)
