"""
Game Types Unlock Page - Shows unlock badges for game types
"""

import tkinter as tk
from systems.unlock_system import UnlockSystem


class TypesUnlockPage:
    """Display game type unlocks with simple badges"""

    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        self.unlock_system = UnlockSystem(game_data)

        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Game Type Unlocks")
        self.window.geometry("800x600")
        self.window.configure(bg='#1a1a2e')

        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()

        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 400
        y = (self.window.winfo_screenheight() // 2) - 300
        self.window.geometry(f"800x600+{x}+{y}")

        self.setup_ui()

    def setup_ui(self):
        """Setup the game types unlock interface"""
        # Title
        title_frame = tk.Frame(self.window, bg='#2b2b3c', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="GAME TYPE UNLOCKS",
                font=('Arial', 20, 'bold'), bg='#2b2b3c', fg='#4a9eff').pack(pady=12)

        # Close button
        close_btn = tk.Button(title_frame, text="X", command=self.window.destroy,
                            bg='#ff4444', fg='white', font=('Arial', 10, 'bold'),
                            padx=10, cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')

        # Main content
        content_frame = tk.Frame(self.window, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Get all unlocked game types
        unlocked_types = self.unlock_system.get_all_unlocked_game_types()

        # Define all possible game types (30 total for display)
        all_game_types = [
            'Text Adventure', 'Arcade', 'Platformer', 'Puzzle', 'Shooter',
            'Beat em Up', 'RPG', 'Racing', 'Fighting', 'Action-Adventure',
            'FPS', 'TPS', 'Sports', 'Simulation', 'Survival',
            'Strategy', 'MMORPG', 'Rhythm', 'Visual Novel', 'Horror',
            'Sandbox', 'Open World', 'Battle Royale', 'MOBA', 'Idle',
            'Office', 'Retro', 'Educational', 'Motion-Control', 'Touch-Based',
            'VR', 'AR'
        ]

        # Create badge grid (6 columns, 5 rows)
        row = 0
        col = 0
        max_cols = 6

        for i, game_type in enumerate(all_game_types):
            # Create small badge frame
            badge_frame = tk.Frame(content_frame, bg='#2a2a3e', relief='ridge', bd=1,
                                  width=110, height=70)
            badge_frame.grid(row=row, column=col, padx=5, pady=5)
            badge_frame.grid_propagate(False)

            # Check if unlocked
            is_unlocked = game_type in unlocked_types

            if is_unlocked:
                # Show game type name
                tk.Label(badge_frame, text=game_type,
                        font=('Arial', 8, 'bold'), bg='#2a2a3e', fg='#00ff00',
                        wraplength=100).place(relx=0.5, rely=0.5, anchor='center')
            else:
                # Show generic locked badge
                tk.Label(badge_frame, text="🔒",
                        font=('Arial', 16), bg='#2a2a3e', fg='#666666').place(relx=0.5, rely=0.3, anchor='center')
                tk.Label(badge_frame, text=f"Type {i+1}",
                        font=('Arial', 8), bg='#2a2a3e', fg='#888888').place(relx=0.5, rely=0.7, anchor='center')

            # Move to next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Stats at bottom
        stats_frame = tk.Frame(self.window, bg='#2a2a3e', height=50)
        stats_frame.pack(fill='x', side='bottom')
        stats_frame.pack_propagate(False)

        unlocked_count = len([t for t in all_game_types if t in unlocked_types])
        tk.Label(stats_frame, text=f"Game Types Unlocked: {unlocked_count}/30",
                font=('Arial', 12), bg='#2a2a3e', fg='white').pack(pady=15)