import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime
from typing import Callable, Optional


class ScreenshotApp:
    def __init__(self, on_ready: Callable[[], None]):
        self.on_ready = on_ready
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._delayed_ready)

    def _delayed_ready(self) -> None:
        self.on_ready()
        self.root.mainloop()

    def schedule_overlay(self, callback: Callable[[], None]) -> None:
        self.root.after(0, callback)
