import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from PIL import Image, ImageTk
import io
import json
import os
import threading
from datetime import datetime

class YugiohDeckBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Yu-Gi-Oh! Deck Builder - Ultimate Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c3e50")
        
        # Center the window
        self.center_window()
        
        # Initialize variables
        self.current_deck = []
        self.all_cards = []
        self.filtered_cards = []
        self.current_theme = "dark"
        self.card_images = {}
        self.is_loading = False
        
        # Setup theme colors
        self.setup_themes()
        
        # Create GUI
        self.create_menu()
        self.create_main_frame()
        self.create_header()
        self.create_card_list_frame()
        self.create_deck_frame()
        self.create_details_frame()
        self.create_status_bar()
        
        # Load initial data
        self.load_initial_cards()
        
        # Apply initial theme
        self.change_theme("dark")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_themes(self):
        self.themes = {
            "light": {
                "bg": "#ecf0f1",
                "fg": "#2c3e50",
                "button_bg": "#3498db",
                "button_fg": "#ffffff",
                "button_hover": "#2980b9",
                "list_bg": "#ffffff",
                "list_fg": "#2c3e50",
                "header_bg": "#3498db",
                "header_fg": "#ffffff",
                "highlight": "#e74c3c",
                "success": "#27ae60",
                "warning": "#f39c12",
                "border": "#bdc3c7"
            },
            "dark": {
                "bg": "#2c3e50",
                "fg": "#ecf0f1",
                "button_bg": "#34495e",
                "button_fg": "#ecf0f1",
                "button_hover": "#2c3e50",
                "list_bg": "#34495e",
                "list_fg": "#ecf0f1",
                "header_bg": "#1a252f",
                "header_fg": "#ecf0f1",
                "highlight": "#e74c3c",
                "success": "#27ae60",
                "warning": "#f39c12",
                "border": "#7f8c8d"
            }
        }
    
    def create_menu(self):
        menubar = tk.Menu(self.root, bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        file_menu.add_command(label="New Deck", command=self.new_deck, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Deck", command=self.open_deck, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Deck", command=self.save_deck, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Import Cards", command=self.import_cards)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        view_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        view_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_deck())
        self.root.bind('<Control-o>', lambda e: self.open_deck())
        self.root.bind('<Control-s>', lambda e: self.save_deck())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["header_bg"], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, text="YU-GI-OH! DECK BUILDER", 
                              font=("Arial", 18, "bold"), 
                              bg=self.themes[self.current_theme]["header_bg"],
                              fg=self.themes[self.current_theme]["header_fg"])
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Search frame
        search_frame = tk.Frame(header_frame, bg=self.themes[self.current_theme]["header_bg"])
        search_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", 
                bg=self.themes[self.current_theme]["header_bg"],
                fg=self.themes[self.current_theme]["header_fg"]).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, 
                                    font=("Arial", 10), bd=2, relief=tk.SOLID)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.filter_cards)
        self.search_entry.bind('<Return>', lambda e: self.search_cards())
        
        search_btn = tk.Button(search_frame, text="🔍 Search", command=self.search_cards,
                              bg=self.themes[self.current_theme]["button_bg"],
                              fg=self.themes[self.current_theme]["button_fg"],
                              font=("Arial", 10, "bold"),
                              bd=0, padx=15, pady=5,
                              cursor="hand2")
        search_btn.pack(side=tk.LEFT)
        
        # Add hover effect
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg=self.themes[self.current_theme]["button_hover"]))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg=self.themes[self.current_theme]["button_bg"]))
    
    def create_card_list_frame(self):
        # Left frame for card list
        left_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Header
        header = tk.Frame(left_frame, bg=self.themes[self.current_theme]["header_bg"], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="AVAILABLE CARDS", 
                font=("Arial", 12, "bold"),
                bg=self.themes[self.current_theme]["header_bg"],
                fg=self.themes[self.current_theme]["header_fg"]).pack(pady=10)
        
        # Card list with scrollbar
        list_frame = tk.Frame(left_frame, bg=self.themes[self.current_theme]["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.card_listbox = tk.Listbox(list_frame, height=20, 
                                      bg=self.themes[self.current_theme]["list_bg"],
                                      fg=self.themes[self.current_theme]["list_fg"],
                                      font=("Arial", 10),
                                      selectbackground=self.themes[self.current_theme]["highlight"],
                                      bd=2, relief=tk.SOLID)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.card_listbox.yview)
        self.card_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.card_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.card_listbox.bind('<<ListboxSelect>>', self.on_card_select)
        
        # Add to deck button
        add_btn = tk.Button(left_frame, text="➕ Add to Deck", command=self.add_to_deck,
                           bg=self.themes[self.current_theme]["success"],
                           fg="white",
                           font=("Arial", 10, "bold"),
                           bd=0, padx=20, pady=8,
                           cursor="hand2")
        add_btn.pack(pady=(10, 0))
        
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#219a52"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=self.themes[self.current_theme]["success"]))
    
    def create_deck_frame(self):
        # Middle frame for current deck
        middle_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["bg"])
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)
        
        # Header with deck count
        header = tk.Frame(middle_frame, bg=self.themes[self.current_theme]["header_bg"], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        self.deck_count_label = tk.Label(header, text="CURRENT DECK (0 cards)", 
                                        font=("Arial", 12, "bold"),
                                        bg=self.themes[self.current_theme]["header_bg"],
                                        fg=self.themes[self.current_theme]["header_fg"])
        self.deck_count_label.pack(pady=10)
        
        # Deck list with scrollbar
        deck_frame = tk.Frame(middle_frame, bg=self.themes[self.current_theme]["bg"])
        deck_frame.pack(fill=tk.BOTH, expand=True)
        
        self.deck_listbox = tk.Listbox(deck_frame, height=20,
                                      bg=self.themes[self.current_theme]["list_bg"],
                                      fg=self.themes[self.current_theme]["list_fg"],
                                      font=("Arial", 10),
                                      selectbackground=self.themes[self.current_theme]["highlight"],
                                      bd=2, relief=tk.SOLID)
        
        deck_scrollbar = ttk.Scrollbar(deck_frame, orient=tk.VERTICAL, command=self.deck_listbox.yview)
        self.deck_listbox.configure(yscrollcommand=deck_scrollbar.set)
        
        self.deck_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        deck_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deck_listbox.bind('<<ListboxSelect>>', self.on_deck_card_select)
        
        # Deck management buttons
        btn_frame = tk.Frame(middle_frame, bg=self.themes[self.current_theme]["bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        remove_btn = tk.Button(btn_frame, text="🗑️ Remove", command=self.remove_from_deck,
                              bg=self.themes[self.current_theme]["warning"],
                              fg="white",
                              font=("Arial", 10, "bold"),
                              bd=0, padx=15, pady=5,
                              cursor="hand2")
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(btn_frame, text="🧹 Clear All", command=self.clear_deck,
                             bg=self.themes[self.current_theme]["highlight"],
                             fg="white",
                             font=("Arial", 10, "bold"),
                             bd=0, padx=15, pady=5,
                             cursor="hand2")
        clear_btn.pack(side=tk.LEFT)
        
        # Hover effects
        remove_btn.bind("<Enter>", lambda e: remove_btn.config(bg="#e67e22"))
        remove_btn.bind("<Leave>", lambda e: remove_btn.config(bg=self.themes[self.current_theme]["warning"]))
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#c0392b"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=self.themes[self.current_theme]["highlight"]))
    
    def create_details_frame(self):
        # Right frame for card details
        right_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["bg"])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(right_frame, bg=self.themes[self.current_theme]["header_bg"], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="CARD DETAILS", 
                font=("Arial", 12, "bold"),
                bg=self.themes[self.current_theme]["header_bg"],
                fg=self.themes[self.current_theme]["header_fg"]).pack(pady=10)
        
        # Card image frame
        image_frame = tk.Frame(right_frame, bg=self.themes[self.current_theme]["bg"])
        image_frame.pack(pady=10)
        
        self.card_image_label = tk.Label(image_frame, text="Select a card to view details",
                                        bg=self.themes[self.current_theme]["bg"],
                                        fg=self.themes[self.current_theme]["fg"],
                                        font=("Arial", 10),
                                        width=30, height=15,
                                        relief=tk.SOLID, bd=2)
        self.card_image_label.pack()
        
        # Card details text
        details_frame = tk.Frame(right_frame, bg=self.themes[self.current_theme]["bg"])
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(details_frame, height=15, width=40, wrap=tk.WORD,
                                   bg=self.themes[self.current_theme]["list_bg"],
                                   fg=self.themes[self.current_theme]["list_fg"],
                                   font=("Arial", 10),
                                   bd=2, relief=tk.SOLID)
        
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Make details text read-only
        self.details_text.config(state=tk.DISABLED)
    
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             relief=tk.SUNKEN, anchor=tk.W,
                             bg=self.themes[self.current_theme]["header_bg"],
                             fg=self.themes[self.current_theme]["header_fg"])
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def fetch_card_data(self, card_name):
        self.update_status(f"Fetching data for {card_name}...")
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for card in data['data']:
                    if card['name'].lower() == card_name.lower():
                        self.update_status(f"Found {card_name}")
                        return card
                self.update_status(f"Card '{card_name}' not found")
                return None
            else:
                self.update_status(f"API Error: {response.status_code}")
                messagebox.showerror("Error", f"API Error: {response.status_code}")
                return None
        except Exception as e:
            self.update_status(f"Error fetching data: {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch card data: {str(e)}")
            return None
    
    def fetch_card_image(self, image_url):
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((250, 350), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            return None
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def load_initial_cards(self):
        self.update_status("Loading initial cards...")
        # Load more popular cards initially
        popular_cards = [
            "Dark Magician", "Blue-Eyes White Dragon", "Red-Eyes Black Dragon",
            "Exodia the Forbidden One", "Summoned Skull", "Celtic Guardian",
            "Dark Magician Girl", "Kuriboh", "Time Wizard", "Mystical Elf",
            "Gaia The Fierce Knight", "Buster Blader", "Jinzo", "Cyber Dragon",
            "Elemental HERO Neos", "Stardust Dragon", "Black Luster Soldier",
            "Obelisk the Tormentor", "Slifer the Sky Dragon", "The Winged Dragon of Ra",
            "Blue-Eyes Ultimate Dragon", "Magician of Black Chaos", "Dark Paladin", "Toon World",
            "Toon Summoned Skull", "Toon Mermaid", "Toon Blue-Eyes White Dragon", "Toon Dark Magician Girl",
            "Obnoxious Celtic Guard", "Breaker the Magical Warrior", "Sangan", "Man-Eater Bug",
            "Trap Hole", "Mirror Force", "Monster Reborn", "Pot of Greed",
            "Polymerization", "Change of Heart", "Swords of Revealing Light", "Raigeki"
        ]
        
        for card_name in popular_cards:
            card_data = self.fetch_card_data(card_name)
            if card_data:
                self.all_cards.append(card_data)
                self.card_listbox.insert(tk.END, card_data['name'])
        
        self.filtered_cards = self.all_cards.copy()
        self.update_status(f"Loaded {len(self.all_cards)} cards")
    
    def search_cards(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            self.update_status("Please enter a search term")
            return
        
        self.update_status(f"Searching for '{search_term}'...")
        card_data = self.fetch_card_data(search_term)
        if card_data:
            # Clear current list and add the found card
            self.card_listbox.delete(0, tk.END)
            self.filtered_cards = [card_data]
            self.card_listbox.insert(tk.END, card_data['name'])
            self.update_status(f"Found: {card_data['name']}")
        else:
            messagebox.showinfo("Not Found", f"Card '{search_term}' not found.")
            self.update_status(f"Card '{search_term}' not found")
    
    def filter_cards(self, event):
        search_term = self.search_var.get().lower()
        self.card_listbox.delete(0, tk.END)
        
        if not search_term:
            # Show all cards if search is empty
            for card in self.all_cards:
                self.card_listbox.insert(tk.END, card['name'])
            self.filtered_cards = self.all_cards.copy()
            return
        
        filtered = []
        for card in self.all_cards:
            if search_term in card['name'].lower():
                self.card_listbox.insert(tk.END, card['name'])
                filtered.append(card)
        
        self.filtered_cards = filtered
        self.update_status(f"Found {len(filtered)} matching cards")
    
    def on_card_select(self, event):
        selection = self.card_listbox.curselection()
        if not selection:
            return
        
        card_name = self.card_listbox.get(selection[0])
        card_data = next((card for card in self.filtered_cards if card['name'] == card_name), None)
        
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
        
        # Display card information with better formatting
        details = f"🏷️  Name: {card_data['name']}\n\n"
        details += f"📋 Type: {card_data['type']}\n"
        details += f"🏆 Race: {card_data.get('race', 'N/A')}\n"
        details += f"✨ Attribute: {card_data.get('attribute', 'N/A')}\n"
        
        if 'atk' in card_data:
            details += f"⚔️  ATK: {card_data['atk']}\n"
        if 'def' in card_data:
            details += f"🛡️  DEF: {card_data['def']}\n"
        if 'level' in card_data:
            details += f"⭐ Level: {card_data['level']}\n"
        
        details += f"\n📖 Description:\n{card_data['desc']}"
        
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        
        # Load and display card image
        if 'card_images' in card_data and card_data['card_images']:
            image_url = card_data['card_images'][0]['image_url']
            self.update_status("Loading image...")
            
            # Load image in background to prevent UI freezing
            def load_image():
                photo = self.fetch_card_image(image_url)
                if photo:
                    self.card_image_label.config(image=photo)
                    self.card_image_label.image = photo
                    self.update_status("Image loaded")
                else:
                    self.card_image_label.config(text="Image not available")
                    self.update_status("Image load failed")
            
            threading.Thread(target=load_image, daemon=True).start()
        else:
            self.card_image_label.config(text="Image not available")
    
    def add_to_deck(self):
        selection = self.card_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a card to add to your deck.")
            return
        
        card_name = self.card_listbox.get(selection[0])
        card_data = next((card for card in self.filtered_cards if card['name'] == card_name), None)
        
        if card_data:
            # Check if card already in deck
            if any(card['name'] == card_name for card in self.current_deck):
                messagebox.showwarning("Warning", f"{card_name} is already in your deck!")
                return
                
            self.current_deck.append(card_data)
            self.deck_listbox.insert(tk.END, card_data['name'])
            self.update_deck_count()
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
        self.update_deck_count()
        self.update_status(f"Removed {card_name} from deck")
    
    def clear_deck(self):
        if not self.current_deck:
            messagebox.showinfo("Info", "Your deck is already empty.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear your entire deck?"):
            self.current_deck.clear()
            self.deck_listbox.delete(0, tk.END)
            self.update_deck_count()
            self.update_status("Deck cleared")
    
    def update_deck_count(self):
        count = len(self.current_deck)
        self.deck_count_label.config(text=f"CURRENT DECK ({count} cards)")
    
    def new_deck(self):
        if self.current_deck and not messagebox.askyesno("Confirm", "Create new deck? Current deck will be lost."):
            return
        
        self.current_deck.clear()
        self.deck_listbox.delete(0, tk.END)
        self.update_deck_count()
        self.update_status("Created new empty deck")
        messagebox.showinfo("New Deck", "Created a new empty deck.")
    
    def save_deck(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Your deck is empty. Nothing to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Deck"
        )
        
        if file_path:
            try:
                # Save only essential card data
                deck_data = []
                for card in self.current_deck:
                    deck_data.append({
                        'id': card['id'],
                        'name': card['name'],
                        'type': card['type'],
                        'atk': card.get('atk', 0),
                        'def': card.get('def', 0)
                    })
                
                with open(file_path, 'w') as f:
                    json.dump(deck_data, f, indent=2)
                
                self.update_status(f"Deck saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Deck saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save deck: {str(e)}")
                self.update_status("Save failed")
    
    def open_deck(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open Deck"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    deck_data = json.load(f)
                
                self.current_deck.clear()
                self.deck_listbox.delete(0, tk.END)
                
                self.update_status("Loading deck...")
                loaded_count = 0
                
                for card_info in deck_data:
                    # Fetch full card data for each card in the deck
                    card_data = self.fetch_card_data(card_info['name'])
                    if card_data:
                        self.current_deck.append(card_data)
                        self.deck_listbox.insert(tk.END, card_data['name'])
                        loaded_count += 1
                
                self.update_deck_count()
                self.update_status(f"Loaded {loaded_count} cards from deck")
                messagebox.showinfo("Success", f"Deck loaded successfully! ({loaded_count} cards)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load deck: {str(e)}")
                self.update_status("Load failed")
    
    def import_cards(self):
        """Import additional cards from a text file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Import Cards"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    card_names = [line.strip() for line in f if line.strip()]
                
                self.update_status(f"Importing {len(card_names)} cards...")
                imported_count = 0
                
                for card_name in card_names:
                    if not any(card['name'].lower() == card_name.lower() for card in self.all_cards):
                        card_data = self.fetch_card_data(card_name)
                        if card_data:
                            self.all_cards.append(card_data)
                            self.card_listbox.insert(tk.END, card_data['name'])
                            imported_count += 1
                
                self.update_status(f"Imported {imported_count} new cards")
                messagebox.showinfo("Success", f"Imported {imported_count} new cards!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import cards: {str(e)}")
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Update all widgets with new theme colors
        widgets = [
            self.root, self.main_frame, self.card_listbox, self.deck_listbox,
            self.details_text, self.card_image_label
        ]
        
        for widget in widgets:
            try:
                widget.config(bg=theme['bg'])
                if hasattr(widget, 'config') and 'fg' in widget.config():
                    widget.config(fg=theme['fg'])
            except:
                pass
        
        # Update specific widgets
        self.card_listbox.config(bg=theme['list_bg'], fg=theme['list_fg'], 
                               selectbackground=theme['highlight'])
        self.deck_listbox.config(bg=theme['list_bg'], fg=theme['list_fg'],
                               selectbackground=theme['highlight'])
        self.details_text.config(bg=theme['list_bg'], fg=theme['list_fg'])
        
        self.update_status(f"Switched to {theme_name} theme")
    
    def show_about(self):
        about_text = """Yu-Gi-Oh! Deck Builder - Ultimate Edition

Version: 2.0
Developed with Python and Tkinter

Features:
- Search and browse Yu-Gi-Oh! cards
- Build and manage your deck
- Save/Load deck configurations
- Light/Dark theme support
- High-quality card images

Data provided by YGOPRODeck API"""
        
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    app = YugiohDeckBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
