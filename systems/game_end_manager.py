"""
Game End Manager
Handles the ending of all minigames, score distribution, and transition back to development
"""

import tkinter as tk
from tkinter import ttk
import random
from dataclasses import dataclass
from typing import Dict, Optional, Callable
import json
import os

@dataclass
class GTGISSScores:
    """GTGISS score structure"""
    gameplay: int = 0
    technical: int = 0
    graphics: int = 0
    innovation: int = 0
    sound: int = 0
    story: int = 0

    @property
    def total(self) -> int:
        return self.gameplay + self.technical + self.graphics + self.innovation + self.sound + self.story

    def to_dict(self) -> Dict[str, int]:
        return {
            'gameplay': self.gameplay,
            'technical': self.technical,
            'graphics': self.graphics,
            'innovation': self.innovation,
            'sound': self.sound,
            'story': self.story,
            'total': self.total
        }

    def copy(self):
        return GTGISSScores(
            gameplay=self.gameplay,
            technical=self.technical,
            graphics=self.graphics,
            innovation=self.innovation,
            sound=self.sound,
            story=self.story
        )

class GameEndManager:
    """Manages the ending of minigames and score distribution"""

    # Singleton instance
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not GameEndManager._initialized:
            self.current_scores = GTGISSScores()
            self.before_scores = None
            self.after_scores = None
            self.minigame_score = 0
            self.game_name = "Untitled Game"
            self.game_type = "Unknown"
            self.game_topic = "Unknown"
            self.return_callback = None
            self.root = None
            GameEndManager._initialized = True

    def set_game_info(self, game_name: str, game_type: str, game_topic: str, current_scores: GTGISSScores):
        """Set the current game information before starting minigame"""
        self.game_name = game_name
        self.game_type = game_type
        self.game_topic = game_topic
        self.before_scores = current_scores.copy()
        self.current_scores = current_scores.copy()

        # Save to temporary file for minigames to read
        temp_data = {
            'game_name': game_name,
            'game_type': game_type,
            'game_topic': game_topic,
            'before_scores': self.before_scores.to_dict()
        }

        temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_game_data.json')
        with open(temp_path, 'w') as f:
            json.dump(temp_data, f)

    def handle_game_end(self, minigame_score: int, root: tk.Tk = None, return_callback: Callable = None):
        """Handle the end of a minigame"""
        self.minigame_score = minigame_score
        self.root = root or tk.Tk()
        self.return_callback = return_callback

        # Load game data if not set
        if self.before_scores is None:
            self._load_temp_data()

        # Distribute the minigame score to GTGISS categories
        self.distribute_score(minigame_score)

        # Show the results window
        self.show_results_window()

    def _load_temp_data(self):
        """Load temporary game data if available"""
        temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_game_data.json')
        if os.path.exists(temp_path):
            with open(temp_path, 'r') as f:
                data = json.load(f)
                self.game_name = data.get('game_name', 'Untitled Game')
                self.game_type = data.get('game_type', 'Unknown')
                self.game_topic = data.get('game_topic', 'Unknown')

                before_data = data.get('before_scores', {})
                self.before_scores = GTGISSScores(
                    gameplay=before_data.get('gameplay', 0),
                    technical=before_data.get('technical', 0),
                    graphics=before_data.get('graphics', 0),
                    innovation=before_data.get('innovation', 0),
                    sound=before_data.get('sound', 0),
                    story=before_data.get('story', 0)
                )
                self.current_scores = self.before_scores.copy()

    def distribute_score(self, minigame_score: int):
        """Distribute minigame score to GTGISS categories"""
        print(f"\n[GAME END] Distributing {minigame_score} points from minigame")

        # Start with before scores
        self.after_scores = self.before_scores.copy()

        # Categories and their weights based on game type
        weights = self.get_category_weights()

        # Distribute points based on weights
        remaining = minigame_score
        distribution = {}

        # Calculate total weight
        total_weight = sum(weights.values())

        # Distribute proportionally with some randomness
        for category, weight in weights.items():
            if remaining <= 0:
                break

            # Base amount from weight
            base_amount = int((weight / total_weight) * minigame_score)

            # Add some randomness (-2 to +2)
            variance = random.randint(-2, 2)
            amount = max(0, base_amount + variance)

            # Don't exceed remaining
            amount = min(amount, remaining)

            distribution[category] = amount
            remaining -= amount

        # Distribute any remaining points randomly
        categories = list(weights.keys())
        while remaining > 0:
            category = random.choice(categories)
            points = min(random.randint(1, 3), remaining)
            distribution[category] = distribution.get(category, 0) + points
            remaining -= points

        # Apply distribution
        for category, points in distribution.items():
            current = getattr(self.after_scores, category)
            setattr(self.after_scores, category, current + points)
            print(f"  +{points} to {category}")

        print(f"[GAME END] Total before: {self.before_scores.total}")
        print(f"[GAME END] Total after: {self.after_scores.total}")

    def get_category_weights(self) -> Dict[str, int]:
        """Get category weights based on game type"""
        # Default weights
        weights = {
            'gameplay': 5,
            'technical': 3,
            'graphics': 3,
            'innovation': 2,
            'sound': 2,
            'story': 2
        }

        # Adjust based on game type
        if self.game_type.lower() == "arcade":
            weights['gameplay'] = 7
            weights['technical'] = 4
            weights['graphics'] = 5
            weights['sound'] = 3
            weights['story'] = 1
        elif self.game_type.lower() in ["text adventure", "adventure"]:
            weights['story'] = 7
            weights['gameplay'] = 4
            weights['innovation'] = 4
            weights['graphics'] = 1
        elif self.game_type.lower() == "rpg":
            weights['story'] = 6
            weights['gameplay'] = 5
            weights['graphics'] = 4
        elif self.game_type.lower() == "puzzle":
            weights['gameplay'] = 6
            weights['innovation'] = 5
            weights['technical'] = 3
        elif self.game_type.lower() == "shooter":
            weights['gameplay'] = 6
            weights['technical'] = 5
            weights['graphics'] = 4
            weights['sound'] = 4

        return weights

    def show_results_window(self):
        """Show the game results window with before/after scores"""
        # Create window
        self.results_window = tk.Toplevel(self.root) if self.root else tk.Tk()
        self.results_window.title("Development Results")
        self.results_window.geometry("800x700")
        self.results_window.configure(bg='#0a0a0f')

        # Center window
        self.results_window.update_idletasks()
        x = (self.results_window.winfo_screenwidth() // 2) - 400
        y = (self.results_window.winfo_screenheight() // 2) - 350
        self.results_window.geometry(f"800x700+{x}+{y}")

        # Main container
        main_frame = tk.Frame(self.results_window, bg='#0a0a0f')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="DEVELOPMENT COMPLETE",
            font=('Consolas', 24, 'bold'),
            fg='#00ff88',
            bg='#0a0a0f'
        )
        title_label.pack(pady=(0, 10))

        # Game info
        game_info_label = tk.Label(
            main_frame,
            text=f"{self.game_name}",
            font=('Arial', 18, 'bold'),
            fg='#4a9eff',
            bg='#0a0a0f'
        )
        game_info_label.pack()

        game_type_label = tk.Label(
            main_frame,
            text=f"{self.game_type} - {self.game_topic}",
            font=('Arial', 12),
            fg='#888888',
            bg='#0a0a0f'
        )
        game_type_label.pack(pady=(0, 20))

        # Minigame score
        minigame_frame = tk.Frame(main_frame, bg='#1a1a2e', relief='ridge', bd=2)
        minigame_frame.pack(fill='x', pady=10)

        tk.Label(
            minigame_frame,
            text=f"Minigame Score: {self.minigame_score} points",
            font=('Arial', 14, 'bold'),
            fg='#ffc107',
            bg='#1a1a2e'
        ).pack(pady=10)

        # GTGISS Scores Container
        scores_container = tk.Frame(main_frame, bg='#0a0a0f')
        scores_container.pack(fill='both', expand=True, pady=20)

        # Before scores (left)
        before_frame = tk.Frame(scores_container, bg='#1a1a2e', relief='ridge', bd=2)
        before_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        tk.Label(
            before_frame,
            text="BEFORE MINIGAME",
            font=('Arial', 14, 'bold'),
            fg='#888888',
            bg='#1a1a2e'
        ).pack(pady=10)

        self._create_score_display(before_frame, self.before_scores)

        # Arrow
        arrow_frame = tk.Frame(scores_container, bg='#0a0a0f')
        arrow_frame.pack(side='left', padx=10)

        tk.Label(
            arrow_frame,
            text="→",
            font=('Arial', 32, 'bold'),
            fg='#00ff88',
            bg='#0a0a0f'
        ).pack(expand=True)

        # After scores (right)
        after_frame = tk.Frame(scores_container, bg='#1a1a2e', relief='ridge', bd=2)
        after_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))

        tk.Label(
            after_frame,
            text="AFTER MINIGAME",
            font=('Arial', 14, 'bold'),
            fg='#00ff88',
            bg='#1a1a2e'
        ).pack(pady=10)

        self._create_score_display(after_frame, self.after_scores, show_changes=True)

        # Total change
        total_change = self.after_scores.total - self.before_scores.total
        change_label = tk.Label(
            main_frame,
            text=f"Total Points Gained: +{total_change}",
            font=('Arial', 16, 'bold'),
            fg='#00ff88',
            bg='#0a0a0f'
        )
        change_label.pack(pady=20)

        # Continue button
        continue_btn = tk.Button(
            main_frame,
            text="Continue to Development",
            font=('Arial', 14, 'bold'),
            bg='#4a9eff',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.continue_to_development
        )
        continue_btn.pack(pady=20)

        # Make window modal
        self.results_window.transient(self.root)
        self.results_window.grab_set()

    def _create_score_display(self, parent: tk.Frame, scores: GTGISSScores, show_changes: bool = False):
        """Create a display for GTGISS scores"""
        categories = [
            ('Gameplay', 'gameplay', '#4CAF50'),
            ('Technical', 'technical', '#FF9800'),
            ('Graphics', 'graphics', '#2196F3'),
            ('Innovation', 'innovation', '#9C27B0'),
            ('Sound', 'sound', '#E91E63'),
            ('Story', 'story', '#00BCD4')
        ]

        for display_name, key, color in categories:
            row_frame = tk.Frame(parent, bg='#1a1a2e')
            row_frame.pack(fill='x', padx=20, pady=5)

            # Category name
            tk.Label(
                row_frame,
                text=f"{display_name}:",
                font=('Arial', 11),
                fg=color,
                bg='#1a1a2e',
                width=12,
                anchor='w'
            ).pack(side='left')

            # Score value
            value = getattr(scores, key)
            tk.Label(
                row_frame,
                text=str(value),
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='#1a1a2e',
                width=4,
                anchor='e'
            ).pack(side='left', padx=(0, 10))

            # Show change if after scores
            if show_changes and self.before_scores:
                before_value = getattr(self.before_scores, key)
                change = value - before_value
                if change > 0:
                    change_text = f"+{change}"
                    change_color = '#00ff88'
                elif change < 0:
                    change_text = str(change)
                    change_color = '#ff4444'
                else:
                    change_text = ""
                    change_color = '#888888'

                if change_text:
                    tk.Label(
                        row_frame,
                        text=change_text,
                        font=('Arial', 10),
                        fg=change_color,
                        bg='#1a1a2e'
                    ).pack(side='left')

            # Progress bar
            bar_frame = tk.Frame(row_frame, bg='#2a2a2a', height=15, width=100)
            bar_frame.pack(side='left', padx=5, fill='x', expand=True)
            bar_frame.pack_propagate(False)

            # Fill bar based on value (max 50 for display)
            bar_width = min(100, int((value / 50) * 100))
            if bar_width > 0:
                bar = tk.Frame(bar_frame, bg=color, height=15, width=bar_width)
                bar.pack(side='left')

        # Separator
        separator = tk.Frame(parent, bg='#444444', height=2)
        separator.pack(fill='x', padx=20, pady=10)

        # Total
        total_frame = tk.Frame(parent, bg='#1a1a2e')
        total_frame.pack(fill='x', padx=20, pady=(0, 10))

        tk.Label(
            total_frame,
            text="TOTAL:",
            font=('Arial', 12, 'bold'),
            fg='#ffc107',
            bg='#1a1a2e',
            width=12,
            anchor='w'
        ).pack(side='left')

        tk.Label(
            total_frame,
            text=str(scores.total),
            font=('Arial', 14, 'bold'),
            fg='#00ff88',
            bg='#1a1a2e'
        ).pack(side='left')

    def continue_to_development(self):
        """Continue to the next development stage"""
        # Close results window
        if hasattr(self, 'results_window'):
            self.results_window.destroy()

        # Clean up temp file
        temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_game_data.json')
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

        # Call return callback if provided
        if self.return_callback:
            self.return_callback(self.after_scores)
        else:
            print("[GAME END] No return callback provided")

    @classmethod
    def reset(cls):
        """Reset the singleton instance"""
        cls._instance = None
        cls._initialized = False

# Convenience function for minigames to call
def end_minigame(score: int, root: tk.Tk = None, callback: Callable = None):
    """End a minigame and show results"""
    manager = GameEndManager()
    manager.handle_game_end(score, root, callback)