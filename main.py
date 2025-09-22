import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml
import os
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from deepseek.services.naming import get_random_studio_names

class SaveManager:
    def __init__(self):
        self.save_dir = Path("saves")
        self.save_dir.mkdir(exist_ok=True)

    def list_saves(self):
        """Return list of available save files"""
        save_files = []
        for file in self.save_dir.glob("*.yaml"):
            try:
                with open(file, 'r') as f:
                    data = yaml.safe_load(f)
                    save_info = {
                        'filename': file.stem,
                        'path': str(file),
                        'studio_name': data.get('player_data', {}).get('studio_name', 'Unknown Studio'),
                        'last_played': data.get('game_metadata', {}).get('last_played', 'Unknown'),
                        'playtime': data.get('game_metadata', {}).get('playtime_hours', 0)
                    }
                    save_files.append(save_info)
            except Exception as e:
                print(f"Error reading save file {file}: {e}")
        return save_files

    def load_game(self, filename):
        """Load game data from save file"""
        save_path = self.save_dir / f"{filename}.yaml"
        try:
            with open(save_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Failed to load save file: {e}")

    def save_game(self, filename, game_data):
        """Save game data to file"""
        save_path = self.save_dir / f"{filename}.yaml"
        try:
            # Update metadata
            game_data['game_metadata']['last_played'] = datetime.now().isoformat()

            with open(save_path, 'w') as f:
                yaml.dump(game_data, f, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            raise Exception(f"Failed to save game: {e}")

class GameData:
    def __init__(self):
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """Initialize with default game data"""
        self.data = {
            'game_metadata': {
                'version': '1.0.0',
                'save_name': 'New Studio',
                'created_date': datetime.now().isoformat(),
                'last_played': datetime.now().isoformat(),
                'playtime_hours': 0.0
            },
            'player_data': {
                'studio_name': 'My Game Studio',
                'player_name': 'Game Developer',
                'current_money': 10000,
                'reputation': 0,
                'stress_level': 0,
                'energy': 100
            },
            'skills': {
                'programming': 25,
                'art': 25,
                'design': 25,
                'marketing': 10,
                'business': 10,
                'project_management': 10
            },
            'studio_stats': {
                'games_published': 0,
                'total_sales': 0,
                'awards_won': 0,
                'employees_hired': 0,
                'years_in_business': 0
            },
            'current_projects': [],
            'employees': [],
            'completed_games': [],
            'game_types': {
                'unlocked': ['Text Adventure', 'Simple Puzzle'],
                'locked': ['Platformer', 'RPG', 'Strategy', 'Racing']
            },
            'settings': {
                'auto_save_enabled': True,
                'difficulty': 'Normal',
                'tutorial_completed': False
            }
        }

    def load_from_dict(self, data):
        """Load game data from dictionary"""
        self.data = data

    def get(self, *keys):
        """Get nested value from data"""
        current = self.data
        for key in keys:
            current = current.get(key, {})
        return current

    def set(self, value, *keys):
        """Set nested value in data"""
        current = self.data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

class StartMenu:
    def __init__(self, parent, on_new_game, on_load_game, on_options, on_quit):
        self.parent = parent
        self.on_new_game = on_new_game
        self.on_load_game = on_load_game
        self.on_options = on_options
        self.on_quit = on_quit
        self.frame = None

    def show(self):
        if self.frame:
            self.frame.destroy()

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(self.frame, text="Game Dev Studio",
                               font=('Arial', 24, 'bold'))
        title_label.pack(pady=50)

        subtitle_label = ttk.Label(self.frame, text="Build Your Gaming Empire",
                                  font=('Arial', 12))
        subtitle_label.pack(pady=10)

        # Buttons frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=50)

        # Buttons
        ttk.Button(button_frame, text="New Game",
                  command=self.on_new_game, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Load Game",
                  command=self.on_load_game, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Options",
                  command=self.on_options, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Quit",
                  command=self.on_quit, width=20).pack(pady=5)

class LoadGameMenu:
    def __init__(self, parent, save_manager, on_back, on_load):
        self.parent = parent
        self.save_manager = save_manager
        self.on_back = on_back
        self.on_load = on_load
        self.frame = None

    def show(self):
        if self.frame:
            self.frame.destroy()

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(self.frame, text="Load Game",
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)

        # Saves list frame
        saves_frame = ttk.Frame(self.frame)
        saves_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Treeview for save files
        columns = ('Studio Name', 'Last Played', 'Hours Played')
        self.tree = ttk.Treeview(saves_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(saves_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Load save files
        self.refresh_saves()

        # Buttons frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Load Selected",
                  command=self.load_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Selected",
                  command=self.delete_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh",
                  command=self.refresh_saves).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Back",
                  command=self.on_back).pack(side='left', padx=5)

    def refresh_saves(self):
        """Refresh the list of save files"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        saves = self.save_manager.list_saves()
        for save in saves:
            self.tree.insert('', 'end', values=(
                save['studio_name'],
                save['last_played'][:10] if save['last_played'] != 'Unknown' else 'Unknown',
                f"{save['playtime']:.1f}h"
            ), tags=(save['filename'],))

    def load_selected(self):
        """Load the selected save file"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a save file to load.")
            return

        item = self.tree.item(selection[0])
        filename = item['tags'][0]

        try:
            self.on_load(filename)
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load save file: {str(e)}")

    def delete_selected(self):
        """Delete the selected save file"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a save file to delete.")
            return

        item = self.tree.item(selection[0])
        filename = item['tags'][0]

        if messagebox.askyesno("Confirm Delete", f"Delete save file '{filename}'?"):
            try:
                save_path = self.save_manager.save_dir / f"{filename}.yaml"
                save_path.unlink()
                self.refresh_saves()
                messagebox.showinfo("Deleted", "Save file deleted successfully.")
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete save file: {str(e)}")

class MainGameWindow:
    def __init__(self, parent, game_data, save_manager, on_save, on_menu):
        self.parent = parent
        self.game_data = game_data
        self.save_manager = save_manager
        self.on_save = on_save
        self.on_menu = on_menu
        self.frame = None

    def show(self):
        if self.frame:
            self.frame.destroy()

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill='both', expand=True)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Studio Overview Tab
        self.create_studio_tab(notebook)

        # Projects Tab
        self.create_projects_tab(notebook)

        # Team Tab
        self.create_team_tab(notebook)

        # Market Tab
        self.create_market_tab(notebook)

        # Menu bar frame
        menu_frame = ttk.Frame(self.frame)
        menu_frame.pack(fill='x', pady=5)

        ttk.Button(menu_frame, text="Save Game",
                  command=self.on_save).pack(side='left', padx=5)
        ttk.Button(menu_frame, text="Main Menu",
                  command=self.on_menu).pack(side='left', padx=5)

    def create_studio_tab(self, notebook):
        """Create studio overview tab"""
        studio_frame = ttk.Frame(notebook)
        notebook.add(studio_frame, text="Studio")

        # Studio info
        info_frame = ttk.LabelFrame(studio_frame, text="Studio Information")
        info_frame.pack(fill='x', padx=10, pady=5)

        player_data = self.game_data.get('player_data')
        studio_stats = self.game_data.get('studio_stats')

        ttk.Label(info_frame, text=f"Studio: {player_data.get('studio_name', 'Unknown')}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Owner: {player_data.get('player_name', 'Unknown')}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Money: ${player_data.get('current_money', 0):,}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Reputation: {player_data.get('reputation', 0)}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Games Published: {studio_stats.get('games_published', 0)}").pack(anchor='w')

        # Skills frame
        skills_frame = ttk.LabelFrame(studio_frame, text="Skills")
        skills_frame.pack(fill='x', padx=10, pady=5)

        skills = self.game_data.get('skills')
        for skill, level in skills.items():
            skill_frame = ttk.Frame(skills_frame)
            skill_frame.pack(fill='x', padx=5, pady=2)

            ttk.Label(skill_frame, text=f"{skill.title()}:", width=15).pack(side='left')

            progress = ttk.Progressbar(skill_frame, length=200, maximum=100, value=level)
            progress.pack(side='left', padx=5)

            ttk.Label(skill_frame, text=f"{level}").pack(side='left')

    def create_projects_tab(self, notebook):
        """Create projects tab"""
        projects_frame = ttk.Frame(notebook)
        notebook.add(projects_frame, text="Projects")

        ttk.Label(projects_frame, text="Current Projects",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        # Current projects list
        current_projects = self.game_data.get('current_projects')
        if not current_projects:
            ttk.Label(projects_frame, text="No active projects",
                     font=('Arial', 10, 'italic')).pack(pady=20)

        # New project button
        ttk.Button(projects_frame, text="Start New Project",
                  command=self.start_new_project).pack(pady=10)

    def create_team_tab(self, notebook):
        """Create team tab"""
        team_frame = ttk.Frame(notebook)
        notebook.add(team_frame, text="Team")

        ttk.Label(team_frame, text="Team Members",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        employees = self.game_data.get('employees')
        if not employees:
            ttk.Label(team_frame, text="No employees hired yet",
                     font=('Arial', 10, 'italic')).pack(pady=20)
            ttk.Label(team_frame, text="You are working solo for now!",
                     font=('Arial', 10)).pack()

        # Hire button
        ttk.Button(team_frame, text="Hire Employee",
                  command=self.hire_employee).pack(pady=10)

    def create_market_tab(self, notebook):
        """Create market tab"""
        market_frame = ttk.Frame(notebook)
        notebook.add(market_frame, text="Market")

        ttk.Label(market_frame, text="Game Market Analysis",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        # Game types info
        game_types_frame = ttk.LabelFrame(market_frame, text="Available Game Types")
        game_types_frame.pack(fill='x', padx=10, pady=5)

        game_types = self.game_data.get('game_types', {})
        unlocked = game_types.get('unlocked', [])
        locked = game_types.get('locked', [])

        ttk.Label(game_types_frame, text="Unlocked Types:",
                 font=('Arial', 10, 'bold')).pack(anchor='w')
        for game_type in unlocked:
            ttk.Label(game_types_frame, text=f"  • {game_type}").pack(anchor='w')

        ttk.Label(game_types_frame, text="Locked Types:",
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,0))
        for game_type in locked:
            ttk.Label(game_types_frame, text=f"  • {game_type} (Requires research)").pack(anchor='w')

    def start_new_project(self):
        """Start a new game project"""
        messagebox.showinfo("New Project", "Project creation coming soon!")

    def hire_employee(self):
        """Hire a new employee"""
        messagebox.showinfo("Hire Employee", "Employee hiring coming soon!")

class GameDevStudioApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Dev Studio")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Initialize managers and data
        self.save_manager = SaveManager()
        self.game_data = GameData()

        # Initialize UI components
        self.current_screen = None
        self.start_menu = StartMenu(self.root,
                                  self.new_game,
                                  self.show_load_menu,
                                  self.show_options,
                                  self.quit_game)

        self.load_menu = LoadGameMenu(self.root,
                                    self.save_manager,
                                    self.show_start_menu,
                                    self.load_game)

        # Show start menu
        self.show_start_menu()

    def show_start_menu(self):
        """Show the start menu"""
        self.clear_screen()
        self.start_menu.show()
        self.current_screen = "start"

    def show_load_menu(self):
        """Show the load game menu"""
        self.clear_screen()
        self.load_menu.show()
        self.current_screen = "load"

    def show_main_game(self):
        """Show the main game window"""
        self.clear_screen()
        self.main_game = MainGameWindow(self.root,
                                      self.game_data,
                                      self.save_manager,
                                      self.save_current_game,
                                      self.show_start_menu)
        self.main_game.show()
        self.current_screen = "game"

    def show_options(self):
        """Show options menu"""
        messagebox.showinfo("Options", "Options menu coming soon!")

    def clear_screen(self):
        """Clear all widgets from the main window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def new_game(self):
        """Start a new game"""
        # Show new game dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("New Game")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Studio name entry
        ttk.Label(dialog, text="Studio Name:").pack(pady=5)
        studio_name_var = tk.StringVar(value="My Game Studio")
        ttk.Entry(dialog, textvariable=studio_name_var, width=30).pack(pady=5)

        # Player name entry
        ttk.Label(dialog, text="Your Name:").pack(pady=5)
        player_name_var = tk.StringVar(value="Game Developer")
        ttk.Entry(dialog, textvariable=player_name_var, width=30).pack(pady=5)

        # Difficulty selection
        ttk.Label(dialog, text="Difficulty:").pack(pady=5)
        difficulty_var = tk.StringVar(value="Normal")
        difficulty_combo = ttk.Combobox(dialog, textvariable=difficulty_var,
                                       values=["Easy", "Normal", "Hard"],
                                       state="readonly")
        difficulty_combo.pack(pady=5)

        def start_game():
            # Create new game data
            self.game_data.reset_to_defaults()
            self.game_data.set(studio_name_var.get(), 'player_data', 'studio_name')
            self.game_data.set(player_name_var.get(), 'player_data', 'player_name')
            self.game_data.set(difficulty_var.get(), 'settings', 'difficulty')

            dialog.destroy()
            self.show_main_game()

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Start Game",
                  command=start_game).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel",
                  command=dialog.destroy).pack(side='left', padx=5)

    def load_game(self, filename):
        """Load a game from save file"""
        try:
            save_data = self.save_manager.load_game(filename)
            self.game_data.load_from_dict(save_data)
            self.show_main_game()
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load game: {str(e)}")

    def save_current_game(self):
        """Save the current game"""
        if self.current_screen != "game":
            return

        # Show save dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Game")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Save Name:").pack(pady=5)
        save_name_var = tk.StringVar(value=self.game_data.get('player_data', 'studio_name'))
        ttk.Entry(dialog, textvariable=save_name_var, width=30).pack(pady=5)

        def do_save():
            try:
                self.save_manager.save_game(save_name_var.get(), self.game_data.data)
                dialog.destroy()
                messagebox.showinfo("Saved", "Game saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save game: {str(e)}")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Save", command=do_save).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)

    def quit_game(self):
        """Quit the application"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GameDevStudioApp()
    app.run()