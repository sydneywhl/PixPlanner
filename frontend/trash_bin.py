import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk
from backend.trash_bin_logic import get_all_trashed_notes, auto_delete_note


def display_trash_bin_page(contentFrame, on_open_note):
    style = ttk.Style()
    bg_colour = style.lookup("TFrame", "background")

    # MAIN FRAME FOR TITLE AND BUTTONS + SEARCH
    topFrame = ttk.Frame(contentFrame, borderwidth=2, relief="solid")
    topFrame.pack(side="top", fill="x")

    # INNER FRAME FOR TITLE
    titleFrame = ttk.Frame(topFrame, borderwidth=2, relief="solid")
    titleFrame.pack(side="left")

    # TITLE OF CONTENT
    titleLabel = ttk.Label(titleFrame, text="Trash Bin", style="title.TLabel")
    titleLabel.pack(anchor="w", padx=20, pady=0)

    # INNER FRAME FOR BUTTONS + SEARCH
    buttonSearchFrame = ttk.Frame(topFrame)
    buttonSearchFrame.pack(side="right", fill="x", expand=True)

    # BUTTONS FOR CREATE, SEARCH, SORT
    # CREATE BUTTON
    restoreNote = ttk.Button(buttonSearchFrame, text="Restore", style="restoreNote.TButton")
    restoreNote.pack(pady=20, padx=(0, 20), anchor="e")

    # CREATING A SCROLLABLE CANVAS FRAME (SCREEN)
    canvas = tk.Canvas(contentFrame, bg=bg_colour, highlightthickness=0)
    scrollbar = ttk.Scrollbar(contentFrame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # inner frame to hold notesGrid
    scrollableFrame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollableFrame.bind("<Configure>", update_scrollregion)

    # GRID FRAME TO DISPLAY ALL STICKY NOTES AND NOTE BOOK
    notesGrid = ttk.Frame(scrollableFrame)
    notesGrid.pack(fill="both", expand=True, padx=10, pady=10)

    ICON_SIZE = (100, 100)

    # STICKY NOTE ICON
    stickyNotePIL = Image.open("images/app_icons/sticky_note.png").convert("RGBA").resize(ICON_SIZE)
    stickyNote = ImageTk.PhotoImage(stickyNotePIL)

    # NOTE PAGE ICON
    notePagePIL = Image.open("images/app_icons/note_page.png").convert("RGBA").resize(ICON_SIZE)
    notePage = ImageTk.PhotoImage(notePagePIL)

    """# STICKY PAD
    stickyPadPIL = Image.open("images/app_icons/sticky_pad.png").convert("RGBA")
    stickyPad = ImageTk.PhotoImage(stickyPadPIL)
    stickyPadLabel = ttk.Label(contentFrame, image=stickyPad, style="LogoLabel.TLabel")
    stickyPadLabel.image = stickyPad
    stickyPadLabel.pack(pady=20)

    # NOTE BOOK
    noteBookPIL = Image.open("images/app_icons/note_book.png").convert("RGBA")
    noteBook = ImageTk.PhotoImage(noteBookPIL)
    noteBookLabel = ttk.Label(contentFrame, image=noteBook, style="LogoLabel.TLabel")
    noteBookLabel.image = noteBook
    noteBookLabel.pack(pady=20)"""

    # CALL FUNCTION TO DELETE ALL NOTES THAT ARE PAST 30 DAYS
    auto_delete_note()

    # CALL FUNCTION TO FETCH ALL NOTES FROM DB
    notes = get_all_trashed_notes()

    icon_refs = []
    columns = 10

    # create noteFrame for every sticky_note and note_page
    for index, note in enumerate(notes):
        row = index // columns
        col = index % columns

        noteFrame = ttk.Frame(notesGrid, height=100, width=120)
        noteFrame.grid(row=row, column=col, padx=10, pady=15)
        noteFrame.grid_propagate(False)

        # lambda n=note works by assigning the value of note to n, every iteration
        # so it's like the equivalent of every iteration of lambda having its own version of n.
        # Each loop iteration creates a new lambda, and n=note bakes in whatever note equals
        # right then as that lambda's own personal default — so every lambda ends up permanently
        # holding a different, frozen value of n, instead of all of them sharing and looking up
        # the same outer note variable later.

        # DETERMINE WHAT TYPE OF NOTE IS IT, AND APPLY THE CORRECT ICON
        if note["note_type"] == "sticky_note":
            stickyNoteButton = ttk.Button(noteFrame, image=stickyNote, style="iconOnly.TButton", cursor="hand2",
                                          command=lambda n=note: on_open_note(n)
                                          )
            stickyNoteButton.image = stickyNote
            stickyNoteButton.pack(pady=0)
            icon_refs.append(stickyNote)
        elif note["note_type"] == "note_page":
            notePageButton = ttk.Button(noteFrame, image=notePage, style="iconOnly.TButton",
                                        cursor="hand2", command=lambda n=note: on_open_note(n)
                                        )
            notePageButton.image = notePage
            notePageButton.pack(pady=0)
            icon_refs.append(notePage)
        # elif note["note_type"] == "sticky_pad":
        # pass
        # elif note["note_type"] == "note_book":
        # pass

        # MAKING DISPLAY NAMES SHORTER
        if len(note["note_name"]) >= 10:
            removed_letters = len(note["note_name"]) - 10
            shorten_name = note["note_name"][:-removed_letters]
            display_name = shorten_name + "..."

            titleLabel = ttk.Label(noteFrame, text=display_name, font=("Montserrat", 12))
            titleLabel.pack()
        else:
            titleLabel = ttk.Label(noteFrame, text=note["note_name"], font=("Montserrat", 12))
            titleLabel.pack()

