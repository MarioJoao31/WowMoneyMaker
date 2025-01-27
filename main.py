import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import pydirectinput
from datetime import datetime
import win32gui
import win32con
import pygetwindow as gw
from pynput import mouse  # For mouse event listening


mailXY = []
auctionXY = []

def focus_game_window(window_title="World of Warcraft"):
    """
    Focuses on the specified game window by title.
    """
    try:
        # Find the window
        game_window = None
        for window in gw.getAllTitles():
            if window_title.lower() in window.lower():
                game_window = window
                break

        if not game_window:
            print(f"Window with title '{window_title}' not found!")
            return False

        # Get the window handle
        hwnd = win32gui.FindWindow(None, game_window)

        # Bring the window to the foreground
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
        win32gui.SetForegroundWindow(hwnd)  # Focus on the window
        print(f"Focused on window: {game_window}")
        return True

    except Exception as e:
        print(f"Error focusing on window: {e}")
        return False

# Tkinter application class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Preto Escravo")

        # Initialize UI components
        self.create_widgets()

        # Variables for mouse listener
        self.mouse_listener = None

    def create_widgets(self):
        # Button to capture mouse position on the next click
        tk.Label(self.root, text="Mail coordenates").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self.root, text="Mail x,y", command=self.start_mouse_listener_mail, bg="green", fg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.root, text="auction coordenates").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self.root, text="Auction x,y", command=self.start_mouse_listener_auction, bg="green", fg="white").grid(row=1, column=1, padx=10, pady=5)

        # Duration input
        tk.Label(self.root, text="Move Duration (seconds):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)
        self.duration_entry.insert(0, "5")  # Default duration

        # Log box
        tk.Label(self.root, text="Logs:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.log_box = scrolledtext.ScrolledText(self.root, width=60, height=10, state="disabled")
        self.log_box.grid(row=5, column=0, padx=5, pady=2)

    def log_message(self, message):
        """
        Logs a message to the log box with a timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, f"{formatted_message}\n")
        self.log_box.configure(state="disabled")
        self.log_box.see(tk.END)

    def start_mouse_listener_mail(self):
        """
        Starts a listener for the next mouse click to capture coordinates.
        """
        self.log_message("Waiting for the next mouse click...")
        
        #focar janela
        focus_game_window()

        def on_click(x, y, button, pressed):
            if pressed:  # Only capture on the mouse button press
                self.log_message(f"Mouse clicked at X={x}, Y={y}")
                mailXY.append(x)
                mailXY.append(y)
                print(mailXY)
                # Stop the listener after capturing the click
                return False

        # Start the mouse listener
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()
    
    def start_mouse_listener_auction(self):
        """
        Starts a listener for the next mouse click to capture coordinates.
        """
        self.log_message("Waiting for the next mouse click...")
        
        #focar janela
        focus_game_window()

        def on_click(x, y, button, pressed):
            if pressed:  # Only capture on the mouse button press
                self.log_message(f"Mouse clicked at X={x}, Y={y}")
                auctionXY.append(x)
                auctionXY.append(y)
                print(mailXY)
                # Stop the listener after capturing the click
                return False

        # Start the mouse listener
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
