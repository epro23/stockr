import tkinter as tk
from tkinter import ttk
class guiInteractables:
    def __init__(self, guiWindow, type, target_frame, padx=None, pady=None, side=None, 
                 fill=None, entry_text=None, on_submit=None,function=None):
        self.guiWindow = guiWindow
        self.type = type.lower()
        if target_frame is not None and target_frame in guiWindow.frames:
            self.target_frame = guiWindow.frames[target_frame]
        else:
            self.target_frame = guiWindow.root
        self.padx = padx
        self.pady = pady
        self.side = side
        self.fill = fill
        self.entry_text = entry_text if entry_text else "You forgot input text!"

        self.on_submit = on_submit
        self.function = function    # per widget
        
        self.dispatch_type()

    def dispatch_type(self):
        method_name = f"create_{self.type}"
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            print(f"[Warning]: Interactable visual type '{self.type}' not yet implemented.")
    
    def handle_submit(self, event=None):
        value = self.entry.get()
        if callable(self.function):
            self.function(value)
        if callable(self.on_submit):
            self.on_submit(value)
        self.entry.delete(0, tk.END)
    
    def handle_combobox_submit(self, event=None):
        value = self.combobox.get()
        if callable(self.function):
            self.function(value)
        if callable(self.on_submit):
            self.on_submit(value)
# ----------------------------------------------------------------------------------------------------------
    def create_entry(self):
        self.entry = tk.Entry(self.target_frame, width=30)
        self.entry.insert(0, string=self.entry_text)
        self.entry.bind("<Return>", self.handle_submit)
        self.entry.pack(padx=self.padx, pady=self.pady, side=self.side, fill=self.fill)
        return self.entry
# ----------------------------------------------------------------------------------------------------------
    def create_combobox(self):
        self.combo_var = tk.StringVar()
        self.combobox = ttk.Combobox(self.target_frame, textvariable=self.combo_var, state="readonly", width=30)
        self.combobox['values'] = self.guiWindow.stock_tickers
        self.combobox.bind("<<ComboboxSelected>>", self.handle_combobox_submit)
        self.combobox.set(self.entry_text)
        self.combobox.pack(padx=self.padx, pady=self.pady, side=self.side, fill=self.fill)
        return self.combobox
