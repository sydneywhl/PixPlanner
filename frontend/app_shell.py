import ttkbootstrap as ttk

from frontend.sidebar import display_sidebar
from frontend.my_notes import display_my_notes_page
from frontend.note_page_editor import display_note_page_editor
#from frontend.sticky_note_editor import display_sticky_note_editor
from frontend.focus_session import display_focus_session_page
from frontend.trash_bin import display_trash_bin_page
from frontend.settings import display_settings_page
from backend.my_notes_logic import update_note, add_note, delete_note
from backend.trash_bin_logic import restore_note, permanently_delete_note
from backend.sys_tray import create_tray_icon

# APP LAUNCHER AFTER LOG IN
def launch_app():
    root = ttk.Window(theme="catppuccin-dark")
    root.title("Pix Planner")
    root.iconbitmap('images/pix_planner_logo.ico')  # window's icon

    # the window's size, L x H
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # fullscreen but visible minmax buttons
    root.state("zoomed")

    # STYLES
    style = ttk.Style()
    bg_colour = style.lookup("TFrame", "background")

    style.configure("sidebarFrame.TFrame", background="#5b6ee1") # blue colour of sidebar.py
    style.configure("navButtons.TButton", background="white", foreground="black", font=("Montserrat", 12)) #sidebar.py
    style.configure("title.TLabel", font=("Montserrat Bold", 25)) # all titles of pages
    style.configure("title.TEntry", font=("Montserrat Bold", 20)) # entry box of note page editor
    style.configure("iconOnly.TButton", background=bg_colour, borderwidth=0, focuscolor="") # all icons in my_notes.py
    style.map("iconOnly.TButton",
              background=[("active", root.cget("background")), ("pressed", root.cget("background"))],
              foreground=[("active", "#7b8ff5")],
              relief=[("pressed", "flat"), ("active", "flat")])
    style.configure("createNote.TButton", font=("Montserrat", 18)) # create note button at the top of my_notes.py
    style.configure("restoreNote.TButton", font=("Montserrat", 18)) # restore note button at the top of trash_bin.p
    style.configure("focusLabel.TLabel", font=("Montserrat", 25, "italic")) # "how long will you focus?" at focus_session.py
    style.configure("durationFocus.TButton", font=("Montserrat", 18), background="#fff086",foreground="black") # yellow duration buttons at focus_session.py
    style.configure("pinkButton.TButton", font=("Montserrat", 18), background="#f69ad6", foreground="black", width=10) # pink start/pause/end session buttons at focus_session.py
    style.configure("errorLabel.TLabel", font=("Montserrat", 16), foreground="red") # error label at focus_session.py
    style.configure("popupLabel.TLabel", font=("Montserrat", 22))
    style.configure("yesNoButton.TButton", font=("Montserrat", 14), background="#f69ad6", foreground="black") # popup yes/no buttons at focus_session.py



    # MAIN FRAME
    mainFrame = ttk.Frame(root)
    mainFrame.pack(fill="both", expand="True")

    # CONTENT FRAME
    contentFrame = ttk.Frame(mainFrame)

    # to determine what page to display in the contentFrame
    def display_page(page_name, note=None):
        # clear existing content in the contentFrame to put new content when switching pages
        for widget in contentFrame.winfo_children():
            widget.destroy()

        # to determine what page was requested, and then build said page
        if page_name == "my_notes":
            display_my_notes_page(contentFrame, on_open_note=open_note_editor, on_create_note=create_new_note_page)
        elif page_name == "note_page_editor":
            display_note_page_editor(contentFrame, note, on_save=save_note_and_return, on_delete=send_to_trash_bin)
        elif page_name == "trash_preview":
            display_note_page_editor(contentFrame, note,
                                     read_only=True,
                                     on_restore=restore_note_from_trash,
                                     on_delete_forever=delete_note_permanently)
        elif page_name == "focus_session":
            display_focus_session_page(contentFrame)
        elif page_name == "trash_bin":
            display_trash_bin_page(contentFrame, on_open_note=open_trash_preview)
        elif page_name == "settings":
            display_settings_page(contentFrame)

    # UPDATE: OPENS THE NOTE_PAGE_EDITOR FOR AN EXISTING FILE
    # calls display_page() (to widget.destroy) and then display the note_page_editor.py
    def open_note_editor(note):
        display_page("note_page_editor", note=note)

    # ADD: OPENS THE NOTE_PAGE_EDITOR FOR A NEW FILE
    def create_new_note_page():
        blank_note_page = {"note_id": None, "note_name": "", "note_type": "note_page", "note_text": "",
                           "created_at": ""}
        display_page("note_page_editor", note=blank_note_page)

    # SAVES THE NOTES AND RETURNS BACK TO MY_NOTES
    # calls the update_note() from my_notes_logic.py then display_page() (to widget.destroy) and displays my_notes.py
    # calls the add_note() from my_notes_logic.py then add it to the db
    def save_note_and_return(note_id, note_name, note_text,note_type):
        if note_id is None:
            add_note(note_name, note_text,note_type) # note_id is auto added at the db level
        else:
            update_note(note_id, note_name, note_text)
        display_page("my_notes")

    # SENDS NOTES FROM MY_NOTES TO TRASH_BIN
    def send_to_trash_bin(note_id):
        delete_note(note_id)
        display_page("my_notes")

    # ALLOWS USER TO PREVIEW TRASHED NOTES
    def open_trash_preview(note):
        display_page("trash_preview", note=note)

    # ALLOWS USER TO RESTORE TRASHED NOTES
    def restore_note_from_trash(note_id):
        restore_note(note_id)
        display_page("trash_bin")

    # DELETES NOTES IN TRASH BIN PERMANENTLY
    def delete_note_permanently(note_id):
        permanently_delete_note(note_id)
        display_page("trash_bin")









    # display the sidebar on the mainFrame
    display_sidebar(mainFrame, on_nav=display_page)

    # then, pack the contentFrame
    contentFrame.pack(side="left", fill="both", expand=True)

    # default page shown on contentFrame is my_notes
    display_page("my_notes")

    # SYSTEM TRAY FEATURE
    def hide_to_tray():
        root.withdraw()
        create_tray_icon(root)

    root.protocol("WM_DELETE_WINDOW", hide_to_tray)



    root.mainloop()
