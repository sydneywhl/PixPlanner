import tkinter as tk

def add_tooltip(widget, text):
    tooltip = None

    def show_tooltip(event):
        nonlocal tooltip
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)   # removes window border/title bar
        x = widget.winfo_rootx() + 25
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tooltip, text=text, background="#333333", foreground="white",
                          font=("Montserrat", 10), padx=8, pady=4)
        label.pack()

    def hide_tooltip(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)