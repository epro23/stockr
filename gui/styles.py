# gui/styles.py
import sv_ttk
from tkinter import ttk

def apply_theme(root):
    """Apply the global Sun Valley dark theme and shared ttk styles."""
    sv_ttk.set_theme("dark")

    style = ttk.Style()
    # Example: dark Treeview defaults
    style.configure("Custom.Treeview",
                    background="#2b2b2b",
                    fieldbackground="#2b2b2b",
                    foreground="white",
                    rowheight=24,
                    font=("Helvetica", 10))
    style.configure("Custom.Treeview.Heading",
                    background="#3c3f41",
                    foreground="white",
                    font=("Helvetica", 10, "bold"))
    style.map("Custom.Treeview",
              background=[("selected", "#505050")])
