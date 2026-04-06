import win32clipboard
from PIL import Image
import io
import struct


def copy_to_clipboard(image: Image.Image) -> None:
    """
    Copy a PIL Image to the Windows clipboard.
    """
    output = io.BytesIO()
    image.save(output, format="PNG")
    png_data = output.getvalue()

    img_rgb = image.convert("RGB")
    bmp_data = io.BytesIO()
    img_rgb.save(bmp_data, format="BMP")
    bmp_bytes = bmp_data.getvalue()

    bmp_header = b"\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    bmp_info_header_size = 40

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()

        CF_PNG = win32clipboard.RegisterClipboardFormat("PNG")
        win32clipboard.SetClipboardData(CF_PNG, png_data)

        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_bytes[14:])
    finally:
        win32clipboard.CloseClipboard()
