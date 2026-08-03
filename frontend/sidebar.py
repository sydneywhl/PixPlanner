import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk


def display_sidebar(mainFrame, on_nav):
    sidebarFrame = ttk.Frame(mainFrame, width=200, style="sidebarFrame.TFrame")
    sidebarFrame.pack(side="left", fill="y")
    sidebarFrame.pack_propagate(False)

    # SETTINGS BUTTON PAGE
    ttk.Button(sidebarFrame, text="Settings",
               command=lambda: on_nav("settings"), style="navButtons.TButton").pack(fill="x", pady=2, side="bottom")

    # TRASH BIN BUTTON PAGE
    ttk.Button(sidebarFrame, text="Trash Bin",
               command=lambda: on_nav("trash_bin"), style="navButtons.TButton").pack(fill="x", pady=2, side="bottom")

    # FOCUS SESSION BUTTON PAGE
    ttk.Button(sidebarFrame, text="Focus Session",
               command=lambda: on_nav("focus_session"), style="navButtons.TButton").pack(fill="x", pady=2,
                                                                                         side="bottom")
    # MY NOTES BUTTON PAGE
    ttk.Button(sidebarFrame, text="My Notes",
               command=lambda: on_nav("my_notes"), style="navButtons.TButton").pack(fill="x", pady=2, side="bottom")




    return sidebarFrame