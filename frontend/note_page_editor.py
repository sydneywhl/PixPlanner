import ttkbootstrap as ttk
import tkinter as tk
from backend.my_notes_logic import update_note
from PIL import Image, ImageTk

# FOR UPDATING EXISTING NOTES
def display_note_page_editor(contentFrame, note, on_save=None, read_only=False, on_restore=None, on_delete_forever=None, on_delete=None):
    style = ttk.Style()
    bg_colour = style.lookup("TFrame", "background")

    # TITLE OF THE NOTE
    titleEntry = ttk.Entry(contentFrame, font=("Montserrat", 20), style="title.TEntry")
    titleEntry.insert(0, note["note_name"])
    titleEntry.pack(pady=20, fill="x", padx=20)

    # TEXT AREA (LEFT FRAME)
    editorFrame = ttk.Frame(contentFrame)
    editorFrame.pack(side="left", fill="both", expand="True")

    bodyText = tk.Text(editorFrame, font=("Montserrat", 14), wrap="word", background=bg_colour,
                       foreground="white", insertbackground="white")
    bodyText.insert("1.0", note["note_text"])
    bodyText.pack(pady=10, fill="both", expand=True, padx=20)

    # ACTION AREA (RIGHT FRAME)
    actionFrame = ttk.Frame(contentFrame, width=150, borderwidth=1)
    actionFrame.pack(side="right", fill="y", pady=10)
    actionFrame.pack_propagate(False)

    # FOR TRASHED NOTES
    if read_only:
        titleEntry.configure(state="disabled")
        bodyText.configure(state="disabled")

        restoreButton = ttk.Button(actionFrame, text="Restore", command=lambda: on_restore(note["note_id"]),  width=100)
        restoreButton.pack(pady=(0, 10), padx=(0, 20))

        deleteForeverButton = ttk.Button(actionFrame, text="Delete Forever",
                                         command=lambda: on_delete_forever(note["note_id"]), width=100)
        deleteForeverButton.pack(pady=(0, 10), padx=(0, 20))

    #FOR NOTES
    else:
        # SAVE/UPDATE TEXT TO DB: calls on_save
        def save_and_close():
            updated_title = titleEntry.get()
            updated_body = bodyText.get("1.0", "end-1c")
            on_save(note["note_id"], updated_title, updated_body, note["note_type"])

        saveButton = ttk.Button(actionFrame, text="Save", command=save_and_close, width=80)
        saveButton.pack(pady=(0,10), padx=(0,20))

        deleteForeverButton = ttk.Button(actionFrame, text="Delete",
                                         command=lambda: on_delete(note["note_id"]), width=100)
        deleteForeverButton.pack(pady=(0, 10), padx=(0, 20))


