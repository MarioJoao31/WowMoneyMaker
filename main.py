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

#focus game window
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
        self.duration_move_forward = tk.Entry(self.root)
        self.duration_move_forward.grid(row=2, column=1, padx=10, pady=5)
        self.duration_move_forward.insert(0, "7")  # Default duration
        # Duration input
        tk.Label(self.root, text="Move Duration (seconds):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.duration_move_backwards = tk.Entry(self.root)
        self.duration_move_backwards.grid(row=3, column=1, padx=10, pady=5)
        self.duration_move_backwards.insert(0, "11")  # Default duration

        #start button 
        tk.Button(self.root, text="Start ", command=self.Start, bg="green", fg="white").grid(row=4, column=0, padx=10, pady=5)

        # Log box
        tk.Label(self.root, text="Logs:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
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

        # Function to simulate character movement
   
    def move_forward(self, duration):
        """
        Simulates holding down the 'W' key for a specific duration.
        Logs the action using the provided log callback.
        """
        self.log_message(f"Moving forward for {duration} seconds...")
        pydirectinput.keyDown('w')  # Press and hold the 'W' key
        time.sleep(duration)        # Wait for the duration
        pydirectinput.keyUp('w')    # Release the 'W' key
        self.log_message("Stopped moving.")

    def move_backwards(self, duration):
        """
        Simulates holding down the 's' key for a specific duration.
        Logs the action using the provided log callback.
        """
        self.log_message(f"Moving Backwards for {duration} seconds...")
        pydirectinput.keyDown('s')  # Press and hold the 'W' key
        time.sleep(duration)        # Wait for the duration
        pydirectinput.keyUp('s')    # Release the 'W' key
        self.log_message("Stopped moving.")

    def Start(self):
        """
        Starts the forward movement.
        """
        try:
            focus_game_window()
            # andar para a frente
            duration_forward = float(self.duration_move_forward.get())  # Get duration from the input field
            self.move_forward(duration_forward)

            # andar para atras
            duration_backwards = float(self.duration_move_backwards.get())  # Get duration from the input field
            self.move_backwards(duration_backwards)


        except ValueError:
            self.log_message("Invalid duration! Please enter a number.")
    


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
