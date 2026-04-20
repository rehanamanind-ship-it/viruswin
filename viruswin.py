import tkinter as tk
from tkinter import ttk
import winsound
import os
import random
import ctypes  # used for minimizing other windows via Win32 API

# pillow is needed to display jpeg images
from PIL import Image, ImageTk
import base64
from io import BytesIO

def load_embedded_image(image_name):
    """Load an image from the embedded base64 data."""
    try:
        with open("embedded_images.txt", "r") as f:
            content = f.read()
        
        # Find the image data
        start = content.find(f"{image_name} = '''") + len(f"{image_name} = '''")
        end = content.find("'''", start)
        if start == -1 or end == -1:
            return None
        
        base64_data = content[start:end].strip()
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_bytes))
        return image
    except Exception:
        return None


spawn_windows = []
timer_id = None

def on_extra_window_closing(window):
    """Handle closing events for spawned windows."""
    window.withdraw()
    window.deiconify()
    # Play sound when window reopens
    winsound.MessageBeep()
    winsound.Beep(800, 200)

def check_extra_windows_minimized():
    """Check if any spawned windows are minimized and restore them."""
    global spawn_windows
    for window in spawn_windows:
        try:
            if window.state() == "iconic":
                window.state("normal")
                window.lift()
                # Play sound when window is restored from minimized
                winsound.MessageBeep()
                winsound.Beep(800, 200)
        except tk.TclError:
            # Window was destroyed
            pass
    root.after(100, check_extra_windows_minimized)

def move_windows_randomly():
    """Move spawned windows to random positions on the screen."""
    global spawn_windows
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    for window in spawn_windows:
        try:
            # Generate random position
            random_x = random.randint(0, max(0, screen_width - 300))
            random_y = random.randint(0, max(0, screen_height - 200))
            window.geometry(f"300x200+{random_x}+{random_y}")
        except tk.TclError:
            pass
    
    root.after(500, move_windows_randomly)

def spawn_extra_windows():
    """Spawn additional prank windows (four text messages, one meme image, and two extra images).

    The windows are all 300x200 and will be moved randomly once created.
    """
    global spawn_windows
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Define positions for the 4 text windows in a pattern around the screen
    positions = [
        (0, 0),  # Top-left
        (screen_width - 300, 0),  # Top-right
        (0, screen_height - 200),  # Bottom-left
        (screen_width - 300, screen_height - 200)  # Bottom-right
    ]
    
    # spawn the four "you are dumb" windows
    for i in range(4):
        winsound.MessageBeep()
        winsound.Beep(800, 200)
        
        extra_window = tk.Toplevel(root)
        extra_window.title("Window " + str(i+1))
        extra_window.geometry(f"300x200+{positions[i][0]}+{positions[i][1]}")
        extra_window.resizable(False, False)
        extra_window.attributes('-topmost', True)
        extra_window.protocol("WM_DELETE_WINDOW", lambda w=extra_window: on_extra_window_closing(w))
        ttk.Label(extra_window, text="You are dum dum lunatic idiot", font=("Arial", 14)).pack(pady=50)
        spawn_windows.append(extra_window)
    
    # spawn the fifth window showing the Mike Wazowski meme
    winsound.MessageBeep()
    winsound.Beep(800, 200)
    img = load_embedded_image("Mike viruswin.jpeg")
    if img:
        img = img.resize((300, 200))
        photo = ImageTk.PhotoImage(img)
    else:
        photo = None
    
    extra_window = tk.Toplevel(root)
    extra_window.title("Window 5")
    # center of the screen
    center_x = (screen_width - 300) // 2
    center_y = (screen_height - 200) // 2
    extra_window.geometry(f"300x200+{center_x}+{center_y}")
    extra_window.resizable(False, False)
    extra_window.attributes('-topmost', True)
    extra_window.protocol("WM_DELETE_WINDOW", lambda w=extra_window: on_extra_window_closing(w))
    if photo:
        lbl = ttk.Label(extra_window, image=photo)
        lbl.image = photo  # keep reference
        lbl.pack()
    else:
        ttk.Label(extra_window, text="[image]", font=("Arial", 14)).pack(pady=50)
    spawn_windows.append(extra_window)
    
    # spawn two more prank windows (cat and troll images) with random start positions
    for img_name, title in [("catwin.jpeg", "Cat Window"), ("trollwin.jpg", "Troll Window")]:
        winsound.MessageBeep()
        winsound.Beep(800, 200)
        img = load_embedded_image(img_name)
        if img:
            img = img.resize((300, 200))
            photo = ImageTk.PhotoImage(img)
        else:
            photo = None
        extra_window = tk.Toplevel(root)
        extra_window.title(title)
        # start at a random position
        rand_x = random.randint(0, max(0, screen_width - 300))
        rand_y = random.randint(0, max(0, screen_height - 200))
        extra_window.geometry(f"300x200+{rand_x}+{rand_y}")
        extra_window.resizable(False, False)
        extra_window.attributes('-topmost', True)
        extra_window.protocol("WM_DELETE_WINDOW", lambda w=extra_window: on_extra_window_closing(w))
        if photo:
            lbl = ttk.Label(extra_window, image=photo)
            lbl.image = photo
            lbl.pack()
        else:
            ttk.Label(extra_window, text="[image]", font=("Arial", 14)).pack(pady=50)
        spawn_windows.append(extra_window)
    
    # Start moving windows randomly
    move_windows_randomly()

def show_start_menu():
    """Restore the taskbar / start menu that we previously hid."""
    user32 = ctypes.windll.user32
    SW_SHOW = 5
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, SW_SHOW)


def hide_start_menu():
    """Hide the taskbar/start menu by hiding the Shell_TrayWnd window."""
    user32 = ctypes.windll.user32
    SW_HIDE = 0
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, SW_HIDE)


def ensure_start_menu_hidden():
    """Keep attempting to hide the start menu periodically.

    The user can still bring up the menu with the Windows key so we
    repeatedly hide the taskbar to make it harder to use.
    """
    hide_start_menu()
    root.after(1000, ensure_start_menu_hidden)


def kill_program():
    """Terminate the prank and restore normal desktop state.

    This can be invoked from the hot‑key thread or by the password
    check; the caller should use ``root.after`` if running from a
    different thread.
    """
    global timer_id
    # cancel pending timer
    if timer_id:
        root.after_cancel(timer_id)
    # destroy any extra windows
    for window in spawn_windows:
        try:
            window.destroy()
        except Exception:
            pass
    show_start_menu()
    try:
        root.destroy()
    except Exception:
        pass


def check_password():
    """Check if the entered password is correct."""
    global timer_id
    
    password = password_entry.get()
    if password == "1357":
        # Cancel the timer if correct password is entered
        if timer_id:
            root.after_cancel(timer_id)
        # Close all spawned windows
        for window in spawn_windows:
            window.destroy()
        show_start_menu()
        root.destroy()
    else:
        password_entry.delete(0, tk.END)
        status_label.config(text="Incorrect password, try again!")

def on_closing():
    """Handle window close event by recreating the window."""
    root.withdraw()
    root.deiconify()


def check_minimized():
    """Restore the main window immediately if it's minimized."""
    if root.state() == "iconic":
        root.state("normal")
        root.lift()
    root.after(100, check_minimized)


def minimize_other_windows():
    """Minimize all visible top‑level windows except VS Code and this program.

    This uses the Windows API via ctypes so there is no external dependency. We
    skip windows whose title contains "Visual Studio Code" (the editor) or our
    own main window title, and ignore empty titles. The function can be run
    once at startup and periodically to keep other apps minimized while the
    prank is running.
    """
    user32 = ctypes.windll.user32
    SW_MINIMIZE = 6

    def enum_callback(hwnd, lParam):
        # only consider visible windows
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            # skip the main tkinter window and VS Code itself
            if title == "hacked baby!" or "Visual Studio Code" in title:
                return True
            # skip windows without a title (tooltips, etc.)
            if not title.strip():
                return True
            # minimize everything else
            user32.ShowWindow(hwnd, SW_MINIMIZE)
        return True

    enum_func = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(enum_callback)
    user32.EnumWindows(enum_func, 0)


def periodic_minimize():
    """Periodically minimize other windows every few seconds."""
    minimize_other_windows()
    root.after(5000, periodic_minimize)


def start_password_timer():
    """Start a 10-second timer to spawn windows if password not entered."""
    global timer_id
    timer_id = root.after(10000, spawn_extra_windows)

# Create the main window
root = tk.Tk()
root.title("hacked baby!")
root.geometry("700x600")
# prevent resizing (disables maximize) and keep fixed shape
root.resizable(False, False)

# Make the window always on top
root.attributes('-topmost', True)

# Prevent the window from closing normally
root.protocol("WM_DELETE_WINDOW", on_closing)

# Add a label
ttk.Label(root, text="Enter password to save yourself!").pack(pady=20)

# Add a text entry widget for password
password_entry = ttk.Entry(root, width=30, show="*")
password_entry.pack(pady=10)

# Add a submit button
submit_button = ttk.Button(root, text="Submit", command=check_password)
submit_button.pack(pady=10)

# Add a status label
status_label = ttk.Label(root, text="", foreground="red")
status_label.pack(pady=10)



# Start the 10-second password timer
start_password_timer()

# Restore main window if someone minimizes it
check_minimized()

# minimize all other windows immediately and then periodically
minimize_other_windows()
periodic_minimize()

# Start checking spawned windows
check_extra_windows_minimized()

# hide the taskbar/start menu and keep it hidden
hide_start_menu()
ensure_start_menu_hidden()

# ---------------------------------------------------------------------
# global hotkey listener for the letter "K".  we register hotkey
# K (no modifiers) and simply shut down when the message arrives. a
# small fallback keeps the behaviour when our window is focused.
# ---------------------------------------------------------------------
import threading

def _hotkey_thread():
    user32 = ctypes.windll.user32
    MOD_NONE = 0x0000
    VK_K = 0x4B
    # arbitrary identifier
    if not user32.RegisterHotKey(None, 1, MOD_NONE, VK_K):
        return
    msg = ctypes.wintypes.MSG()
    while True:
        if user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == 0x0312:  # WM_HOTKEY
                root.after(0, kill_program)
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

threading.Thread(target=_hotkey_thread, daemon=True).start()

# fallback: detect "k" keypress when our window has focus
pressed = set()

def _on_key_press(event):
    pressed.add(event.keysym)
    if "k" in pressed or "K" in pressed:
        kill_program()

def _on_key_release(event):
    pressed.discard(event.keysym)

root.bind_all("<KeyPress>", _on_key_press)
root.bind_all("<KeyRelease>", _on_key_release)

# Start the application event loop
root.mainloop()