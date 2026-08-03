from PIL import Image
import threading
import pystray

def create_tray_icon(root):
    icon_image = Image.open("images/pix_planner_logo.png")

    # RESTORE THE WINDOW FROM THE SYSTEM TRAY
    def restore_window(icon, item):
        icon.stop()
        root.after(0, lambda: (root.deiconify(), root.state("zoomed"))) # bring the window back on the main thread

    # COMPLETELY QUIT THE APP
    def quit_app(icon, item):
        icon.stop()
        root.after(0, root.destroy)

    # MENU OF THE SYSTEM TRAY (RIGHT CLICK)
    menu = pystray.Menu(
        pystray.MenuItem("Open Pix Planner", restore_window, default=True),
        pystray.MenuItem("Quit", quit_app)
        #pystray.MenuItem("Add Sticky Note", create_tray_icon)
        #pystray.MenuItem("Add Note Page", create_tray_icon)
    )

    tray_icon = pystray.Icon("PixPlanner", icon_image, "Pix Planner", menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()
    # non-daemon (important, must finish, wait for completion before allowing program to exit)
    # daemon (bg helper, can dispose): wont wait for this thread to finish before main thread exits
    # if main thread ends(or once there is no more non-daemon threads running),
    # this thread ends too
    # new thread bc this tray_icon.run() is blocking, cant run tgt with root.mainloop()