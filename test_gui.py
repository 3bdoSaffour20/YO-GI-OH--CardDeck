import tkinter as tk
from tkinter import ttk

def test_gui():
    print("Testing tkinter GUI setup...")
    
    try:
        root = tk.Tk()
        root.title("GUI Test")
        root.geometry("400x200")
        
        label = ttk.Label(root, text="Tkinter is working correctly!")
        label.pack(pady=20)
        
        button = ttk.Button(root, text="Close", command=root.quit)
        button.pack(pady=10)
        
        print("✓ Tkinter GUI created successfully")
        print("✓ Widgets (Label, Button) working correctly")
        print("✓ Theme support (ttk) working")
        
        root.mainloop()
        print("✓ GUI test completed successfully")
        
    except Exception as e:
        print(f"✗ GUI test failed: {str(e)}")

if __name__ == "__main__":
    test_gui()
