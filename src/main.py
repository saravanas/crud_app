import tkinter as tk
from ui.app import CRUDApp
import sys
import os

def main():
    # Ensure the data directory exists for the database
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    
    # Create the main window
    root = tk.Tk()
    root.geometry("600x600")
    app = CRUDApp(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
