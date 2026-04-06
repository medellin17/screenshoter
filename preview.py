import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime
from typing import Callable, Optional

from clipboard import copy_to_clipboard


class PreviewWindow:
    """
    Small preview window after screenshot capture.
    Offers options to save to file or close.
    """

    def __init__(
        self,
        image: Image.Image,
        on_save: Callable[[str], None],
        on_close: Callable[[], None],
    ):
        """
        Args:
            image: PIL Image to preview
            on_save: callback with chosen file path
            on_close: callback when closed without saving
        """
        self.image = image
        self.on_save = on_save
        self.on_close = on_close

        self.file_path: Optional[str] = None

        self._create_window()

    def _create_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Screenshot")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        screen_w = self.root.winfo_screenwidth()
        x = screen_w - 420
        y = 50
        self.root.geometry(f"400x350+{x}+{y}")

        self._create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close_click)
        self.root.bind("<Escape>", lambda e: self._on_close_click())

    def _create_widgets(self) -> None:
        preview_frame = ttk.Frame(self.root)
        preview_frame.pack(padx=10, pady=10)

        img_w, img_h = self.image.size
        max_w, max_h = 380, 250

        ratio = min(max_w / img_w, max_h / img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)

        display_img = self.image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(display_img)

        img_label = ttk.Label(preview_frame, image=self.photo)
        img_label.pack()

        info_label = ttk.Label(preview_frame, text=f"{img_w} x {img_h}", font=("", 9))
        info_label.pack(pady=(5, 0))

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        save_btn = ttk.Button(
            btn_frame, text="Save", command=self._on_save_click, width=10
        )
        save_btn.pack(side=tk.LEFT, padx=3)

        copy_btn = ttk.Button(
            btn_frame, text="Copy", command=self._on_copy_click, width=10
        )
        copy_btn.pack(side=tk.LEFT, padx=3)

        close_btn = ttk.Button(
            btn_frame, text="Close", command=self._on_close_click, width=10
        )
        close_btn.pack(side=tk.LEFT, padx=3)

    def _on_save_click(self) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_name = f"screenshot_{timestamp}.png"

        downloads = os.path.join(os.path.expanduser("~"), "Downloads")

        initial_file = os.path.join(downloads, default_name)

        file_path = filedialog.asksaveasfilename(
            initialfile=initial_file,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Screenshot",
        )

        if file_path:
            self.image.save(file_path, "PNG")
            self.file_path = file_path
            self.root.destroy()
            self.on_save(file_path)
        else:
            pass

    def _on_copy_click(self) -> None:
        try:
            copy_to_clipboard(self.image)
            self.root.destroy()
            self.on_close()
        except Exception as e:
            print(f"Copy error: {e}")

    def _on_close_click(self) -> None:
        self.root.destroy()
        self.on_close()

    def show(self) -> None:
        self.root.mainloop()
