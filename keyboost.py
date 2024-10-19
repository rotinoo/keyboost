import pyautogui
import keyboard
import tkinter as tk
from tkinter import messagebox
import threading

# Global variables
amplify = False
key_to_amplify = ''
repetitions = 100
pyautogui.PAUSE = 0.05 # Interval of the repetition default 0.1
key_hook = None  # Keep track of the hooked key
stop_repeating = False  # Flag to stop the repetitions

def amplify_key():
    """This function amplifies the key press when the specific key is pressed."""
    global stop_repeating
    print(f"Amplifying '{key_to_amplify}' key {repetitions} times...")
    
    # Reset the stop flag each time a new repetition starts
    stop_repeating = False

    # Perform the repetitions
    for _ in range(repetitions):
        if stop_repeating:  # Check if we should stop
            print("Repetition stopped.")
            break
        pyautogui.press(key_to_amplify)

def start_amplification():
    """Start listening for key presses and amplify the specified key."""
    global amplify, key_to_amplify, repetitions, key_hook, stop_repeating
    key_to_amplify = key_entry.get()
    try:
        repetitions = int(repeat_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for repetitions")
        return

    if not key_to_amplify:
        messagebox.showerror("Invalid Input", "Please enter a key to amplify")
        return

    amplify = True
    toggle_status_label.config(text=f"Status: Amplifying '{key_to_amplify}'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

    # Bind the chosen key to the amplification process
    key_hook = keyboard.on_press_key(key_to_amplify, lambda _: threading.Thread(target=amplify_key).start())

def stop_amplification():
    """Stop listening for key presses and interrupt ongoing repetitions."""
    global amplify, key_hook, stop_repeating
    amplify = False
    stop_repeating = True  # This flag will stop the ongoing repetitions
    toggle_status_label.config(text="Status: Stopped")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

    # Unbind the specific key if it was hooked
    if key_hook is not None:
        keyboard.unhook(key_hook)
        key_hook = None  # Reset key hook to prevent multiple bindings

def f3_pressed():
    """Global hotkey to start amplification when F3 is pressed."""
    if start_button['state'] == 'normal':  # Only start if it's not already running
        start_amplification()

def f4_pressed():
    """Global hotkey to stop amplification when F4 is pressed."""
    if stop_button['state'] == 'normal':  # Only stop if it's running
        stop_amplification()

def create_gui():
    global key_entry, repeat_entry, toggle_status_label, start_button, stop_button

    # Initialize the GUI window
    window = tk.Tk()
    window.title("Key Clicker Amplifier")

    # Key input
    tk.Label(window, text="Key to Amplify:").grid(row=0, column=0)
    key_entry = tk.Entry(window)
    key_entry.grid(row=0, column=1)

    # Repetitions input
    tk.Label(window, text="Number of Repetitions:").grid(row=1, column=0)
    repeat_entry = tk.Entry(window)
    repeat_entry.grid(row=1, column=1)

    # Start/Stop buttons
    start_button = tk.Button(window, text="Start", command=start_amplification)
    start_button.grid(row=2, column=0)

    stop_button = tk.Button(window, text="Stop", command=stop_amplification, state='disabled')
    stop_button.grid(row=2, column=1)

    # Status label
    toggle_status_label = tk.Label(window, text="Status: Stopped")
    toggle_status_label.grid(row=3, column=0, columnspan=2)

    # Register global hotkeys
    keyboard.add_hotkey('F3', f3_pressed)
    keyboard.add_hotkey('F4', f4_pressed)

    # Start the window's main loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
