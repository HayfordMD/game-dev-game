"""
Unified Unlock Viewer - Shows unlock badges for topics or game types
"""

import tkinter as tk
from tkinter import ttk
from systems.unlock_system import UnlockSystem


class UnlockViewer:
    """Display unlocks with simple badges - unified for both topics and types"""

    def __init__(self, parent, game_data, view_type="topics"):
        self.parent = parent
        self.game_data = game_data
        self.view_type = view_type  # "topics" or "types"
        self.unlock_system = UnlockSystem(game_data)

        # Configure based on type
        if view_type == "topics":
            self.title = "Topic Unlocks"
            self.title_text = "TOPIC UNLOCKS"
            self.get_unlocked = self.unlock_system.get_all_unlocked_topics
            self.all_items = [
                # Original
                'Table Tennis', 'Fantasy', 'Space', 'Temple', 'Adventure',
                # Horror
                'Zombies', 'Space Zombies', 'Vampires', 'Werewolves', 'Ghosts',
                'Demons', 'Possession', 'Haunted Houses', 'Occult Rituals', 'Psychological Horror',
                'Survival Horror', 'Cursed Artifacts', 'Eldritch Abominations', 'Post-Apocalyptic Horror',
                # Sci-Fi & Futuristic
                'Space Exploration', 'Alien Invasion', 'Space Pirates', 'Time Travel', 'Cyberpunk',
                'AI Uprising', 'Mechs', 'Terraforming', 'Galactic Warfare', 'Space Colonies',
                'Interdimensional Travel', 'Nanotechnology', 'Virtual Reality Worlds', 'Robot Rebellion',
                # Real-World & Occupational
                'Roadwork', 'Trucking', 'Farming', 'Construction', 'Mining',
                'Fishing', 'Logging', 'Factory Work', 'Delivery Services', 'Emergency Response',
                'Garbage Collection', 'Postal Work', 'Oil Drilling', 'Power Grid Management',
                # Fantasy & Mythology
                'Dragons', 'Elves & Dwarves', 'Magic Schools', 'Necromancy', 'Kingdoms & Castles',
                'Gods & Titans', 'Elemental Powers', 'Questing Heroes', 'Mythical Creatures', 'Ancient Ruins',
                'Fairy Tales', 'Dark Forests', 'Magical Artifacts', 'Prophecies',
                # Action & Conflict
                'War', 'Espionage', 'Heists', 'Martial Arts', 'Gladiator Arenas',
                'Gang Warfare', 'Pirate Battles', 'Monster Hunting', 'Bounty Hunting', 'Mercenary Missions',
                'Tactical Infiltration', 'Riot Control', 'Survival Combat', 'Urban Warfare',
                # Historical & Cultural
                'Ancient Egypt', 'Feudal Japan', 'Viking Raids', 'Roman Empire', 'Wild West',
                'World War I', 'World War II', 'Cold War', 'Medieval Europe', 'Renaissance',
                'Industrial Revolution', 'Colonial Exploration', 'Tribal Societies', 'Revolutionary Movements',
                # Urban & Social
                'City Building', 'Dating Sim', 'High School Drama', 'Office Politics', 'Nightlife',
                'Apartment Living', 'Social Media Fame', 'Reality TV', 'Fashion Design', 'Restaurant Management',
                'Crime Investigation', 'Journalism', 'Political Campaigns', 'Suburban Life',
                # Nature & Environment
                'Wildlife Rescue', 'Eco Activism', 'Forest Survival', 'Ocean Exploration', 'Climate Crisis',
                'Natural Disasters', 'Gardening', 'Animal Behavior', 'Weather Control', 'Volcanoes',
                'Arctic Expeditions', 'Desert Survival', 'Cave Diving', 'Meteorology',
                # Creative & Experimental
                'Music Creation', 'Rhythm Games', 'Painting', 'Sculpture', 'Architecture',
                'Dance', 'Poetry', 'Theater', 'Film Production', 'Photography',
                'Fashion', 'Interior Design', 'Toy Making', 'Dreamscapes',
                # Sports
                'Golf', 'Basketball', 'Football', 'Soccer', 'Baseball', 'Tennis',
                'Hockey', 'Boxing', 'Wrestling', 'Skateboarding', 'Skiing', 'Surfing',
                'Olympics', 'Cricket', 'Rugby', 'Volleyball', 'Swimming', 'Track & Field',
                # Other
                'Ninjas', 'Pirates', 'Racing', 'Dinosaurs', 'Robots', 'Bugs'
            ]
            self.label_prefix = "Topic"
        else:  # types
            self.title = "Game Type Unlocks"
            self.title_text = "GAME TYPE UNLOCKS"
            self.get_unlocked = self.unlock_system.get_all_unlocked_game_types
            self.all_items = [
                'Text Adventure', 'Arcade', 'Platformer', 'Puzzle', 'Shooter',
                'Beat em Up', 'RPG', 'Racing', 'Fighting', 'Action-Adventure',
                'FPS', 'TPS', 'Sports', 'Simulation', 'Survival',
                'Strategy', 'MMORPG', 'Rhythm', 'Visual Novel', 'Horror',
                'Sandbox', 'Open World', 'Battle Royale', 'MOBA', 'Idle',
                'Office', 'Retro', 'Educational', 'Motion-Control', 'Touch-Based',
                'VR', 'AR', 'Monsters', 'Board Game'
            ]
            self.label_prefix = "Type"

        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        """Create and configure the window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("1200x800")
        self.window.configure(bg='#1a1a2e')

        # Make it modal
        self.window.transient(self.parent)
        self.window.grab_set()

        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 600
        y = (self.window.winfo_screenheight() // 2) - 400
        self.window.geometry(f"1200x800+{x}+{y}")

    def setup_ui(self):
        """Setup the unlock interface"""
        # Title
        title_frame = tk.Frame(self.window, bg='#2b2b3c', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text=self.title_text,
                font=('Arial', 20, 'bold'), bg='#2b2b3c', fg='#4a9eff').pack(pady=12)

        # Close button
        close_btn = tk.Button(title_frame, text="X", command=self.window.destroy,
                            bg='#ff4444', fg='white', font=('Arial', 10, 'bold'),
                            padx=10, cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')

        # Stats at bottom (before scrollable area)
        stats_frame = tk.Frame(self.window, bg='#2a2a3e', height=50)
        stats_frame.pack(fill='x', side='bottom')
        stats_frame.pack_propagate(False)

        # Container for canvas and scrollbar
        container = tk.Frame(self.window, bg='#1a1a2e')
        container.pack(fill='both', expand=True, padx=20, pady=(10, 0))

        # Create scrollable content
        canvas = tk.Canvas(container, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='#1a1a2e')

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Bind mousewheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Get unlocked items
        unlocked_items = self.get_unlocked()

        # Create badge grid
        row = 0
        col = 0
        max_cols = 8

        # Batch create badges for better performance
        for i, item in enumerate(self.all_items):
            # Create small badge frame
            badge_frame = tk.Frame(content_frame, bg='#2a2a3e', relief='ridge', bd=1,
                                  width=110, height=70)
            badge_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            badge_frame.grid_propagate(False)

            # Check if unlocked
            is_unlocked = item in unlocked_items

            if is_unlocked:
                # Show item name - single label
                tk.Label(badge_frame, text=item,
                        font=('Arial', 9, 'bold'), bg='#2a2a3e', fg='#00ff00',
                        wraplength=100).pack(expand=True)
            else:
                # Show locked with combined text - single label
                tk.Label(badge_frame, text=f"🔒\n{self.label_prefix} {i+1}",
                        font=('Arial', 10), bg='#2a2a3e', fg='#666666').pack(expand=True)

            # Move to next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

            # Update window periodically to prevent freezing
            if i % 20 == 0:
                self.window.update_idletasks()

        # Update stats
        unlocked_count = len([item for item in self.all_items if item in unlocked_items])
        tk.Label(stats_frame,
                text=f"{self.title_text.replace(' UNLOCKS', '')}s Unlocked: {unlocked_count}/{len(self.all_items)}",
                font=('Arial', 12), bg='#2a2a3e', fg='white').pack(pady=15)