"""
Game Engine Interface - Create games with OpenEngine
"""

import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar
from systems.unlock_system import UnlockSystem
from games.game_database import GameDatabase
import os
from dotenv import load_dotenv
from deepseek.services.naming import DeepSeekNamingService


class GameEngineWindow:
    """Game creation interface for OpenEngine"""

    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        self.unlock_system = UnlockSystem(game_data)
        self.game_db = GameDatabase()

        # Load API key
        load_dotenv()
        api_key = os.getenv('DEEPSEEK_API_KEY')
        self.naming_service = DeepSeekNamingService(api_key) if api_key else None

        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("OpenEngine - Game Development")
        self.window.geometry("1400x900")
        self.window.configure(bg='#0a0a0f')

        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()

        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 700
        y = (self.window.winfo_screenheight() // 2) - 450
        self.window.geometry(f"1400x900+{x}+{y}")

        self.selected_topic = None
        self.selected_type = None
        self.generated_names = []  # Store generated names
        self.current_name_index = 0  # Track which name we're showing
        self.preloaded_adventure_data = None  # Store preloaded adventure data
        self.preload_thread = None  # Track preload thread

        self.setup_ui()

    def setup_ui(self):
        """Setup the game engine interface"""
        # Title bar
        title_frame = tk.Frame(self.window, bg='#1a1a2e', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="OPENENGINE",
                font=('Consolas', 28, 'bold'), bg='#1a1a2e', fg='#00ff88').pack(side='left', padx=20, pady=10)

        tk.Label(title_frame, text="Free Game Engine",
                font=('Arial', 12), bg='#1a1a2e', fg='#888888').pack(side='left', padx=10, pady=20)

        # Close button
        close_btn = tk.Button(title_frame, text="✕", command=self.window.destroy,
                            bg='#ff4444', fg='white', font=('Arial', 14, 'bold'),
                            padx=15, cursor='hand2', bd=0)
        close_btn.pack(side='right', padx=20)

        # Main container
        main_frame = tk.Frame(self.window, bg='#0a0a0f')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Left panel - Topics
        left_panel = tk.Frame(main_frame, bg='#1a1a2e', width=400)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="SELECT TOPIC",
                font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#4a9eff').pack(pady=10)

        # Topics listbox with scrollbar
        topic_frame = tk.Frame(left_panel, bg='#1a1a2e')
        topic_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        topic_scrollbar = Scrollbar(topic_frame)
        topic_scrollbar.pack(side='right', fill='y')

        self.topic_listbox = Listbox(topic_frame, bg='#0a0a0f', fg='#00ff00',
                                     selectbackground='#2a4a3a', selectforeground='#00ff88',
                                     font=('Consolas', 11), height=20,
                                     yscrollcommand=topic_scrollbar.set)
        self.topic_listbox.pack(side='left', fill='both', expand=True)
        topic_scrollbar.config(command=self.topic_listbox.yview)

        # Populate topics
        topics = self.unlock_system.get_all_unlocked_topics()
        for topic in topics:
            self.topic_listbox.insert(tk.END, topic)

        self.topic_listbox.bind('<<ListboxSelect>>', self.on_topic_select)

        # Middle panel - Game Types
        middle_panel = tk.Frame(main_frame, bg='#1a1a2e', width=400)
        middle_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        middle_panel.pack_propagate(False)

        tk.Label(middle_panel, text="SELECT GAME TYPE",
                font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#4a9eff').pack(pady=10)

        # Game types listbox with scrollbar
        type_frame = tk.Frame(middle_panel, bg='#1a1a2e')
        type_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        type_scrollbar = Scrollbar(type_frame)
        type_scrollbar.pack(side='right', fill='y')

        self.type_listbox = Listbox(type_frame, bg='#0a0a0f', fg='#00ff00',
                                    selectbackground='#2a4a3a', selectforeground='#00ff88',
                                    font=('Consolas', 11), height=20,
                                    yscrollcommand=type_scrollbar.set)
        self.type_listbox.pack(side='left', fill='both', expand=True)
        type_scrollbar.config(command=self.type_listbox.yview)

        # Populate game types
        game_types = self.unlock_system.get_all_unlocked_game_types()
        for gtype in game_types:
            self.type_listbox.insert(tk.END, gtype)

        self.type_listbox.bind('<<ListboxSelect>>', self.on_type_select)

        # Right panel - Game Details & Actions
        right_panel = tk.Frame(main_frame, bg='#1a1a2e', width=400)
        right_panel.pack(side='right', fill='both', expand=True)
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="GAME DETAILS",
                font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#4a9eff').pack(pady=10)

        # Game name entry
        name_frame = tk.Frame(right_panel, bg='#1a1a2e')
        name_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(name_frame, text="Game Name:",
                font=('Arial', 11), bg='#1a1a2e', fg='white').pack(anchor='w')

        # Name entry with button frame
        entry_button_frame = tk.Frame(name_frame, bg='#1a1a2e')
        entry_button_frame.pack(fill='x', pady=5)

        self.name_entry = tk.Entry(entry_button_frame, bg='#0a0a0f', fg='#00ff00',
                                   font=('Consolas', 14, 'bold'), insertbackground='#00ff00',
                                   width=30)
        self.name_entry.pack(side='left', fill='x', expand=True, ipady=5)

        # Save button
        self.save_btn = tk.Button(entry_button_frame, text="💾 Save",
                                 command=self.save_name_for_later,
                                 bg='#5a5a6e', fg='white', font=('Arial', 10),
                                 padx=10, cursor='hand2', state='disabled')
        self.save_btn.pack(side='right', padx=(5, 0))

        # Randomize button
        self.randomize_btn = tk.Button(entry_button_frame, text="🎲 Randomize",
                                      command=self.randomize_name,
                                      bg='#4a4a5e', fg='white', font=('Arial', 10),
                                      padx=10, cursor='hand2', state='disabled')
        self.randomize_btn.pack(side='right', padx=(5, 0))

        # Selection display
        self.selection_frame = tk.Frame(right_panel, bg='#2a2a3e', relief='ridge', bd=1)
        self.selection_frame.pack(fill='x', padx=20, pady=20)

        self.selection_label = tk.Label(self.selection_frame,
                text="No selection",
                font=('Consolas', 11), bg='#2a2a3e', fg='#888888',
                justify='left', anchor='w')
        self.selection_label.pack(padx=10, pady=10)

        # Engine info
        engine_frame = tk.Frame(right_panel, bg='#0a0a0f')
        engine_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(engine_frame, text="Engine: OpenEngine (Free)",
                font=('Arial', 10), bg='#0a0a0f', fg='#666666').pack()
        tk.Label(engine_frame, text="Version: 1.0.0",
                font=('Arial', 10), bg='#0a0a0f', fg='#666666').pack()

        # Development time estimate
        self.time_label = tk.Label(right_panel,
                text="Development Time: -- days",
                font=('Arial', 11), bg='#1a1a2e', fg='#ffaa00')
        self.time_label.pack(pady=10)

        # Create button
        self.create_btn = tk.Button(right_panel, text="GO TO PLANNING",
                                   command=self.go_to_planning,
                                   bg='#00aa44', fg='white', font=('Arial', 12, 'bold'),
                                   padx=30, pady=10, cursor='hand2',
                                   state='disabled')
        self.create_btn.pack(pady=20)

        # Status bar
        status_frame = tk.Frame(self.window, bg='#0a0a0f', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(status_frame, text="Select a topic and game type to begin",
                                     font=('Arial', 10), bg='#0a0a0f', fg='#666666')
        self.status_label.pack(side='left', padx=10)

    def on_topic_select(self, event):
        """Handle topic selection"""
        selection = self.topic_listbox.curselection()
        if selection:
            self.selected_topic = self.topic_listbox.get(selection[0])
            self.update_selection_display()

    def on_type_select(self, event):
        """Handle game type selection"""
        selection = self.type_listbox.curselection()
        if selection:
            self.selected_type = self.type_listbox.get(selection[0])
            self.update_selection_display()

    def update_selection_display(self):
        """Update the selection display and enable/disable create button"""
        if self.selected_topic and self.selected_type:
            self.selection_label.config(
                text=f"Topic: {self.selected_topic}\nType: {self.selected_type}",
                fg='#00ff00'
            )
            self.create_btn.config(state='normal')
            self.randomize_btn.config(state='normal')
            self.save_btn.config(state='normal')

            # Set default name
            default_name = f"{self.selected_topic} {self.selected_type} GAME!!"
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, default_name)

            # Reset generated names when topic/type changes
            self.generated_names = [default_name]
            self.current_name_index = 0

            # If Text Adventure is selected, start preloading the adventure data
            if self.selected_type == 'Text Adventure':
                self.preload_text_adventure()

            # Estimate development time (simplified)
            base_days = 30
            if self.selected_type in ['Online']:
                base_days = 120
            elif self.selected_type in ['RPG', 'Strategy', 'Simulation']:
                base_days = 90
            elif self.selected_type in ['Arcade', 'Puzzle', 'Text Adventure']:
                base_days = 14

            self.time_label.config(text=f"Development Time: ~{base_days} days")
            self.status_label.config(text="Ready to create game!")
        else:
            text_parts = []
            if self.selected_topic:
                text_parts.append(f"Topic: {self.selected_topic}")
            if self.selected_type:
                text_parts.append(f"Type: {self.selected_type}")

            if text_parts:
                self.selection_label.config(text="\n".join(text_parts), fg='#ffaa00')
            else:
                self.selection_label.config(text="No selection", fg='#888888')

            self.create_btn.config(state='disabled')
            self.randomize_btn.config(state='disabled')
            self.save_btn.config(state='disabled')
            self.generated_names = []  # Clear generated names
            self.current_name_index = 0

    def preload_text_adventure(self):
        """Start preloading text adventure data in background"""
        import threading
        import sys
        import os

        # Cancel any existing preload thread
        if self.preload_thread and self.preload_thread.is_alive():
            return  # Already preloading

        def preload_worker():
            """Worker thread to preload adventure data"""
            try:
                import json
                print(f"[PRELOAD] Starting background API request for Text Adventure - {self.selected_topic}")

                # Add deepseek path to imports
                sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'deepseek'))
                from deepseek_client import DeepSeekClient

                client = DeepSeekClient()

                # First try a simple test request for a boon
                print(f"[PRELOAD] Testing API with simple boon request for {self.selected_topic}")
                boon = client.test_boon_request(self.selected_topic)
                if boon:
                    print(f"[PRELOAD] API test successful! Boon: {boon}")
                    print(f"[PRELOAD] Now using incremental generation...")
                else:
                    print(f"[PRELOAD] API test failed, but continuing...")

                # Use incremental generation for faster results
                self.preloaded_adventure_data = client.generate_adventure_incremental(self.selected_topic)

                if self.preloaded_adventure_data:
                    print(f"[PRELOAD] Successfully preloaded adventure data for {self.selected_topic}")

                    # Save to cache file for DeepAdventure to find
                    cache_file = f"/tmp/adventure_cache_{self.selected_topic.replace(' ', '_')}.json"
                    try:
                        with open(cache_file, 'w') as f:
                            json.dump(self.preloaded_adventure_data, f)
                        print(f"[PRELOAD] Saved to cache: {cache_file}")
                    except Exception as cache_error:
                        print(f"[PRELOAD] Failed to save cache: {cache_error}")
                else:
                    print(f"[PRELOAD] Failed to preload adventure data for {self.selected_topic}")

            except Exception as e:
                print(f"[PRELOAD] Error during preload: {e}")
                import traceback
                traceback.print_exc()
                self.preloaded_adventure_data = None

        # Start the preload thread
        self.preload_thread = threading.Thread(target=preload_worker)
        self.preload_thread.daemon = True
        self.preload_thread.start()

        # Update status to show preloading
        if self.status_label:
            self.status_label.config(text="Ready to create game! (Preloading adventure data...)")

    def go_to_planning(self):
        """Start multi-stage development process"""
        game_name = self.name_entry.get().strip()

        if not game_name:
            messagebox.showwarning("Missing Name", "Please enter a game name!")
            return

        if not self.selected_topic or not self.selected_type:
            messagebox.showwarning("Incomplete Selection", "Please select both a topic and game type!")
            return

        # Import here to avoid circular imports
        from desktop.development_stages import MultiStageDevelopment

        # Close this window
        self.window.destroy()

        # Start multi-stage development with preloaded data
        multi_stage = MultiStageDevelopment(
            self.parent,
            self.game_data,
            game_name,
            self.selected_type,
            self.selected_topic,
            preloaded_adventure_data=self.preloaded_adventure_data if self.selected_type == 'Text Adventure' else None
        )

    def open_developer_selection(self, game_name):
        """Open developer selection window for planning phase"""
        dev_window = tk.Toplevel(self.window)
        dev_window.title("Select Lead Developer for Planning")
        dev_window.geometry("600x500")
        dev_window.configure(bg='#1a1a2e')
        dev_window.transient(self.window)
        dev_window.grab_set()

        # Center the window
        dev_window.update_idletasks()
        x = (dev_window.winfo_screenwidth() // 2) - 300
        y = (dev_window.winfo_screenheight() // 2) - 250
        dev_window.geometry(f"600x500+{x}+{y}")

        # Title
        title_label = tk.Label(dev_window, text="SELECT LEAD DEVELOPER",
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)

        # Game info
        info_label = tk.Label(dev_window,
                             text=f"Game: {game_name}\nTopic: {self.selected_topic} | Type: {self.selected_type}",
                             font=('Arial', 11), bg='#1a1a2e', fg='#aaaaaa')
        info_label.pack(pady=10)

        # Developer list frame
        list_frame = tk.Frame(dev_window, bg='#1a1a2e')
        list_frame.pack(fill='both', expand=True, padx=30, pady=10)

        tk.Label(list_frame, text="Available Developers:",
                font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='white').pack(anchor='w', pady=5)

        # Listbox for developers
        dev_listbox = tk.Listbox(list_frame, bg='#2a2a3e', fg='white',
                                font=('Arial', 11), selectmode='single',
                                activestyle='none', highlightthickness=0)
        dev_listbox.pack(fill='both', expand=True)

        # Add player as the only option for now
        dev_listbox.insert(tk.END, "You (Player)")

        # Add placeholder for future NPCs
        dev_listbox.insert(tk.END, "[No employees hired yet]")

        # Buttons frame
        button_frame = tk.Frame(dev_window, bg='#1a1a2e')
        button_frame.pack(pady=20)

        # View Contacts button
        contacts_btn = tk.Button(button_frame, text="View Contacts",
                               command=lambda: self.open_contacts_window(),
                               bg='#4a4a6e', fg='white', font=('Arial', 11),
                               padx=15, pady=5)
        contacts_btn.pack(side='left', padx=10)

        # Select button
        select_btn = tk.Button(button_frame, text="Select Developer",
                             command=lambda: self.select_developer(dev_window, dev_listbox, game_name),
                             bg='#00aa44', fg='white', font=('Arial', 11, 'bold'),
                             padx=15, pady=5)
        select_btn.pack(side='left', padx=10)

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel",
                             command=dev_window.destroy,
                             bg='#aa0044', fg='white', font=('Arial', 11),
                             padx=15, pady=5)
        cancel_btn.pack(side='left', padx=10)

    def select_developer(self, dev_window, dev_listbox, game_name):
        """Handle developer selection"""
        selection = dev_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a developer!")
            return

        selected_dev = dev_listbox.get(selection[0])

        if selected_dev == "[No employees hired yet]":
            messagebox.showinfo("No Employees", "You need to hire employees first!\nFor now, you'll lead the planning.")
            selected_dev = "You (Player)"

        # Close developer selection window
        dev_window.destroy()

        # Proceed with game creation
        self.create_game_with_developer(game_name, selected_dev)

    def create_game_with_developer(self, game_name, developer):
        """Create the game with selected developer as lead"""
        # Show development window
        self.show_development_window(game_name, developer)

    def show_development_window(self, game_name, developer):
        """Show the game development progress window"""
        from systems.game_development import GameDevelopment, GameRating

        dev_window = tk.Toplevel(self.window)
        dev_window.title("Game Development")
        dev_window.geometry("700x600")
        dev_window.configure(bg='#1a1a2e')
        dev_window.transient(self.window)
        dev_window.grab_set()

        # Center the window
        dev_window.update_idletasks()
        x = (dev_window.winfo_screenwidth() // 2) - 350
        y = (dev_window.winfo_screenheight() // 2) - 300
        dev_window.geometry(f"700x600+{x}+{y}")

        # Title
        title_label = tk.Label(dev_window, text="GAME DEVELOPMENT",
                              font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)

        # Game info
        info_label = tk.Label(dev_window,
                             text=f"Game: {game_name}\nTopic: {self.selected_topic} | Type: {self.selected_type}\nLead Developer: {developer}",
                             font=('Arial', 11), bg='#1a1a2e', fg='#aaaaaa')
        info_label.pack(pady=10)

        # Progress label
        progress_label = tk.Label(dev_window, text="Development in progress...",
                                font=('Arial', 12), bg='#1a1a2e', fg='#ffaa00')
        progress_label.pack(pady=10)

        # Start button
        start_btn = tk.Button(dev_window, text="START DEVELOPMENT",
                            command=lambda: self.start_development(dev_window, game_name, developer),
                            bg='#00aa44', fg='white', font=('Arial', 14, 'bold'),
                            padx=30, pady=10, cursor='hand2')
        start_btn.pack(pady=30)

    def start_development(self, dev_window, game_name, developer):
        """Start the development process and show results"""
        from systems.game_development import GameDevelopment

        # Clear the window
        for widget in dev_window.winfo_children():
            widget.destroy()

        # Title
        title_label = tk.Label(dev_window, text="DEVELOPMENT RESULTS",
                              font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)

        # Game name
        name_label = tk.Label(dev_window, text=game_name,
                             font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='#00ff00')
        name_label.pack(pady=5)

        # Initialize development system
        dev_system = GameDevelopment(self.game_data)

        # Develop the game and get scores
        score = dev_system.develop_game(game_name, self.selected_type, self.selected_topic,
                                       developer, "OpenEngine")

        # Get rating
        rating = dev_system.get_game_rating(score)
        rating_desc = dev_system.get_rating_description(rating)

        # Create scores frame
        scores_frame = tk.Frame(dev_window, bg='#2a2a3e', relief='ridge', bd=2)
        scores_frame.pack(pady=20, padx=50, fill='both', expand=True)

        # Category scores
        categories = [
            ("Gameplay", score.gameplay),
            ("Technical", score.technical),
            ("Graphics", score.graphics),
            ("Innovation", score.innovation),
            ("Sound/Audio", score.sound_audio),
            ("Story", score.story)
        ]

        tk.Label(scores_frame, text="CATEGORY SCORES", font=('Arial', 14, 'bold'),
                bg='#2a2a3e', fg='white').pack(pady=10)

        for category, value in categories:
            cat_frame = tk.Frame(scores_frame, bg='#2a2a3e')
            cat_frame.pack(fill='x', padx=30, pady=5)

            # Category name
            tk.Label(cat_frame, text=f"{category}:", font=('Arial', 12),
                    bg='#2a2a3e', fg='white', width=15, anchor='w').pack(side='left')

            # Score value with color coding
            if value >= 30:
                color = '#00ff00'  # Green for excellent
            elif value >= 20:
                color = '#ffff00'  # Yellow for good
            elif value >= 10:
                color = '#ffaa00'  # Orange for okay
            else:
                color = '#ff4444'  # Red for poor

            tk.Label(cat_frame, text=f"+{value}", font=('Arial', 12, 'bold'),
                    bg='#2a2a3e', fg=color, width=10).pack(side='left')

            # Progress bar
            bar_frame = tk.Frame(cat_frame, bg='#1a1a2e', height=20, width=200)
            bar_frame.pack(side='left', padx=10)
            bar_frame.pack_propagate(False)

            bar_fill = tk.Frame(bar_frame, bg=color, height=20, width=int(value * 4))  # Max 50 * 4 = 200
            bar_fill.pack(side='left')

        # Separator
        tk.Frame(scores_frame, bg='#4a4a5a', height=2).pack(fill='x', pady=15, padx=30)

        # Total score
        total_frame = tk.Frame(scores_frame, bg='#2a2a3e')
        total_frame.pack(pady=10)

        tk.Label(total_frame, text="TOTAL SCORE:", font=('Arial', 14, 'bold'),
                bg='#2a2a3e', fg='white').pack(side='left', padx=10)

        total_color = '#00ff00' if score.total >= 180 else '#ffff00' if score.total >= 120 else '#ffaa00' if score.total >= 90 else '#ff4444'
        tk.Label(total_frame, text=str(score.total), font=('Arial', 16, 'bold'),
                bg='#2a2a3e', fg=total_color).pack(side='left')

        # Rating
        rating_frame = tk.Frame(dev_window, bg='#3a3a4e', relief='ridge', bd=2)
        rating_frame.pack(pady=10, padx=50, fill='x')

        # Rating color based on tier
        rating_colors = {
            'Masterpiece': '#ff00ff',  # Magenta
            'Legendary': '#ffff00',    # Yellow
            'Outstanding': '#00ffff',   # Cyan
            'Excellent': '#00ff00',     # Green
            'Notable': '#88ff88',       # Light green
            'Good': '#aaffaa',          # Pale green
            'Fun': '#ffaa00',           # Orange
            'Decent': '#ff8800',        # Dark orange
            'Meh...': '#ff4444',        # Red
            'Poor': '#aa0000'           # Dark red
        }

        rating_color = rating_colors.get(rating.value, '#ffffff')

        tk.Label(rating_frame, text="RATING", font=('Arial', 12),
                bg='#3a3a4e', fg='white').pack(pady=5)
        tk.Label(rating_frame, text=rating.value, font=('Arial', 18, 'bold'),
                bg='#3a3a4e', fg=rating_color).pack(pady=5)
        tk.Label(rating_frame, text=rating_desc, font=('Arial', 10, 'italic'),
                bg='#3a3a4e', fg='#aaaaaa', wraplength=500).pack(pady=5, padx=20)

        # Save game to database
        result = self.game_db.create_game(game_name, self.selected_topic, self.selected_type, "OpenEngine")

        # Also save the scores
        if 'game_history' not in self.game_data.data:
            self.game_data.data['game_history'] = []

        game_record = {
            'name': game_name,
            'topic': self.selected_topic,
            'type': self.selected_type,
            'developer': developer,
            'scores': score.to_dict(),
            'rating': rating.value,
            'date': self.game_data.data.get('game_time', {}).get('current_date', 'Unknown')
        }
        self.game_data.data['game_history'].append(game_record)

        # Check for unlocks
        unlocks = self.unlock_system.check_game_creation_unlocks(game_name, self.selected_topic, self.selected_type)

        if unlocks:
            unlock_msg = "New unlocks!\n"
            for unlock_type, unlock_name, unlock_desc in unlocks:
                unlock_msg += f"\n{unlock_type.title()}: {unlock_name}\n{unlock_desc}"
            messagebox.showinfo("Unlocks!", unlock_msg)

        # Continue button
        continue_btn = tk.Button(dev_window, text="CONTINUE",
                               command=lambda: self.finish_development(dev_window),
                               bg='#4a4a6e', fg='white', font=('Arial', 12),
                               padx=20, pady=5)
        continue_btn.pack(pady=20)

    def finish_development(self, dev_window):
        """Finish development and close windows"""
        # Close development window
        dev_window.destroy()

        # Clear selections
        self.selected_topic = None
        self.selected_type = None
        self.name_entry.delete(0, tk.END)
        self.topic_listbox.selection_clear(0, tk.END)
        self.type_listbox.selection_clear(0, tk.END)
        self.update_selection_display()

        # Close main window
        self.window.destroy()

    def open_contacts_window(self):
        """Open contacts window to view available contacts"""
        contacts_window = tk.Toplevel(self.window)
        contacts_window.title("Contacts")
        contacts_window.geometry("500x600")
        contacts_window.configure(bg='#1a1a2e')

        # Center the window
        contacts_window.update_idletasks()
        x = (contacts_window.winfo_screenwidth() // 2) - 250
        y = (contacts_window.winfo_screenheight() // 2) - 300
        contacts_window.geometry(f"500x600+{x}+{y}")

        # Title
        title_label = tk.Label(contacts_window, text="CONTACTS",
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)

        # Notebook for categories
        notebook = ttk.Notebook(contacts_window)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)

        # Developers tab
        dev_frame = tk.Frame(notebook, bg='#2a2a3e')
        notebook.add(dev_frame, text="Developers")

        dev_list = tk.Listbox(dev_frame, bg='#2a2a3e', fg='white',
                             font=('Arial', 11), selectmode='single')
        dev_list.pack(fill='both', expand=True, padx=10, pady=10)
        dev_list.insert(tk.END, "No developer contacts yet")

        # Artists tab
        art_frame = tk.Frame(notebook, bg='#2a2a3e')
        notebook.add(art_frame, text="Artists")

        art_list = tk.Listbox(art_frame, bg='#2a2a3e', fg='white',
                             font=('Arial', 11), selectmode='single')
        art_list.pack(fill='both', expand=True, padx=10, pady=10)
        art_list.insert(tk.END, "No artist contacts yet")

        # Designers tab
        design_frame = tk.Frame(notebook, bg='#2a2a3e')
        notebook.add(design_frame, text="Designers")

        design_list = tk.Listbox(design_frame, bg='#2a2a3e', fg='white',
                                font=('Arial', 11), selectmode='single')
        design_list.pack(fill='both', expand=True, padx=10, pady=10)
        design_list.insert(tk.END, "No designer contacts yet")

        # Publishers tab
        pub_frame = tk.Frame(notebook, bg='#2a2a3e')
        notebook.add(pub_frame, text="Publishers")

        pub_list = tk.Listbox(pub_frame, bg='#2a2a3e', fg='white',
                             font=('Arial', 11), selectmode='single')
        pub_list.pack(fill='both', expand=True, padx=10, pady=10)
        pub_list.insert(tk.END, "No publisher contacts yet")

        # Close button
        close_btn = tk.Button(contacts_window, text="Close",
                            command=contacts_window.destroy,
                            bg='#4a4a6e', fg='white', font=('Arial', 11),
                            padx=20, pady=5)
        close_btn.pack(pady=20)

    def create_game(self):
        """Create the game with selected options"""
        game_name = self.name_entry.get().strip()

        if not game_name:
            messagebox.showwarning("Missing Name", "Please enter a game name!")
            return

        if not self.selected_topic or not self.selected_type:
            messagebox.showwarning("Incomplete Selection", "Please select both a topic and game type!")
            return

        # Create the game
        result = self.game_db.create_game(game_name, self.selected_topic, self.selected_type, "OpenEngine")

        # Check for unlocks
        unlocks = self.unlock_system.check_game_creation_unlocks(game_name, self.selected_topic, self.selected_type)

        if unlocks:
            unlock_msg = "New unlocks!\n"
            for unlock_type, unlock_name, unlock_desc in unlocks:
                unlock_msg += f"\n{unlock_type.title()}: {unlock_name}\n{unlock_desc}"
            messagebox.showinfo("Unlocks!", unlock_msg)

        messagebox.showinfo("Success", f"Game '{game_name}' created successfully!\n\nDevelopment will begin immediately.")

        # Clear selections
        self.selected_topic = None
        self.selected_type = None
        self.name_entry.delete(0, tk.END)
        self.topic_listbox.selection_clear(0, tk.END)
        self.type_listbox.selection_clear(0, tk.END)
        self.update_selection_display()

        # Close window
        self.window.destroy()

    def generate_game_names(self):
        """Generate 10 game names using DeepSeek API in one call"""
        if not self.naming_service:
            print("No naming service available (API key not found)")
            return

        print(f"Generating names for {self.selected_topic} {self.selected_type}...")

        try:
            # Store default name as first option
            default_name = f"{self.selected_topic} {self.selected_type} GAME!!"

            # Request all 10 names in one API call
            prompt = f"""Give me 10 creative names for a {self.selected_topic} {self.selected_type} game.
            Mix of styles:
            - 2 FUN names (playful, lighthearted)
            - 2 SERIOUS names (dramatic, intense)
            - 2 EPIC names (grand, legendary)
            - 2 MYSTERIOUS names (intriguing, enigmatic)
            - 2 STRANGE names (weird, unique)

            Return only the names, one per line, no explanations or categories."""

            try:
                print(f"Requesting 10 names from API in single call...")
                names = self.naming_service.generate_game_names(prompt, count=10)
                if names:
                    print(f"Got {len(names)} names: {names}")
                    self.generated_names = [default_name] + names[:10]
                else:
                    # Fallback to default only
                    self.generated_names = [default_name]
            except Exception as e:
                print(f"Failed to get names: {e}")
                # Use fallback names
                self.generated_names = [default_name]

            # If we didn't get exactly 11 names (default + 10), fill with variations
            while len(self.generated_names) < 11:
                variation = f"{self.selected_topic} {self.selected_type} {len(self.generated_names)}"
                self.generated_names.append(variation)

            print(f"Generated {len(self.generated_names)} total names")
            self.current_name_index = 0

        except Exception as e:
            print(f"Error generating names: {e}")

    def randomize_name(self):
        """Generate names on first click, then cycle through them"""
        # Only proceed if both topic and type are selected
        if not self.selected_topic or not self.selected_type:
            return

        # Generate names on first click (when we only have the default)
        if len(self.generated_names) <= 1:
            self.generate_game_names()

        # Cycle to next name
        self.current_name_index = (self.current_name_index + 1) % len(self.generated_names)

        # Update entry field
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.generated_names[self.current_name_index])

    def save_name_for_later(self):
        """Save the current name to notes"""
        current_name = self.name_entry.get().strip()
        if not current_name:
            messagebox.showwarning("No Name", "Please enter a game name to save!")
            return

        # Initialize saved names list if not exists (using consistent key with NotesApp)
        if 'saved_game_names' not in self.game_data.data:
            self.game_data.data['saved_game_names'] = []

        # Add the name with metadata
        saved_entry = {
            'name': current_name,
            'topic': self.selected_topic if self.selected_topic else "No topic selected",
            'type': self.selected_type if self.selected_type else "No type selected",
            'date': self.game_data.data.get('game_time', {}).get('current_date', 'Unknown')
        }

        # Check if already saved
        existing_names = [entry.get('name') if isinstance(entry, dict) else entry
                         for entry in self.game_data.data['saved_game_names']]
        if current_name not in existing_names:
            self.game_data.data['saved_game_names'].append(saved_entry)

            # Show success with option to open notes
            result = messagebox.askyesno("Saved to Notes",
                                        f"'{current_name}' has been saved to your notes!\n\nWould you like to open the Notes app?")
            if result:
                self.open_notes_app()
        else:
            messagebox.showinfo("Already Saved", f"'{current_name}' is already in your notes!")

    def open_notes_app(self):
        """Open the Notes application"""
        from desktop.notes_app import NotesApp
        NotesApp(self.window, self.game_data)