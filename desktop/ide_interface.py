"""
IDE Interface for Game Development
Shows Vidi Vinci Vim (1978-1984) or Ecliption (1984+)
"""

import tkinter as tk
from tkinter import Canvas, messagebox
import os
import importlib.util
import sys
from typing import Optional, Dict, Any


class IDEInterface:
    """Game development IDE with retro terminal look"""

    def __init__(self, root, game_data, on_back: Optional[callable] = None):
        self.root = root
        self.game_data = game_data
        self.on_back = on_back

        # Get current year to determine IDE name
        current_year = 1978
        if 'time' in game_data.data:
            current_year = game_data.data['time'].get('year', 1978)
        elif 'game_time' in game_data.data:
            date_str = game_data.data['game_time'].get('current_date', '1978-01-01')
            current_year = int(date_str.split('-')[0])

        # Set IDE name based on year
        self.ide_name = "Ecliption" if current_year >= 1984 else "Vidi Vinci Vim"

        # Terminal colors (green and black)
        self.bg_color = '#000000'
        self.text_color = '#00ff00'
        self.dim_color = '#008800'

        # Game list - will scan for available games
        self.available_games = []
        self.scan_for_games()

        self.setup_ui()

    def scan_for_games(self):
        """Scan the DevelopmentGames folder for available games"""
        games_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DevelopmentGames')

        # Create directory if it doesn't exist
        if not os.path.exists(games_dir):
            os.makedirs(games_dir)

        self.available_games = []

        # Game categories to scan
        categories = {
            'arcade': 'Arcade Games',
            'rhythm': 'Rhythm Games',
            'adventure': 'Adventure Games'
        }

        # Scan each category folder
        for folder, category_name in categories.items():
            folder_path = os.path.join(games_dir, folder)
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.py') and file != '__init__.py':
                        game_name = file[:-3].replace('_', ' ').replace('Arcade', '').title()
                        self.available_games.append({
                            'name': game_name,
                            'file': os.path.join(folder, file),
                            'category': category_name,
                            'description': f'{category_name} - {game_name}'
                        })

        # Also scan root directory for uncategorized games
        if os.path.exists(games_dir):
            for file in os.listdir(games_dir):
                file_path = os.path.join(games_dir, file)
                if os.path.isfile(file_path) and file.endswith('.py') and file != '__init__.py':
                    game_name = file[:-3].replace('_', ' ').title()
                    self.available_games.append({
                        'name': game_name,
                        'file': file,
                        'category': 'Uncategorized',
                        'description': f'Custom game - {game_name}'
                    })

        # Sort games by category then name
        self.available_games.sort(key=lambda x: (x['category'], x['name']))

    def setup_ui(self):
        """Setup the IDE interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set window to fullscreen dimensions (1920x1080)
        self.root.geometry("1920x1080")
        self.root.configure(bg=self.bg_color)

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Terminal header
        self.create_terminal_header()

        # Main content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Show game selection menu
        self.show_game_menu()

    def create_terminal_header(self):
        """Create the terminal-style header"""
        header_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # ASCII art style title
        title_text = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                           {self.ide_name:^30}                        ║
║                     Game Development Environment                          ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """

        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=('Courier', 12),
            fg=self.text_color,
            bg=self.bg_color,
            justify='left'
        )
        title_label.pack(pady=10)

    def show_game_menu(self):
        """Show the game selection menu"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Menu title
        menu_label = tk.Label(
            self.content_frame,
            text="SELECT GAME TO TEST:",
            font=('Courier', 16, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        menu_label.pack(pady=20)

        # Terminal style separator
        separator = tk.Label(
            self.content_frame,
            text="─" * 60,
            font=('Courier', 12),
            fg=self.dim_color,
            bg=self.bg_color
        )
        separator.pack()

        # List games by category
        current_category = None
        for i, game in enumerate(self.available_games, 1):
            # Add category header if new category
            if game['category'] != current_category:
                current_category = game['category']

                # Category separator
                if i > 1:
                    sep_label = tk.Label(
                        self.content_frame,
                        text="",
                        font=('Courier', 8),
                        fg=self.dim_color,
                        bg=self.bg_color
                    )
                    sep_label.pack(pady=5)

                # Category header
                category_label = tk.Label(
                    self.content_frame,
                    text=f"── {current_category} ──",
                    font=('Courier', 12, 'bold'),
                    fg=self.text_color,
                    bg=self.bg_color
                )
                category_label.pack(pady=10)

            game_frame = tk.Frame(self.content_frame, bg=self.bg_color)
            game_frame.pack(pady=5)

            # Game button styled like terminal text
            game_text = f"  [{i}] {game['name']:<25}"
            game_btn = tk.Button(
                game_frame,
                text=game_text,
                font=('Courier', 12),
                fg=self.text_color,
                bg=self.bg_color,
                bd=0,
                activebackground=self.bg_color,
                activeforeground='#00ffff',
                justify='left',
                anchor='w',
                command=lambda g=game: self.launch_game(g)
            )
            game_btn.pack()

            # Hover effect
            game_btn.bind('<Enter>', lambda e, btn=game_btn: btn.config(fg='#00ffff'))
            game_btn.bind('<Leave>', lambda e, btn=game_btn: btn.config(fg=self.text_color))

        # Terminal style separator
        separator2 = tk.Label(
            self.content_frame,
            text="─" * 60,
            font=('Courier', 12),
            fg=self.dim_color,
            bg=self.bg_color
        )
        separator2.pack(pady=20)

        # Instructions
        instructions = tk.Label(
            self.content_frame,
            text="Click on a game to test it in the development environment",
            font=('Courier', 10),
            fg=self.dim_color,
            bg=self.bg_color
        )
        instructions.pack()

        # Back button (terminal style)
        back_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        back_frame.pack(pady=40)

        back_btn = tk.Button(
            back_frame,
            text="[ESC] EXIT IDE",
            font=('Courier', 12),
            fg=self.text_color,
            bg=self.bg_color,
            bd=1,
            highlightbackground=self.text_color,
            activebackground=self.bg_color,
            activeforeground='#ff0000',
            command=self.exit_ide
        )
        back_btn.pack()

        # Bind ESC key
        self.root.bind('<Escape>', lambda e: self.exit_ide())

    def launch_game(self, game: Dict[str, str]):
        """Launch the selected game"""
        game_file = game['file']
        games_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DevelopmentGames')
        game_path = os.path.join(games_dir, game_file)

        # Create Temple Arcade if it doesn't exist
        if game_file == 'TempleArcade.py' and not os.path.exists(game_path):
            self.create_temple_arcade(game_path)

        # Check if game file exists
        if not os.path.exists(game_path):
            messagebox.showerror("Error", f"Game file not found: {game_file}")
            return

        try:
            # Load the game module
            spec = importlib.util.spec_from_file_location(game['name'], game_path)
            game_module = importlib.util.module_from_spec(spec)

            # Add the module to sys.modules
            sys.modules[game['name']] = game_module

            # Execute the module
            spec.loader.exec_module(game_module)

            # Look for a main game class or function
            if hasattr(game_module, 'TempleRunner'):
                # Create new window for the game
                game_window = tk.Toplevel(self.root)
                game_instance = game_module.TempleRunner(game_window)
            elif hasattr(game_module, 'main'):
                game_module.main(self.root)
            else:
                messagebox.showerror("Error", f"No game class or main function found in {game_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")

    def create_temple_arcade(self, path: str):
        """Create the Temple Arcade game file if it doesn't exist"""
        # This will be created by the next Write operation
        pass

    def exit_ide(self):
        """Exit the IDE and return to previous screen"""
        self.root.unbind('<Escape>')
        if self.on_back:
            self.on_back()