import tkinter as tk
from pynput import keyboard
from pynput.keyboard import Key
import threading
import pystray
from PIL import Image, ImageDraw

from capture import capture_screenregion
from clipboard import copy_to_clipboard


class TrayManager:
    def __init__(self, on_screenshot, on_quit):
        self.on_screenshot = on_screenshot
        self.on_quit = on_quit
        self.icon = None

    def _create_icon_image(self):
        img = Image.new("RGB", (64, 64), color=(42, 42, 42))
        draw = ImageDraw.Draw(img)
        draw.rectangle([12, 20, 52, 48], outline="white", width=2)
        draw.rectangle([22, 12, 42, 20], outline="white", width=2)
        draw.ellipse([26, 26, 38, 38], fill="white")
        return img

    def _make_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Сделать скриншот", lambda _: self.on_screenshot()),
            pystray.MenuItem("Выход", lambda _: self.on_quit()),
        )

    def start(self):
        self.icon = pystray.Icon(
            "screenshoter", self._create_icon_image(), "Screenshoter", self._make_menu()
        )
        self.icon.run_detached()

    def stop(self):
        if self.icon:
            self.icon.stop()


class ScreenshotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.is_capturing = False
        self.current_overlay = None

        self.tray = TrayManager(self.trigger_screenshot, self.quit_app)
        self.tray.start()

        listener = keyboard.Listener(on_press=self._on_pynput_key)
        listener.daemon = True
        listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close_window)
        self.root.mainloop()

    def _on_pynput_key(self, key) -> None:
        if self.is_capturing:
            return
        if key == Key.print_screen:
            self.trigger_screenshot()

    def trigger_screenshot(self) -> None:
        if self.is_capturing:
            return
        self.is_capturing = True
        self.root.after(0, self._start_overlay)

    def _start_overlay(self) -> None:
        self.current_overlay = Overlay(self.root, self._on_select, self._on_cancel)
        self.current_overlay.show()

    def _on_select(self, left: int, top: int, right: int, bottom: int) -> None:
        image = capture_screenregion((left, top, right, bottom))
        copy_to_clipboard(image)
        Preview(self.root, image, self._on_save, self._on_close_preview)

    def _on_cancel(self) -> None:
        self.is_capturing = False

    def _on_save(self, path: str) -> None:
        print(f"Saved: {path}")
        self.is_capturing = False

    def _on_close_preview(self) -> None:
        self.is_capturing = False

    def _on_close_window(self) -> None:
        self.root.withdraw()

    def quit_app(self) -> None:
        self.tray.stop()
        self.root.quit()
        self.root.destroy()


class Overlay:
    def __init__(self, parent, on_select, on_cancel):
        self.parent = parent
        self.on_select = on_select
        self.on_cancel = on_cancel
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.top = tk.Toplevel(parent)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-alpha", 0.75)
        self.top.attributes("-topmost", True)
        self.top.configure(bg="black")

        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()

        self.canvas = tk.Canvas(
            self.top, width=screen_w, height=screen_h, bg="black", highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.top.bind("<Escape>", lambda e: self._cancel())

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
            self.top.destroy()
            self.on_select(left, top, right, bottom)
        else:
            self._cancel()

    def _cancel(self) -> None:
        self.top.destroy()
        self.on_cancel()

    def show(self) -> None:
        self.top.grab_set()


class Preview:
    def __init__(self, parent, image, on_save, on_close):
        self.parent = parent
        self.image = image
        self.on_save = on_save
        self.on_close = on_close

        self.top = tk.Toplevel(parent)
        self.top.title("Screenshot")
        self.top.resizable(False, False)
        self.top.attributes("-topmost", True)

        screen_w = self.top.winfo_screenwidth()
        x = screen_w - 420
        y = 50
        self.top.geometry(f"400x350+{x}+{y}")

        self._create_widgets()

        self.top.protocol("WM_DELETE_WINDOW", self._on_close)
        self.top.bind("<Escape>", lambda e: self._on_close())

    def _create_widgets(self) -> None:
        from tkinter import ttk, filedialog
        from PIL import Image as PILImage, ImageTk
        import os
        from datetime import datetime

        preview_frame = ttk.Frame(self.top)
        preview_frame.pack(padx=10, pady=10)

        img_w, img_h = self.image.size
        max_w, max_h = 380, 250

        ratio = min(max_w / img_w, max_h / img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)

        display_img = self.image.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(display_img)

        img_label = ttk.Label(preview_frame, image=self.photo)
        img_label.pack()

        info_label = ttk.Label(preview_frame, text=f"{img_w} x {img_h}", font=("", 9))
        info_label.pack(pady=(5, 0))

        btn_frame = ttk.Frame(self.top)
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
            btn_frame, text="Close", command=self._on_close, width=10
        )
        close_btn.pack(side=tk.LEFT, padx=3)

    def _on_save_click(self) -> None:
        from tkinter import filedialog
        import os
        from datetime import datetime

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
            self.top.destroy()
            self.on_save(file_path)

    def _on_copy_click(self) -> None:
        try:
            print(f"Copy clicked, image: {self.image.mode} {self.image.size}")
            copy_to_clipboard(self.image)
            print("Copied to clipboard")
        except Exception as e:
            print(f"Copy error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self.top.destroy()
            self.on_close()

    def _on_close(self) -> None:
        self.top.destroy()
        self.on_close()


def main() -> None:
    print("Screenshoter started. Press PrintScreen to capture.")
    print("ESC to cancel selection.")
    ScreenshotApp()


if __name__ == "__main__":
    main()
