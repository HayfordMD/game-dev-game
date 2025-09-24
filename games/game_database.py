"""
Game Database System
Stores all created games and their metadata
"""

import json
import os
from datetime import datetime


class GameDatabase:
    """Manages all games created by the player"""

    def __init__(self):
        self.db_file = "games/games_db.json"
        self.games = self.load_games()

    def load_games(self):
        """Load games database"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_games(self):
        """Save games database"""
        os.makedirs('games', exist_ok=True)
        with open(self.db_file, 'w') as f:
            json.dump(self.games, f, indent=2)

    def create_game(self, name, topic, game_type, year, month, rating=None):
        """Create a new game entry"""
        game = {
            'id': len(self.games) + 1,
            'name': name,
            'topic': topic,
            'game_type': game_type,
            'created_date': {
                'year': year,
                'month': month
            },
            'rating': rating,
            'sales': 0,
            'platforms': [],
            'development_time': 0,
            'team_size': 1
        }

        self.games.append(game)
        self.save_games()

        # Generate Python script for the game
        self.generate_game_script(game)

        return game

    def generate_game_script(self, game):
        """Generate a Python script file for the game"""
        safe_name = game['name'].replace(' ', '_').replace('/', '_').lower()
        script_path = f"games/{safe_name}.py"

        script_content = f'''"""
Game: {game['name']}
Topic: {game['topic']}
Type: {game['game_type']}
Created: {game['created_date']['year']}/{game['created_date']['month']:02d}
"""

import tkinter as tk
from tkinter import messagebox


class {safe_name.title().replace('_', '')}Game:
    """Game implementation for {game['name']}"""

    def __init__(self):
        self.name = "{game['name']}"
        self.topic = "{game['topic']}"
        self.game_type = "{game['game_type']}"
        self.window = None

    def launch(self):
        """Launch the game"""
        self.window = tk.Tk()
        self.window.title(self.name)
        self.window.geometry("640x480")

        # Game title
        tk.Label(self.window, text=self.name, font=('Arial', 24, 'bold')).pack(pady=20)
        tk.Label(self.window, text=f"{self.topic} - {self.game_type}", font=('Arial', 14)).pack()

        # Game content area
        content_frame = tk.Frame(self.window, bg='#333', width=600, height=350)
        content_frame.pack(pady=20)
        content_frame.pack_propagate(False)

'''

        # Add game-type specific content
        if game['game_type'] == 'Text Adventure':
            script_content += '''        # Text adventure interface
        self.text_area = tk.Text(content_frame, bg='black', fg='green',
                                 font=('Courier', 12), wrap=tk.WORD)
        self.text_area.pack(fill='both', expand=True, padx=10, pady=10)

        self.text_area.insert(tk.END, f"Welcome to {self.name}!\\n\\n")
        self.text_area.insert(tk.END, f"A {self.topic} text adventure awaits...\\n\\n")
        self.text_area.insert(tk.END, "> ")

        # Input field
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=10)

        self.input_field = tk.Entry(input_frame, width=50, font=('Courier', 12))
        self.input_field.pack(side='left', padx=5)
        self.input_field.bind('<Return>', self.process_command)

        tk.Button(input_frame, text="Enter", command=self.process_command).pack(side='left')

    def process_command(self, event=None):
        """Process player commands"""
        command = self.input_field.get()
        self.text_area.insert(tk.END, f"{command}\\n")

        # Simple command processing
        if command.lower() in ['look', 'examine']:
            self.text_area.insert(tk.END, f"You see a {self.topic.lower()} world around you...\\n")
        elif command.lower() in ['help', '?']:
            self.text_area.insert(tk.END, "Commands: look, help, quit\\n")
        elif command.lower() in ['quit', 'exit']:
            self.window.destroy()
            return
        else:
            self.text_area.insert(tk.END, "I don't understand that command.\\n")

        self.text_area.insert(tk.END, "> ")
        self.text_area.see(tk.END)
        self.input_field.delete(0, tk.END)
'''

        elif game['game_type'] == 'Arcade':
            script_content += '''        # Arcade game interface
        canvas = tk.Canvas(content_frame, bg='black', width=580, height=330)
        canvas.pack(padx=10, pady=10)

        # Simple arcade game elements
        self.score = 0
        self.score_label = tk.Label(self.window, text=f"Score: {self.score}",
                                   font=('Arial', 14))
        self.score_label.pack()

'''
            # Special case for Table Tennis/Ping
            if game['topic'] == 'Table Tennis' and game['name'].lower() == 'ping':
                script_content += '''        # Ping game - special Table Tennis arcade
        self.ball = canvas.create_oval(285, 160, 295, 170, fill='white')
        self.paddle_left = canvas.create_rectangle(10, 140, 20, 190, fill='white')
        self.paddle_right = canvas.create_rectangle(560, 140, 570, 190, fill='white')

        canvas.create_text(290, 50, text="PING", font=('Arial', 32, 'bold'), fill='white')
        canvas.create_text(290, 90, text="Table Tennis Arcade", font=('Arial', 14), fill='gray')
        canvas.create_text(290, 300, text="Classic game unlocked!", font=('Arial', 10), fill='yellow')
'''
            else:
                script_content += f'''        # Generic arcade elements for {game['topic']}
        canvas.create_text(290, 165, text="{game['topic'].upper()}\\nARCADE",
                          font=('Arial', 24, 'bold'), fill='white', justify='center')
'''

        elif game['game_type'] == 'Office':
            script_content += '''        # Office game interface - productivity suite
        notebook = tk.Frame(content_frame, bg='white')
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Toolbar
        toolbar = tk.Frame(notebook, bg='#ddd', height=40)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)

        tk.Button(toolbar, text="📄 New", font=('Arial', 10)).pack(side='left', padx=2, pady=2)
        tk.Button(toolbar, text="💾 Save", font=('Arial', 10)).pack(side='left', padx=2, pady=2)
        tk.Button(toolbar, text="📊 Chart", font=('Arial', 10)).pack(side='left', padx=2, pady=2)

        # Spreadsheet-like interface
        text_area = tk.Text(notebook, font=('Courier', 11))
        text_area.pack(fill='both', expand=True)
        text_area.insert(tk.END, "Welcome to Office Suite!\\n\\n")
        text_area.insert(tk.END, "Productivity tools for the modern workplace.\\n")
'''
        else:
            script_content += f'''        # Generic game interface for {game['game_type']}
        tk.Label(content_frame, text="Game Area", font=('Arial', 18),
                bg='#333', fg='white').pack(expand=True)
'''

        script_content += '''
        # Exit button
        tk.Button(self.window, text="Exit Game", command=self.window.destroy,
                 bg='#ff4444', fg='white', font=('Arial', 12)).pack(pady=10)

        self.window.mainloop()


if __name__ == "__main__":
    game = ''' + f"{safe_name.title().replace('_', '')}Game()" + '''
    game.launch()
'''

        with open(script_path, 'w') as f:
            f.write(script_content)

        return script_path

    def get_game_by_id(self, game_id):
        """Get a specific game by ID"""
        for game in self.games:
            if game['id'] == game_id:
                return game
        return None

    def get_games_by_type(self, game_type):
        """Get all games of a specific type"""
        return [g for g in self.games if g['game_type'] == game_type]

    def get_games_by_topic(self, topic):
        """Get all games with a specific topic"""
        return [g for g in self.games if g['topic'] == topic]

    def get_recent_games(self, count=5):
        """Get the most recent games"""
        return self.games[-count:] if self.games else []