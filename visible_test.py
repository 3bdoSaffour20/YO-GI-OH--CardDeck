import tkinter as tk
from tkinter import ttk
import time

def create_visible_test():
    root = tk.Tk()
    root.title("Visible Test Window")
    root.geometry("300x200")
    
    # Create a label that will show test results
    result_label = ttk.Label(root, text="Starting test...", font=("Arial", 12))
    result_label.pack(pady=20)
    
    # Create a progress bar
    progress = ttk.Progressbar(root, length=250, mode='indeterminate')
    progress.pack(pady=10)
    progress.start()
    
    # Create a button to close
    close_btn = ttk.Button(root, text="Close Test", command=root.quit)
    close_btn.pack(pady=10)
    
    # Update the label after a delay to simulate testing
    def update_test():
        result_label.config(text="Test completed successfully!\nGUI is working.")
        progress.stop()
        progress.config(mode='determinate', value=100)
    
    root.after(2000, update_test)  # Update after 2 seconds
    
    root.mainloop()

if __name__ == "__main__":
    create_visible_test()
