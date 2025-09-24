"""
Game Engine Interface - Create games with OpenEngine
"""

import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar
from systems.unlock_system import UnlockSystem
from games.game_database import GameDatabase


class GameEngineWindow:
    """Game creation interface for OpenEngine"""

    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        self.unlock_system = UnlockSystem(game_data)
        self.game_db = GameDatabase(game_data)

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

        self.name_entry = tk.Entry(name_frame, bg='#0a0a0f', fg='#00ff00',
                                   font=('Consolas', 12), insertbackground='#00ff00')
        self.name_entry.pack(fill='x', pady=5)

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
        self.create_btn = tk.Button(right_panel, text="CREATE GAME",
                                   command=self.create_game,
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

            # Estimate development time (simplified)
            base_days = 30
            if self.selected_type in ['MMORPG', 'Open World', 'Battle Royale']:
                base_days = 180
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