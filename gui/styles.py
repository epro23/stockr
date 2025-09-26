# gui/styles.py
import sv_ttk
from tkinter import ttk

def apply_theme(root,
                *,
                theme: str = "dark",
                font_family: str = "Helvetica",
                font_size: int = 10,
                heading_font_size: int = 10,
                row_height: int = 22,
                line_spacing: int = 2,
                bg_main: str = "#2b2b2b",
                bg_alt: str = "#252525",
                bg_heading: str = "#3c3f41",
                fg_text: str = "white",
                fg_heading: str = "white",
                bg_selected: str = "#505050"
                ):
    """
    Apply the sv_ttk theme with customizable Treeview/visual styling.

    Parameters
    ----------
    root : Tk
        The root Tk window.
    theme : {"dark","light"}
        Base sv_ttk theme.
    font_family : str
        Table font family.
    font_size : int
        Base font size for table cells.
    heading_font_size : int
        Font size for column headings.
    row_height : int
        Height of each Treeview row.
    line_spacing : int
        Additional spacing between rows (padding).
    bg_main, bg_alt : str
        Alternating row background colors.
    bg_heading : str
        Header background color.
    fg_text, fg_heading : str
        Foreground colors.
    bg_selected : str
        Selected row highlight color.
    """
    # ---------------------
    # Base Theme
    # ---------------------
    sv_ttk.set_theme(theme)

    style = ttk.Style()

    # Core Treeview styling
    base_font = (font_family, font_size)
    heading_font = (font_family, heading_font_size, "bold")

    # Base tables (used for most visuals)
    style.configure(
        "Base.Treeview",
        background=bg_main,
        fieldbackground=bg_main,
        foreground=fg_text,
        rowheight=row_height + line_spacing,
        font=base_font
    )
    style.configure(
        "Base.Treeview.Heading",
        background=bg_heading,
        foreground=fg_heading,
        font=heading_font
    )
    style.map(
        "Base.Treeview",
        background=[("selected", bg_selected)],
        foreground=[("selected", fg_text)]
    )

    # Metrics table – slight variation if desired
    style.configure(
        "Metrics.Treeview",
        background=bg_alt,
        fieldbackground=bg_alt,
        foreground=fg_text,
        rowheight=row_height + line_spacing,
        font=base_font
    )
    style.configure(
        "Metrics.Treeview.Heading",
        background=bg_heading,
        foreground=fg_heading,
        font=heading_font
    )
    style.map(
        "Metrics.Treeview",
        background=[("selected", bg_selected)],
        foreground=[("selected", fg_text)]
    )

    # Optional: adjust other widgets (buttons, labels, etc.) here if needed

