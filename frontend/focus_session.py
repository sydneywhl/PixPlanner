from _pyrepl import commands

import ttkbootstrap as ttk
import tkinter as tk
from pix_utility import center_popup
from PIL import Image, ImageTk

def display_focus_session_page(contentFrame):
    style = ttk.Style()
    bg_colour = style.lookup("TFrame", "background")

    # MAIN FRAME FOR TITLE
    topFrame = ttk.Frame(contentFrame)
    topFrame.pack(side="top", fill="x")

    # INNER FRAME FOR TITLE
    titleFrame = ttk.Frame(topFrame)
    titleFrame.pack(side="left")

    # TITLE OF CONTENT
    titleLabel = ttk.Label(titleFrame, text="Focus Session", style="title.TLabel")
    titleLabel.pack(anchor="w", padx=20, pady=20)

    # BOTTOM FRAME FOR THE TIMER
    focusFrame = ttk.Frame(contentFrame)
    focusFrame.pack(expand=True)

    # TITLE OF FOCUS SESSION: HOW LONG WILL YOU FOCUS?
    titleFocusFrame = ttk.Frame(focusFrame)
    titleFocusFrame.pack(expand=True)
    focusLabel = ttk.Label(titleFocusFrame, text="How long will you focus?", style="focusLabel.TLabel")
    focusLabel.pack(anchor="w", padx=20, pady=0)

    # TIMER OF THE FOCUS SESSION HH:MM:SS
    timerLabel = ttk.Label(focusFrame, text="00:00:00", font=("Montserrat", 60, "bold"))
    timerLabel.pack(pady=10)

    def focus_duration(minutes):
        state["seconds_remaining"] = minutes * 60
        update_display()

    # BUTTONS FOR 30 MIN, 1H, 1:30H, 2H
    timeButtonFrame = ttk.Frame(focusFrame)
    timeButtonFrame.pack(pady=20)

    button30Min = ttk.Button(timeButtonFrame, text="30 min", style="durationFocus.TButton",
                             command=lambda: focus_duration(30))
    button30Min.pack(side="left", padx=10)

    button1H = ttk.Button(timeButtonFrame, text="1 hour", style="durationFocus.TButton",
                          command=lambda: focus_duration(60))
    button1H.pack(side="left", padx=10)

    button1H30M = ttk.Button(timeButtonFrame, text="1 hour 30 min", style="durationFocus.TButton",
                             command=lambda: focus_duration(90))
    button1H30M.pack(side="left", padx=10)

    button2H = ttk.Button(timeButtonFrame, text="2 hours", style="durationFocus.TButton",
                          command=lambda: focus_duration(120))
    button2H.pack(side="left", padx=10)

    # FRAME FOR START, PAUSE AND END SESSION
    startButtonFrame = ttk.Frame(focusFrame)
    startButtonFrame.pack()

    duration = 0  # initialisation of 00:00:00

    # keep track of the running countdown so Start/Pause/Reset can all control the same state
    state = {"seconds_remaining": duration * 60, "timer_id": None, "running": False}

    # STARTING THE TIMER
    def start_timer():
        if state["running"]:
            return
        if state["seconds_remaining"] <= 0:
            errorLabel.configure(text="Please select a duration")
            return

        state["running"] = True
        tick()
        timer_running_buttons()
        errorLabel.configure(text="")
        focusLabel.configure(text="Get back to work!")
        pauseButton.configure(text="Pause", command=pause_timer)

    # PAUSING THE TIMER
    def pause_timer():
        if state["timer_id"] is not None:
            contentFrame.after_cancel(state["timer_id"])  # stop the scheduled next tick
            state["timer_id"] = None
        state["running"] = False
        pauseButton.configure(text="Resume", command=resume_timer)

    def resume_timer():
        state["running"] = True
        tick()
        pauseButton.configure(text="Pause", command=pause_timer)

    # RESETTING THE TIMER
    def reset_timer():
        pause_timer()
        state["seconds_remaining"] = duration * 3600
        update_display()

        # BRING BACK THE DURATION AND START BUTTONS
        show_start_button()

    # POPUP FOR CONFIRMING END SESSION
    def confirm_end_session():
        end_popup = tk.Toplevel(contentFrame, background=bg_colour)
        end_popup.title("End session?")
        end_popup.geometry("500x300")
        end_popup.iconbitmap('images/pix_planner_logo.ico')
        end_popup.resizable(False, False)
        end_popup.transient(contentFrame.winfo_toplevel())
        end_popup.grab_set()

        center_popup(end_popup, contentFrame, 500, 300)

        popupFrame = ttk.Frame(end_popup)
        popupFrame.pack(expand=True)

        popupLabel = ttk.Label(popupFrame, text="Are you sure you want to end this session?",
                               font=("Montserrat", 12), wraplength=250, justify="center", style="popupLabel.TLabel")
        popupLabel.pack(pady=10)

        buttonFrame = ttk.Frame(popupFrame)
        buttonFrame.pack(pady=10)

        def confirm_yes():
            end_popup.destroy()
            reset_timer()  # actually ends the session

        def confirm_no():
            end_popup.destroy()  # just closes the popup, session keeps running

        yesButton = ttk.Button(buttonFrame, text="Yes, end session", command=confirm_yes, style="yesNoButton.TButton")
        yesButton.pack(side="left", padx=10)

        noButton = ttk.Button(buttonFrame, text="Cancel", command=confirm_no, style="yesNoButton.TButton")
        noButton.pack(side="left", padx=10)

    # BUTTON FOR "START", PACKED FROM START
    startButton = ttk.Button(startButtonFrame, text="Start!", style="pinkButton.TButton", command=start_timer)
    startButton.pack(side="left")

    # BUTTON FOR "PAUSE", NOT PACKED AT START
    pauseButton = ttk.Button(startButtonFrame, text="Pause", style="pinkButton.TButton", command=pause_timer)

    # BUTTON FOR "END SESSION", NOT PACKED AT START
    resetButton = ttk.Button(startButtonFrame, text="End session", style="pinkButton.TButton",
                             command=confirm_end_session)

    # ERROR LABEL FOR USERS NOT PICKING A DURATION
    errorLabel = ttk.Label(focusFrame, text="", style="errorLabel.TLabel")
    errorLabel.pack(pady=10)

    def timer_running_buttons():
        timeButtonFrame.forget()
        startButton.forget()

        # BUTTON FOR "PAUSE"
        pauseButton.pack(side="left", padx=(0, 30))

        # BUTTON FOR "END SESSION"
        resetButton.pack(side="left")

    def show_start_button():
        pauseButton.pack_forget()
        resetButton.pack_forget()

        startButton.pack(side="left")
        timeButtonFrame.pack(pady=20, before=startButtonFrame) # bring it back — same args as its original .pack() call

        focusLabel.configure(text="How long will you focus?")

    # UPDATE THE 00:00:00
    def update_display():
        minutes, seconds = divmod(state["seconds_remaining"], 60)
        hours, minutes = divmod(minutes, 60)
        timerLabel.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    # COUNTING DOWN THE SECONDS
    def tick():
        if state["seconds_remaining"] <= 0:
            timerLabel.configure(text="Time's up!")
            state["running"] = False
            return

        state["seconds_remaining"] -= 1
        update_display()
        state["timer_id"] = contentFrame.after(1000, tick)  # schedule next tick in 1 second




