import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import pydirectinput
from datetime import datetime  # Import for timestamps
import win32gui
import win32con
import pygetwindow as gw

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


# Function to simulate character movement
def move_forward(duration, log_callback):
    """
    Simulates holding down the 'W' key for a specific duration.
    Logs the action using the provided log callback.
    """
    log_callback(f"Moving forward for {duration} seconds...")
    pydirectinput.keyDown('w')  # Press and hold the 'W' key
    time.sleep(duration)        # Wait for the duration
    pydirectinput.keyUp('w')    # Release the 'W' key
    log_callback("Stopped moving.")

# Tkinter application class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Movement Manager")

        # Initialize UI components
        self.create_widgets()

        # Thread control variables
        self.running = False
        self.thread = None

    def create_widgets(self):
        # Duration input
        tk.Label(self.root, text="Move Duration (seconds):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=0, column=1, padx=10, pady=5)
        self.duration_entry.insert(0, "3")  # Default duration

        # Start/Stop button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_button, bg="green", fg="white")
        self.start_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Log box
        tk.Label(self.root, text="Logs:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.log_box = scrolledtext.ScrolledText(self.root, width=50, height=10, state="disabled")
        self.log_box.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def log_message(self, message):
        """
        Logs a message to the log box with a timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add timestamp
        formatted_message = f"[{timestamp}] {message}"
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, f"{formatted_message}\n")
        self.log_box.configure(state="disabled")
        self.log_box.see(tk.END)

    def start_button(self):
        """
        Starts the movement in a separate thread.
        """
        if not self.running:
            try:
                #focar na janela do jogo 
                focus_game_window()

                duration = float(self.duration_entry.get())
                self.running = True
                self.start_button.config(text="Stop", bg="red", command=self.stop_movement)
                self.log_message("Starting movement...")

                # Start movement in a new thread
                self.thread = threading.Thread(target=self.run_movement, args=(duration,))
                self.thread.start()
            except ValueError:
                self.log_message("Invalid duration! Please enter a valid number.")

    def run_movement(self, duration):
        """
        Runs the movement logic in a thread-safe way.
        """
        move_forward(duration, self.log_message)
        self.stop_movement()

    def stop_movement(self):
        """
        Stops the movement and resets the UI.
        """
        if self.running:
            self.running = False
            self.start_button.config(text="Start", bg="green", command=self.start_movement)
            self.log_message("Movement stopped.")
            if self.thread and self.thread.is_alive():
                self.thread.join()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
