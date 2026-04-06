import mss
import numpy as np
from PIL import Image


def capture_screenregion(region: tuple[int, int, int, int]) -> Image.Image:
    """
    Capture a screen region.

    Args:
        region: (left, top, right, bottom) - coordinates of the region to capture

    Returns:
        PIL Image object in PNG quality
    """
    with mss.mss() as sct:
        monitor = {
            "left": region[0],
            "top": region[1],
            "width": region[2] - region[0],
            "height": region[3] - region[1],
        }
        screenshot = sct.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        return img


def get_full_screen_size() -> tuple[int, int]:
    """Get the dimensions of the primary monitor."""
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        return monitor["width"], monitor["height"]


def capture_full_screen() -> Image.Image:
    """Capture the entire primary monitor."""
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        screenshot = sct.grab(monitor)
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)


__all__ = ["capture_screenregion", "capture_full_screen"]
