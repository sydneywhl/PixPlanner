from tkinter import messagebox

import ttkbootstrap as ttk
from PIL import Image, ImageTk

import pix_utility
from backend.log_in_logic import create_one_account
from frontend.log_in import display_log_in_screen


def display_create_account_screen():
    root = ttk.Window(theme="catppuccin-dark")
    root.title("Log in to Pix Planner")
    root.iconbitmap('images/pix_planner_logo.ico') # window's icon

    # the window's size, L x H
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #fullscreen but visible minmax buttons
    root.state("zoomed")

    # STYLES
    style = ttk.Style()
    style.configure("Left.TFrame", background="#5b6ee1")
    style.configure("TitleLabel.TLabel", font=("Montserrat", 40,"bold"))
    style.configure("EntryLabel.TLabel", font=("Montserrat", 20))
    #style.configure("EntryBox.TEntry", font=("Montserrat", 20))
    style.configure("CreateAccount.TButton", font=("Montserrat", 20),focuscolor="")
    style.configure("LogoLabel.TLabel", background="#5b6ee1")
    style.configure("SloganLabel.TLabel", background="#5b6ee1", font=("Montserrat", 20,"italic"))
    style.configure("ErrorLabel.TLabel", font=("Montserrat", 16), foreground="red")

    # MAIN FRAME
    mainFrame = ttk.Frame(root)
    mainFrame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)

    # LEFT FRAME
    leftFrame = ttk.Frame(mainFrame, style="Left.TFrame")
    leftFrame.pack(side="left", fill="both",expand=True)
    # LEFT CONTENT'S INNER FRAME
    leftContent = ttk.Frame(leftFrame, style="Left.TFrame")
    leftContent.pack(expand=True)

    # LEFT CONTENTS
    logoImagePIL = Image.open("images/pix_planner_logo.png").convert("RGBA")
    logoImage = ImageTk.PhotoImage(logoImagePIL)
    logoLabel = ttk.Label(leftContent, image=logoImage, style="LogoLabel.TLabel")
    logoLabel.image = logoImage
    logoLabel.pack(pady=20)

    sloganLabel = ttk.Label(leftContent, text="Planning, one pixel at a time", style="SloganLabel.TLabel")
    sloganLabel.pack(pady=20)

    # RIGHT FRAME
    rightFrame = ttk.Frame(mainFrame)
    rightFrame.pack(side="left", fill="both",expand=True)
    # RIGHT CONTENT'S INNER FRAME
    rightContent = ttk.Frame(rightFrame)
    rightContent.pack(expand=True)

    # RIGHT CONTENTS
    # Title of Log In
    logInLabel = ttk.Label(rightContent, text="Create a new account", style="TitleLabel.TLabel")
    logInLabel.pack(pady=20)

    #USERNAME
    # FRAME to hold label + entry side by side
    usernameFrame = ttk.Frame(rightContent)
    usernameFrame.pack(pady=20)

    # label for "Username:"
    usernameLabel = ttk.Label(usernameFrame, text="Username:", style="EntryLabel.TLabel")
    usernameLabel.pack(side="left", padx=5)

    # text field
    logInUsername= ttk.Entry(usernameFrame, style="EntryBox.TEntry", width=20, font=("Montserrat", 20))
    logInUsername.pack(side="left",pady=20)

    #PASSWORD
    # frame to hold label + entry side by side
    passwordFrame = ttk.Frame(rightContent)
    passwordFrame.pack(pady=20)

    # label for "Password:"
    passwordLabel = ttk.Label(passwordFrame, text="Password:", style="EntryLabel.TLabel")
    passwordLabel.pack(side="left", padx=5)

    # text field
    logInPassword= ttk.Entry(passwordFrame, style="EntryBox.TEntry", show="*", width=20,font=("Montserrat", 20))
    logInPassword.pack(side="left",pady=20)

    # WHEN LOGIN BUTTON IS CLICKED
    def create_account_click():
        username = logInUsername.get()
        password = logInPassword.get()
        if username == "" or password == "":
            show_error_message("Please enter both username and password")
        elif len(password) < 10:
            show_error_message("Password must be at least 10 characters")
        else:
            create_one_account(username, password)
            root.destroy()
            display_log_in_screen()

    # ERROR MESSAGE BELOW THE LOG IN BUTTON
    def show_error_message(message):
         errorLabel.configure(text=message)

    # log in button
    CreateAccountButton = ttk.Button(rightContent, text="Create Account", style="CreateAccount.TButton", cursor="hand2", command=create_account_click)
    CreateAccountButton.pack(pady=20)

    # ERROR LABEL
    errorLabel = ttk.Label(rightContent, text="", style="ErrorLabel.TLabel")
    errorLabel.pack(pady=20)

    root.mainloop()