"""
Door Menu UI
Interface for choosing locations to visit
"""

import tkinter as tk
from typing import Dict, Callable, Optional
from datetime import datetime
from systems.door_locations import DoorSystem

class DoorMenuWindow:
    """UI for selecting locations to visit"""

    def __init__(self, game_data: Dict, on_location_selected: Optional[Callable] = None):
        self.game_data = game_data
        self.on_location_selected = on_location_selected
        self.door_system = DoorSystem(game_data)

        # Create window with larger size for all options
        self.window = tk.Toplevel()
        self.window.title("Choose Location to Visit")
        self.window.geometry("1200x800")  # Even larger window for better visibility
        self.window.configure(bg='#2b2b2b')

        # Prevent closing without proper cleanup
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.setup_ui()
        self.refresh_locations()

    def setup_ui(self):
        """Setup the door menu interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#1a1a1a', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🚪 Where would you like to go?",
            font=('Arial', 24, 'bold'),
            fg='#4CAF50',
            bg='#1a1a1a'
        ).pack(pady=20)

        # Current time display
        current_time = self.game_data.get('current_time', datetime.now())
        time_text = current_time.strftime("%A, %B %d, %Y - %I:%M %p")

        self.time_label = tk.Label(
            header_frame,
            text=f"Current Time: {time_text}",
            font=('Arial', 12),
            fg='#FFD700',
            bg='#1a1a1a'
        )
        self.time_label.pack()

        # Main container with scrollbar
        main_frame = tk.Frame(self.window, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Canvas and scrollbar for locations
        canvas = tk.Canvas(main_frame, bg='#2b2b2b', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Section headers
        self.create_section_header("Always Available", 0)
        self.always_row = 1

        self.create_section_header("Currently Open", 10)
        self.open_row = 11

        self.create_section_header("Closed Now", 20)
        self.closed_row = 21

        self.create_section_header("Special Locations", 30)
        self.special_row = 31

        # Bottom panel with close button
        bottom_frame = tk.Frame(self.window, bg='#1a1a1a', height=60)
        bottom_frame.pack(fill='x', side='bottom')
        bottom_frame.pack_propagate(False)

        tk.Button(
            bottom_frame,
            text="Cancel",
            font=('Arial', 14, 'bold'),
            bg='#F44336',
            fg='white',
            activebackground='#D32F2F',
            command=self.close_window,
            width=20
        ).pack(pady=15)

    def create_section_header(self, text: str, row: int):
        """Create a section header"""
        header = tk.Label(
            self.scrollable_frame,
            text=text,
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2b2b2b'
        )
        header.grid(row=row, column=0, columnspan=3, pady=(20, 10), sticky='w')

    def create_location_card(self, location_key: str, location_name: str,
                            description: str, row: int, col: int,
                            is_available: bool, reason: str = ""):
        """Create a card for a location"""
        # Card frame - larger size
        card_frame = tk.Frame(
            self.scrollable_frame,
            bg='#3a3a3a' if is_available else '#1a1a1a',
            relief='raised' if is_available else 'sunken',
            bd=3,
            width=350,
            height=200
        )
        card_frame.grid(row=row, column=col, padx=15, pady=10, sticky='nsew')
        card_frame.pack_propagate(False)

        # Configure grid to expand cards
        self.scrollable_frame.grid_columnconfigure(col, weight=1, minsize=350)

        # Location icon (different for each type)
        icons = {
            'conference': '🎤',
            'arcade': '🎮',
            'university': '🎓',
            'realtor': '🏢',
            'electronics': '💻',
            'gym': '💪',
            'library': '📚',
            'hacker': '💻',
            'bank': '🏦',
            'bar': '🍺',
            'grocery': '🛒',
            'online': '🌐',
            'dream': '💭',
            'making_game': '🎯'
        }

        icon = icons.get(location_key, '📍')

        # Location name with icon
        name_frame = tk.Frame(card_frame, bg=card_frame['bg'])
        name_frame.pack(fill='x', padx=15, pady=(15, 10))

        tk.Label(
            name_frame,
            text=icon,
            font=('Arial', 28),
            bg=card_frame['bg']
        ).pack(side='left', padx=(0, 15))

        tk.Label(
            name_frame,
            text=location_name,
            font=('Arial', 18, 'bold'),
            fg='white' if is_available else '#555555',
            bg=card_frame['bg']
        ).pack(side='left')

        # Description (only show for available locations)
        if is_available:
            tk.Label(
                card_frame,
                text=description,
                font=('Arial', 12),
                fg='#cccccc',
                bg=card_frame['bg'],
                wraplength=320,
                justify='left'
            ).pack(padx=15, pady=5)

        # Special indicator for 24/7
        if location_key == 'grocery':
            tk.Label(
                card_frame,
                text="✨ Always Open",
                font=('Arial', 11, 'bold'),
                fg='#4CAF50',
                bg=card_frame['bg']
            ).pack()

        # Visit button - make it look active or inactive
        button_frame = tk.Frame(card_frame, bg=card_frame['bg'])
        button_frame.pack(side='bottom', pady=15)

        if is_available:
            visit_btn = tk.Button(
                button_frame,
                text="ENTER",
                font=('Arial', 16, 'bold'),
                bg='#4CAF50',
                fg='white',
                activebackground='#5CBF60',
                activeforeground='white',
                relief='raised',
                bd=3,
                command=lambda: self.visit_location(location_key),
                width=20,
                height=2
            )
            visit_btn.pack()
        else:
            # Disabled button appearance
            disabled_btn = tk.Label(
                button_frame,
                text="CLOSED",
                font=('Arial', 16, 'bold'),
                bg='#2a2a2a',
                fg='#444444',
                relief='sunken',
                bd=2,
                width=20,
                height=2
            )
            disabled_btn.pack()

    def refresh_locations(self):
        """Refresh the available locations display"""
        current_date = self.game_data.get('current_time', datetime.now())

        # Get all locations and their availability
        all_locations = {
            'grocery': ('Grocery Store', '24/7 convenience store'),
            'conference': ('Conference', 'Industry events and meetups'),
            'arcade': ('Arcade', 'Retro games and talent scouting'),
            'university': ('University', 'Training and education'),
            'realtor': ('Realtor Office', 'Browse office spaces'),
            'electronics': ('Electronics Store', 'Hardware and upgrades'),
            'gym': ('Gym', 'Work out for health boost'),
            'library': ('Library', 'Quiet study and research'),
            'hacker': ('Hacker Meetup', 'Underground coding scene'),
            'bank': ('Bank', 'Loans and financial services'),
            'bar': ('Bar', 'Developer hangout spot'),
            'online': ('Online Forums', 'Digital connections'),
            'newspaper': ('Newspaper Ads', 'Help wanted section'),
            'headhunter': ('Headhunter', 'Professional recruitment')
        }

        # Categorize locations
        always_available = ['grocery']  # 24/7 stores
        currently_open = []
        currently_closed = []
        special_locations = ['online', 'newspaper', 'headhunter']

        for key, (name, desc) in all_locations.items():
            if key in always_available or key in special_locations:
                continue

            location = self.door_system.locations.get(key)
            if location:
                is_available, reason = location.is_available(current_date)
                if is_available:
                    currently_open.append((key, name, desc, True, ""))
                else:
                    currently_closed.append((key, name, desc, False, reason))

        # Display always available
        col = 0
        for key in always_available:
            name, desc = all_locations[key]
            self.create_location_card(key, name, desc, self.always_row, col, True)
            col += 1
            if col >= 3:
                col = 0
                self.always_row += 1

        # Display currently open
        col = 0
        for key, name, desc, available, reason in currently_open:
            self.create_location_card(key, name, desc, self.open_row, col, available, reason)
            col += 1
            if col >= 3:
                col = 0
                self.open_row += 1

        # Display currently closed
        col = 0
        for key, name, desc, available, reason in currently_closed:
            self.create_location_card(key, name, desc, self.closed_row, col, available, reason)
            col += 1
            if col >= 3:
                col = 0
                self.closed_row += 1

        # Display special locations
        col = 0
        for key in special_locations:
            if key in all_locations:
                name, desc = all_locations[key]
                location = self.door_system.locations.get(key)
                if location:
                    is_available, reason = location.is_available(current_date)
                    self.create_location_card(key, name, desc, self.special_row, col, is_available, reason)
                    col += 1
                    if col >= 3:
                        col = 0
                        self.special_row += 1

    def visit_location(self, location_key: str):
        """Handle visiting a location"""
        result = self.door_system.visit_location(location_key)

        if result['success']:
            # Special handling for grocery store
            if location_key == 'grocery':
                self.open_grocery_store()
            else:
                # Show result and close
                tk.messagebox.showinfo("Location Visit", result['message'])

                # Check for NPC encounter
                if 'npc_encountered' in result:
                    npc = self.door_system.npcs[result['npc_encountered']]
                    message = f"You met {npc['character']['name']}!"
                    if result.get('npc_permanently_unlocked'):
                        message += "\n\n⭐ Permanently unlocked for all future playthroughs!"
                    tk.messagebox.showinfo("NPC Encounter", message)

                self.close_window()
        else:
            tk.messagebox.showerror("Cannot Visit", result['message'])

    def open_grocery_store(self):
        """Open the grocery store window"""
        from desktop.grocery_store_ui import GroceryStoreWindow
        self.window.withdraw()  # Hide door menu

        def on_store_close():
            self.window.deiconify()  # Show door menu again

        GroceryStoreWindow(self.game_data, on_close=on_store_close)

    def close_window(self):
        """Close the door menu window"""
        self.window.destroy()
        if self.on_location_selected:
            self.on_location_selected()