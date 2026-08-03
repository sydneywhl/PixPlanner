import ctypes
import os

def load_font_windows(path):
    FR_PRIVATE = 0x10
    path = os.path.abspath(path)
    ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)

# LOADING THE MONTSERRAT FONTS
def load_all_fonts():
    load_font_windows("fonts/Montserrat-Italic.ttf")
    load_font_windows("fonts/Montserrat-Regular.ttf")
    load_font_windows("fonts/Montserrat-ExtraBold.ttf")
    load_font_windows("fonts/Montserrat-Bold.ttf")

# CENTERING ALL POPUPS
def center_popup(popup, parent_widget, width, height):
    popup.update_idletasks()

    parent = parent_widget.winfo_toplevel()
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    popup.geometry(f"{width}x{height}+{x}+{y}")