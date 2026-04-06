import tkinter as tk
from typing import Callable, Optional


class OverlayWindow:
    """
    Full-screen semi-transparent overlay for selecting a screen region.
    """

    def __init__(
        self,
        on_select: Callable[[int, int, int, int], None],
        on_cancel: Callable[[], None],
    ):
        """
        Args:
            on_select: callback(left, top, right, bottom) when selection is made
            on_cancel: callback when selection is cancelled (ESC)
        """
        self.on_select = on_select
        self.on_cancel = on_cancel

        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.rect_id: Optional[int] = None

        self._create_window()

    def _create_window(self) -> None:
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.75)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(
            self.root,
            width=screen_w,
            height=screen_h,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.root.bind("<Escape>", lambda e: self._cancel())

        self.root.update()

    def _on_mouse_down(self, event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="white",
            width=2,
            fill="#1a1a1a",
        )

    def _on_mouse_drag(self, event) -> None:
        if self.rect_id:
            self.canvas.coords(
                self.rect_id, self.start_x, self.start_y, event.x, event.y
            )

    def _on_mouse_up(self, event) -> None:
        end_x = event.x
        end_y = event.y

        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)

        if right - left > 5 and bottom - top > 5:
            self.root.destroy()
            self.on_select(left, top, right, bottom)
        else:
            self._cancel()

    def _cancel(self) -> None:
        self.root.destroy()
        self.on_cancel()

    def show(self) -> None:
        self.root.mainloop()
