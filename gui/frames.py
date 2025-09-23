import tkinter as tk
class guiFrames:
    def __init__(self, guiWindow, frame_name, width=800, height=600,
                 parent_frame=None, use_place=False,
                 relx=None, rely=None, anchor=None, x=None, y=None,
                 padx=None, pady=None, side=None, fill=None, bg="gray25"):
        self.guiWindow = guiWindow
        self.frame_name = frame_name
        self.width = width
        self.height = height
        self.parent_frame = parent_frame
        self.use_place = use_place
        self.bg = bg
        self.placement = dict(relx=relx, rely=rely, anchor=anchor, x=x, y=y,
                              padx=padx, pady=pady, side=side, fill=fill)

        self.create_frame()

    def create_frame(self):
        parent = self.guiWindow.frames.get(self.parent_frame, self.guiWindow.root)

        bg = self.bg if parent != self.guiWindow.root else "gray25"

        self.frame = tk.Frame(parent, bg=bg, width=self.width, height=self.height)
        self.frame.pack_propagate(False)

        # experimental... revisit logic
        if self.use_place and self.placement["relx"] is not None and self.placement["rely"] is not None:
            placement_args = {k: v for k, v in self.placement.items() if v is not None}
            self.frame.place(**placement_args)
        else:
            self.frame.pack(anchor="center")

        self.guiWindow.frames[self.frame_name] = self.frame
        return self.frame
