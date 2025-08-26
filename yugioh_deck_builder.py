import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from PIL import Image, ImageTk
import io
import json
import os

class YugiohDeckBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Yu-Gi-Oh! Deck Builder")
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.current_deck = []
        self.all_cards = []
        self.current_theme = "light"
        self.card_images = {}
        
        # Setup theme colors
        self.setup_themes()
        
        # Create GUI
        self.create_menu()
        self.create_main_frame()
        self.create_search_frame()
        self.create_card_list_frame()
        self.create_deck_frame()
        self.create_details_frame()
        
        # Load initial data
        self.load_initial_cards()
    
    def setup_themes(self):
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#e0e0e0",
                "button_fg": "#000000",
                "list_bg": "#ffffff",
                "list_fg": "#000000",
                "highlight": "#0078d7"
            },
            "dark": {
                "bg": "#2d2d30",
                "fg": "#ffffff",
                "button_bg": "#3e3e42",
                "button_fg": "#ffffff",
                "list_bg": "#1e1e1e",
                "list_fg": "#ffffff",
                "highlight": "#0078d7"
            }
        }
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Deck", command=self.new_deck)
        file_menu.add_command(label="Open Deck", command=self.open_deck)
        file_menu.add_command(label="Save Deck", command=self.save_deck)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        view_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_search_frame(self):
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search Cards:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.filter_cards)
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_cards)
        search_btn.pack(side=tk.LEFT)
    
    def create_card_list_frame(self):
        # Left frame for card list
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Available Cards").pack(anchor=tk.W)
        
        # Card list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.card_listbox = tk.Listbox(list_frame, height=20)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.card_listbox.yview)
        self.card_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.card_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.card_listbox.bind('<<ListboxSelect>>', self.on_card_select)
        
        # Add to deck button
        add_btn = ttk.Button(left_frame, text="Add to Deck", command=self.add_to_deck)
        add_btn.pack(pady=(5, 0))
    
    def create_deck_frame(self):
        # Middle frame for current deck
        middle_frame = ttk.Frame(self.main_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)
        
        ttk.Label(middle_frame, text="Current Deck").pack(anchor=tk.W)
        
        # Deck list with scrollbar
        deck_frame = ttk.Frame(middle_frame)
        deck_frame.pack(fill=tk.BOTH, expand=True)
        
        self.deck_listbox = tk.Listbox(deck_frame, height=20)
        deck_scrollbar = ttk.Scrollbar(deck_frame, orient=tk.VERTICAL, command=self.deck_listbox.yview)
        self.deck_listbox.configure(yscrollcommand=deck_scrollbar.set)
        
        self.deck_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        deck_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deck_listbox.bind('<<ListboxSelect>>', self.on_deck_card_select)
        
        # Deck management buttons
        btn_frame = ttk.Frame(middle_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        remove_btn = ttk.Button(btn_frame, text="Remove from Deck", command=self.remove_from_deck)
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(btn_frame, text="Clear Deck", command=self.clear_deck)
        clear_btn.pack(side=tk.LEFT)
    
    def create_details_frame(self):
        # Right frame for card details
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="Card Details").pack(anchor=tk.W)
        
        # Card image
        self.card_image_label = ttk.Label(right_frame, text="Select a card to view details")
        self.card_image_label.pack(pady=10)
        
        # Card details text
        details_frame = ttk.Frame(right_frame)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(details_frame, height=15, width=40, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Make details text read-only
        self.details_text.config(state=tk.DISABLED)
    
    def fetch_card_data(self, card_name):
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for card in data['data']:
                    if card['name'].lower() == card_name.lower():
                        return card
                return None
            else:
                messagebox.showerror("Error", f"API Error: {response.status_code}")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch card data: {str(e)}")
            return None
    
    def fetch_card_image(self, image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((200, 300), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            return None
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def load_initial_cards(self):
        # Load some popular cards initially
        popular_cards = [
            "Dark Magician", "Blue-Eyes White Dragon", "Red-Eyes Black Dragon",
            "Exodia the Forbidden One", "Summoned Skull", "Celtic Guardian"
        ]
        
        for card_name in popular_cards:
            card_data = self.fetch_card_data(card_name)
            if card_data:
                self.all_cards.append(card_data)
                self.card_listbox.insert(tk.END, card_data['name'])
    
    def search_cards(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            return
        
        card_data = self.fetch_card_data(search_term)
        if card_data:
            # Clear current list and add the found card
            self.card_listbox.delete(0, tk.END)
            self.all_cards = [card_data]
            self.card_listbox.insert(tk.END, card_data['name'])
        else:
            messagebox.showinfo("Not Found", f"Card '{search_term}' not found.")
    
    def filter_cards(self, event):
        search_term = self.search_var.get().lower()
        self.card_listbox.delete(0, tk.END)
        
        for card in self.all_cards:
            if search_term in card['name'].lower():
                self.card_listbox.insert(tk.END, card['name'])
    
    def on_card_select(self, event):
        selection = self.card_listbox.curselection()
        if not selection:
            return
        
        card_name = self.card_listbox.get(selection[0])
        card_data = next((card for card in self.all_cards if card['name'] == card_name), None)
        
        if card_data:
            self.display_card_details(card_data)
    
    def on_deck_card_select(self, event):
        selection = self.deck_listbox.curselection()
        if not selection:
            return
        
        card_name = self.deck_listbox.get(selection[0])
        card_data = next((card for card in self.current_deck if card['name'] == card_name), None)
        
        if card_data:
            self.display_card_details(card_data)
    
    def display_card_details(self, card_data):
        # Clear previous details
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        # Display card information
        details = f"Name: {card_data['name']}\n\n"
        details += f"Type: {card_data['type']}\n"
        details += f"Race: {card_data.get('race', 'N/A')}\n"
        details += f"Attribute: {card_data.get('attribute', 'N/A')}\n"
        
        if 'atk' in card_data:
            details += f"ATK: {card_data['atk']}\n"
        if 'def' in card_data:
            details += f"DEF: {card_data['def']}\n"
        if 'level' in card_data:
            details += f"Level: {card_data['level']}\n"
        
        details += f"\nDescription:\n{card_data['desc']}"
        
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        
        # Load and display card image
        if 'card_images' in card_data and card_data['card_images']:
            image_url = card_data['card_images'][0]['image_url']
            photo = self.fetch_card_image(image_url)
            if photo:
                self.card_image_label.config(image=photo)
                self.card_image_label.image = photo
            else:
                self.card_image_label.config(text="Image not available")
        else:
            self.card_image_label.config(text="Image not available")
    
    def add_to_deck(self):
        selection = self.card_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a card to add to your deck.")
            return
        
        card_name = self.card_listbox.get(selection[0])
        card_data = next((card for card in self.all_cards if card['name'] == card_name), None)
        
        if card_data:
            self.current_deck.append(card_data)
            self.deck_listbox.insert(tk.END, card_data['name'])
            messagebox.showinfo("Success", f"Added {card_name} to your deck!")
        else:
            messagebox.showerror("Error", "Could not add card to deck.")
    
    def remove_from_deck(self):
        selection = self.deck_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a card to remove from your deck.")
            return
        
        card_name = self.deck_listbox.get(selection[0])
        card_index = selection[0]
        
        self.current_deck.pop(card_index)
        self.deck_listbox.delete(card_index)
    
    def clear_deck(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear your entire deck?"):
            self.current_deck.clear()
            self.deck_listbox.delete(0, tk.END)
    
    def new_deck(self):
        if self.current_deck and not messagebox.askyesno("Confirm", "Create new deck? Current deck will be lost."):
            return
        
        self.current_deck.clear()
        self.deck_listbox.delete(0, tk.END)
        messagebox.showinfo("New Deck", "Created a new empty deck.")
    
    def save_deck(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Your deck is empty. Nothing to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Save only essential card data
                deck_data = []
                for card in self.current_deck:
                    deck_data.append({
                        'id': card['id'],
                        'name': card['name'],
                        'type': card['type']
                    })
                
                with open(file_path, 'w') as f:
                    json.dump(deck_data, f, indent=2)
                
                messagebox.showinfo("Success", "Deck saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save deck: {str(e)}")
    
    def open_deck(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    deck_data = json.load(f)
                
                self.current_deck.clear()
                self.deck_listbox.delete(0, tk.END)
                
                for card_info in deck_data:
                    # Fetch full card data for each card in the deck
                    card_data = self.fetch_card_data(card_info['name'])
                    if card_data:
                        self.current_deck.append(card_data)
                        self.deck_listbox.insert(tk.END, card_data['name'])
                
                messagebox.showinfo("Success", "Deck loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load deck: {str(e)}")
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Update all widgets with new theme colors
        widgets_to_update = [
            self.root, self.main_frame, self.card_listbox, self.deck_listbox,
            self.details_text, self.card_image_label
        ]
        
        for widget in widgets_to_update:
            try:
                widget.config(bg=theme['bg'])
                if hasattr(widget, 'config') and 'fg' in widget.config():
                    widget.config(fg=theme['fg'])
            except:
                pass
        
        # Update specific widgets
        self.card_listbox.config(bg=theme['list_bg'], fg=theme['list_fg'])
        self.deck_listbox.config(bg=theme['list_bg'], fg=theme['list_fg'])
        self.details_text.config(bg=theme['list_bg'], fg=theme['list_fg'])
        
        messagebox.showinfo("Theme Changed", f"Switched to {theme_name} theme")

def main():
    root = tk.Tk()
    app = YugiohDeckBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
