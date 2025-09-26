from tkinter import ttk
class guiFrames:
    def __init__(self, guiWindow, frame_name, bg=None, width=800, height=600,
                 parent_frame=None, use_place=False,
                 relx=None, rely=None, anchor=None, x=None, y=None,
                 padx=None, pady=None, side=None, fill=None):
        self.guiWindow = guiWindow
        self.frame_name = frame_name
        self.width = width
        self.height = height
        self.parent_frame = parent_frame
        self.use_place = use_place
        self.bg = bg or "grey20" 
        self.placement = dict(relx=relx, rely=rely, anchor=anchor, x=x, y=y,
                              padx=padx, pady=pady, side=side, fill=fill)

        self.create_frame(self.frame_name, self.bg)

    def create_frame(self, frame_name, bg):
        parent = self.guiWindow.frames.get(self.parent_frame, self.guiWindow.root)

        style = ttk.Style()

        style_name = f"{self.frame_name}.TFrame"

        style.configure(
            style_name,
            background=bg,
            fieldbackground=bg,
        )

        self.frame = ttk.Frame(
            parent,
            style=style_name,
            width=self.width,
            height=self.height
        )
        self.frame.pack_propagate(False)

        if self.use_place and self.placement["relx"] is not None and self.placement["rely"] is not None:
            placement_args = {k: v for k, v in self.placement.items() if v is not None}
            self.frame.place(**placement_args)
        else:
            self.frame.pack(anchor="center")

        self.guiWindow.frames[self.frame_name] = self.frame
        return self.frame