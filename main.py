import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml
import os
import argparse
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from deepseek.services.naming import get_random_studio_names, get_random_player_names, get_competitor_companies, get_default_competitor_companies
from buildings.studio_room import StudioRoomScreen
from systems.dev_menu import DevMenu

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
    def __init__(self, parent, on_new_game, on_load_game, on_options, on_quit, on_quick_start=None):
        self.parent = parent
        self.on_new_game = on_new_game
        self.on_load_game = on_load_game
        self.on_options = on_options
        self.on_quit = on_quit
        self.on_quick_start = on_quick_start
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
        ttk.Button(button_frame, text="Quick Start (Default Companies)",
                  command=self.on_quick_start, width=20).pack(pady=5)
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

class NewGameScreen:
    def __init__(self, parent, on_back, on_create_studio):
        self.parent = parent
        self.on_back = on_back
        self.on_create_studio = on_create_studio
        self.frame = None

    def show(self):
        if self.frame:
            self.frame.destroy()

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(self.frame, text="Create New Studio",
                               font=('Arial', 24, 'bold'))
        title_label.pack(pady=30)

        # Main content frame
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(expand=True)

        # Studio name section
        ttk.Label(content_frame, text="Name Your Studio", font=('Arial', 14, 'bold')).pack(pady=(20, 10))

        name_frame = ttk.Frame(content_frame)
        name_frame.pack(pady=10)

        self.studio_name_var = tk.StringVar(value="My Game Studio")
        name_entry = ttk.Entry(name_frame, textvariable=self.studio_name_var, width=30, font=('Arial', 12))
        name_entry.pack(side='left', padx=10)

        # Random name button
        self.random_button = ttk.Button(name_frame, text="Random Name?", width=15)
        self.random_button.pack(side='left', padx=10)

        # Random names frame (initially hidden)
        self.random_frame = ttk.LabelFrame(content_frame, text="Choose a Generated Name")
        self.random_names_buttons = []
        self.all_generated_names = []  # Keep track of all generated names
        self.status_label = ttk.Label(self.random_frame, text="", font=('Arial', 10, 'italic'))
        self.status_label.pack(pady=10)

        # Create persistent frames for layout stability
        self.grid_container = ttk.Frame(self.random_frame)
        self.more_button_container = ttk.Frame(self.random_frame)

        def get_random_names():
            """Get random studio names from DeepSeek"""
            self.random_button.config(state='disabled', text="Getting names...")
            self.status_label.config(text="Getting some names!")
            self.frame.update()

            try:
                self.status_label.config(text="Calling AI to generate creative studio names...")
                self.frame.update()

                names = get_random_studio_names()

                # Add new names to all generated names list
                self.all_generated_names.extend(names)

                # Rebuild the entire buttons display
                rebuild_buttons_display()

                # Show the frame
                self.random_frame.pack(fill='x', padx=50, pady=20)

            except Exception as e:
                self.status_label.config(text=f"Error getting names: {str(e)}")
            finally:
                self.random_button.config(state='normal', text="Random Name?")

        def rebuild_buttons_display():
            """Rebuild the buttons display with all generated names"""
            # Clear existing buttons but keep frames
            for btn in self.random_names_buttons:
                btn.destroy()
            self.random_names_buttons.clear()

            if not self.all_generated_names:
                return

            self.status_label.config(text="Choose one or click 'More Random' for new options:")

            # Pack persistent containers if not already packed
            if not self.grid_container.winfo_viewable():
                self.grid_container.pack(pady=10, padx=10, fill='x')
            if not self.more_button_container.winfo_viewable():
                self.more_button_container.pack(pady=10)

            # Create buttons in rows of 5 in the persistent grid container
            names_per_row = 5
            for i, name in enumerate(self.all_generated_names):
                row = i // names_per_row
                col = i % names_per_row

                btn = ttk.Button(self.grid_container, text=name, width=20,
                               command=lambda n=name: select_random_name(n))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
                self.random_names_buttons.append(btn)

            # Configure column weights for even distribution
            for col in range(names_per_row):
                self.grid_container.columnconfigure(col, weight=1)

            # Add more random button in persistent container
            more_button = ttk.Button(self.more_button_container, text="More Random Names", width=25,
                                   command=get_random_names)
            more_button.pack()
            self.random_names_buttons.append(more_button)

        def select_random_name(name):
            """Select a random name and put it in the entry field"""
            self.studio_name_var.set(name)
            self.random_frame.pack_forget()  # Hide the random names frame

        self.random_button.config(command=get_random_names)

        # Player name entry
        ttk.Label(content_frame, text="Your Name:", font=('Arial', 14, 'bold')).pack(pady=(40, 10))

        player_name_frame = ttk.Frame(content_frame)
        player_name_frame.pack(pady=10)

        self.player_name_var = tk.StringVar(value="Game Developer")
        player_name_entry = ttk.Entry(player_name_frame, textvariable=self.player_name_var, width=30, font=('Arial', 12))
        player_name_entry.pack(side='left', padx=10)

        # Player name generator button
        self.player_random_button = ttk.Button(player_name_frame, text="Random Name?", width=15)
        self.player_random_button.pack(side='left', padx=10)

        # Player random names frame (initially hidden)
        self.player_random_frame = ttk.LabelFrame(content_frame, text="Choose a Generated Player Name")
        self.player_random_names_buttons = []
        self.all_generated_player_names = []  # Keep track of all generated player names
        self.player_status_label = ttk.Label(self.player_random_frame, text="", font=('Arial', 10, 'italic'))
        self.player_status_label.pack(pady=10)

        # Create persistent frames for layout stability
        self.player_grid_container = ttk.Frame(self.player_random_frame)
        self.player_more_button_container = ttk.Frame(self.player_random_frame)

        def get_player_names():
            """Get random player names from DeepSeek"""
            self.player_random_button.config(state='disabled', text="Getting names...")
            self.player_status_label.config(text="Getting some names!")
            self.frame.update()

            try:
                names = get_random_player_names()  # Call the imported function

                # Add new names to all generated player names list
                self.all_generated_player_names.extend(names)

                # Rebuild the entire buttons display
                rebuild_player_buttons_display()

                # Show the frame
                self.player_random_frame.pack(fill='x', padx=50, pady=20)

            except Exception as e:
                self.player_status_label.config(text=f"Error getting names: {str(e)}")
            finally:
                self.player_random_button.config(state='normal', text="Random Name?")

        def rebuild_player_buttons_display():
            """Rebuild the player buttons display with all generated names"""
            # Clear existing buttons but keep frames
            for btn in self.player_random_names_buttons:
                btn.destroy()
            self.player_random_names_buttons.clear()

            if not self.all_generated_player_names:
                return

            self.player_status_label.config(text="Choose one or click 'More Random' for new options:")

            # Pack persistent containers if not already packed
            if not self.player_grid_container.winfo_viewable():
                self.player_grid_container.pack(pady=10, padx=10, fill='x')
            if not self.player_more_button_container.winfo_viewable():
                self.player_more_button_container.pack(pady=10)

            # Create buttons in rows of 5 in the persistent grid container
            names_per_row = 5
            for i, name in enumerate(self.all_generated_player_names):
                row = i // names_per_row
                col = i % names_per_row

                btn = ttk.Button(self.player_grid_container, text=name, width=20,
                               command=lambda n=name: select_random_player_name(n))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
                self.player_random_names_buttons.append(btn)

            # Configure column weights for even distribution
            for col in range(names_per_row):
                self.player_grid_container.columnconfigure(col, weight=1)

            # Add more random button in persistent container
            more_button = ttk.Button(self.player_more_button_container, text="More Random Names", width=25,
                                   command=get_player_names)
            more_button.pack()
            self.player_random_names_buttons.append(more_button)

        def select_random_player_name(name):
            """Select a random player name and put it in the entry field"""
            self.player_name_var.set(name)
            self.player_random_frame.pack_forget()  # Hide the random names frame

        self.player_random_button.config(command=get_player_names)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side='bottom', pady=30)

        ttk.Button(button_frame, text="Create Studio",
                  command=self.create_studio, width=15).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Back to Menu",
                  command=self.on_back, width=15).pack(side='left', padx=10)

    def create_studio(self):
        """Create new studio"""
        if not self.studio_name_var.get().strip():
            messagebox.showwarning("Invalid Name", "Please enter a studio name.")
            return

        if not self.player_name_var.get().strip():
            messagebox.showwarning("Invalid Name", "Please enter your name.")
            return

        # Call the create studio callback
        self.on_create_studio(
            self.studio_name_var.get().strip(),
            self.player_name_var.get().strip()
        )

    def open_player_name_generator(self):
        """Open player name generator window"""
        print("Player name generator button clicked!")  # Debug line
        # Create new window positioned above the main window
        name_window = tk.Toplevel(self.parent)
        name_window.title("Choose Player Name")
        name_window.geometry("500x600")
        name_window.transient(self.parent)
        name_window.grab_set()

        # Position window in center of main window
        main_x = self.parent.winfo_x()
        main_y = self.parent.winfo_y()
        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()

        # Calculate center position
        center_x = main_x + (main_width - 500) // 2
        center_y = main_y + (main_height - 600) // 2

        name_window.geometry(f"500x600+{center_x}+{center_y}")

        # Title
        ttk.Label(name_window, text="Choose Your Name", font=('Arial', 16, 'bold')).pack(pady=20)

        # Name entry section
        entry_frame = ttk.Frame(name_window)
        entry_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(entry_frame, text="ENTER NAME", font=('Arial', 12, 'bold')).pack()
        name_var = tk.StringVar(value=self.player_name_var.get())
        name_entry = ttk.Entry(entry_frame, textvariable=name_var, width=40, font=('Arial', 12))
        name_entry.pack(pady=10)

        # Random name button
        random_frame = ttk.Frame(name_window)
        random_frame.pack(pady=10)

        generate_button = ttk.Button(random_frame, text="GENERATE RANDOM NAMES", width=25,
                                   font=('Arial', 11, 'bold'))
        generate_button.pack()

        # Separator
        separator_frame = ttk.Frame(name_window)
        separator_frame.pack(fill='x', padx=20, pady=10)
        ttk.Separator(separator_frame, orient='horizontal').pack(fill='x')

        # Buttons section
        buttons_frame = ttk.Frame(name_window)
        buttons_frame.pack(fill='both', expand=True, padx=20, pady=10)

        ttk.Label(buttons_frame, text="BUTTONS", font=('Arial', 12, 'bold')).pack()

        # Scrollable frame for name buttons
        canvas = tk.Canvas(buttons_frame, height=300)
        scrollbar = ttk.Scrollbar(buttons_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        name_buttons = []

        def generate_names():
            """Generate and display random names"""
            generate_button.config(state='disabled', text="Calling AI...")
            name_window.update()

            try:
                names = get_random_player_names()

                # Clear existing buttons
                for btn in name_buttons:
                    btn.destroy()
                name_buttons.clear()

                # Create buttons for each name
                for i, name in enumerate(names):
                    btn = ttk.Button(scrollable_frame, text=name, width=35,
                                   command=lambda n=name: select_name(n))
                    btn.pack(pady=2, padx=10, fill='x')
                    name_buttons.append(btn)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate names: {str(e)}")
            finally:
                generate_button.config(state='normal', text="GENERATE RANDOM NAMES")

        def select_name(selected_name):
            """Select a name and put it in the entry field"""
            name_var.set(selected_name)

        def submit_name():
            """Submit the selected name"""
            if not name_var.get().strip():
                messagebox.showwarning("Invalid Name", "Please enter or select a name.")
                return

            self.player_name_var.set(name_var.get().strip())
            name_window.destroy()

        generate_button.config(command=generate_names)

        # Bottom separator and submit
        bottom_separator_frame = ttk.Frame(name_window)
        bottom_separator_frame.pack(fill='x', padx=20, pady=(10, 5))
        ttk.Separator(bottom_separator_frame, orient='horizontal').pack(fill='x')

        # Submit button
        submit_frame = ttk.Frame(name_window)
        submit_frame.pack(pady=15)

        ttk.Button(submit_frame, text="SUBMIT", command=submit_name, width=20,
                  style='Accent.TButton').pack()

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
        notebook.pack(fill='both', expand=True, padx=10, pady=(5, 10))

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
        info_frame.pack(fill='x', padx=10, pady=(5, 10))

        player_data = self.game_data.get('player_data')
        studio_stats = self.game_data.get('studio_stats')

        ttk.Label(info_frame, text=f"Studio: {player_data.get('studio_name', 'Unknown')}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Owner: {player_data.get('player_name', 'Unknown')}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Money: ${player_data.get('current_money', 0):,}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Reputation: {player_data.get('reputation', 0)}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Games Published: {studio_stats.get('games_published', 0)}").pack(anchor='w')

        # Skills frame
        skills_frame = ttk.LabelFrame(studio_frame, text="Skills")
        skills_frame.pack(fill='x', padx=10, pady=(5, 15))

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
                 font=('Arial', 16, 'bold')).pack(pady=(15, 10))

        # Current projects list
        current_projects = self.game_data.get('current_projects')
        if not current_projects:
            ttk.Label(projects_frame, text="No active projects",
                     font=('Arial', 12, 'italic')).pack(pady=(30, 20))

        # New project button
        ttk.Button(projects_frame, text="Start New Project",
                  command=self.start_new_project, width=20).pack(pady=15)

    def create_team_tab(self, notebook):
        """Create team tab"""
        team_frame = ttk.Frame(notebook)
        notebook.add(team_frame, text="Team")

        ttk.Label(team_frame, text="Team Members",
                 font=('Arial', 16, 'bold')).pack(pady=(15, 10))

        employees = self.game_data.get('employees')
        if not employees:
            ttk.Label(team_frame, text="No employees hired yet",
                     font=('Arial', 12, 'italic')).pack(pady=(30, 10))
            ttk.Label(team_frame, text="You are working solo for now!",
                     font=('Arial', 12)).pack()

        # Hire button
        ttk.Button(team_frame, text="Hire Employee",
                  command=self.hire_employee, width=20).pack(pady=20)

    def create_market_tab(self, notebook):
        """Create market tab"""
        market_frame = ttk.Frame(notebook)
        notebook.add(market_frame, text="Market")

        ttk.Label(market_frame, text="Game Market Analysis",
                 font=('Arial', 16, 'bold')).pack(pady=(15, 10))

        # Game types info
        game_types_frame = ttk.LabelFrame(market_frame, text="Available Game Types")
        game_types_frame.pack(fill='x', padx=10, pady=(10, 15))

        game_types = self.game_data.get('game_types', {})
        unlocked = game_types.get('unlocked', [])
        locked = game_types.get('locked', [])

        ttk.Label(game_types_frame, text="Unlocked Types:",
                 font=('Arial', 12, 'bold')).pack(anchor='w', pady=(5, 5))
        for game_type in unlocked:
            ttk.Label(game_types_frame, text=f"  • {game_type}", font=('Arial', 11)).pack(anchor='w')

        ttk.Label(game_types_frame, text="Locked Types:",
                 font=('Arial', 12, 'bold')).pack(anchor='w', pady=(15, 5))
        for game_type in locked:
            ttk.Label(game_types_frame, text=f"  • {game_type} (Requires research)", font=('Arial', 11)).pack(anchor='w')

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

        # Center the window on screen
        window_width = 1920
        window_height = 1080
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.minsize(800, 600)

        # Initialize managers and data
        self.save_manager = SaveManager()
        self.game_data = GameData()

        # Initialize UI components
        self.current_screen = None
        self.start_menu = StartMenu(self.root,
                                  self.show_new_game_screen,
                                  self.show_load_menu,
                                  self.show_options,
                                  self.quit_game,
                                  self.quick_start_game)

        self.load_menu = LoadGameMenu(self.root,
                                    self.save_manager,
                                    self.show_start_menu,
                                    self.load_game)

        self.new_game_screen = NewGameScreen(self.root,
                                           self.show_start_menu,
                                           self.create_new_studio)

        # Initialize development menu
        self.dev_menu = DevMenu(self)

        # Bind global hotkey for dev menu
        self.root.bind('<F12>', lambda e: self.dev_menu.show())

        # Show start menu
        self.show_start_menu()

    def show_start_menu(self):
        """Show the start menu"""
        self.clear_screen()
        self.start_menu.show()
        self.current_screen = "start"

    def show_new_game_screen(self):
        """Show the new game screen"""
        self.clear_screen()
        self.new_game_screen.show()
        self.current_screen = "new_game"

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

    def show_studio_room(self):
        """Show the studio room screen"""
        self.clear_screen()
        self.studio_room = StudioRoomScreen(self.root, self.game_data, self.show_start_menu)
        self.current_screen = "studio_room"

    def show_options(self):
        """Show options menu"""
        messagebox.showinfo("Options", "Options menu coming soon!")

    def clear_screen(self):
        """Clear all widgets from the main window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def quick_start_game(self):
        """Quick start a new game with default settings and companies"""
        # Generate random studio and player names
        import random

        # Default studio names
        default_studios = ["Pixel Studios", "Digital Dreams", "Code Masters", "Game Forge", "Bit Factory"]
        studio_name = random.choice(default_studios)

        # Default player names
        default_players = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Cameron", "Quinn"]
        player_name = random.choice(default_players)

        # Show loading screen
        self.clear_screen()
        loading_frame = tk.Frame(self.root, bg='#1a1a2e')
        loading_frame.pack(fill='both', expand=True)

        loading_label = tk.Label(loading_frame, text="Quick Start - Setting up your studio...",
                               font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='white')
        loading_label.pack(pady=200)

        info_label = tk.Label(loading_frame, text=f"Studio: {studio_name}\nPlayer: {player_name}",
                            font=('Arial', 12), bg='#1a1a2e', fg='#cccccc')
        info_label.pack(pady=10)

        status_label = tk.Label(loading_frame, text="Setting up default configuration...",
                              font=('Arial', 12), bg='#1a1a2e', fg='#888888')
        status_label.pack(pady=10)

        progress_label = tk.Label(loading_frame, text="",
                                font=('Arial', 11), bg='#1a1a2e', fg='#ffcc00')
        progress_label.pack(pady=5)

        # Update display
        self.root.update()

        # Create new game data
        progress_label.config(text="✓ Initializing game data...")
        self.root.update()
        self.game_data.reset_to_defaults()
        self.game_data.set(studio_name, 'player_data', 'studio_name')
        self.game_data.set(player_name, 'player_data', 'player_name')
        self.game_data.set("Normal", 'settings', 'difficulty')

        # Use default competitor companies
        status_label.config(text="Loading pre-configured competitor companies...")
        progress_label.config(text="(Quick Start uses cached companies)")
        self.root.update()

        print("Using default competitor companies (no API call)...")
        competitors = get_default_competitor_companies()
        self.game_data.data['competitors'] = {
            'companies': competitors,
            'generated_date': datetime.now().isoformat(),
            'is_default': True
        }

        # Update status
        status_label.config(text=f"✓ Loaded {len(competitors)} companies")
        progress_label.config(text="Ready to start!")
        self.root.update()
        print(f"Loaded {len(competitors)} default competitor companies")

        # Brief delay to show the message
        self.root.after(500, self.show_studio_room)

    def create_new_studio(self, studio_name, player_name):
        """Create new studio with provided data"""
        # Show loading screen
        self.clear_screen()
        loading_frame = tk.Frame(self.root, bg='#1a1a2e')
        loading_frame.pack(fill='both', expand=True)

        loading_label = tk.Label(loading_frame, text="Setting up your new studio...",
                               font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='white')
        loading_label.pack(pady=200)

        status_label = tk.Label(loading_frame, text="Generating competitor companies...",
                              font=('Arial', 12), bg='#1a1a2e', fg='#888888')
        status_label.pack(pady=10)

        # Progress indicator
        progress_label = tk.Label(loading_frame, text="",
                                font=('Arial', 11), bg='#1a1a2e', fg='#ffcc00')
        progress_label.pack(pady=5)

        # Update display
        self.root.update()

        # Create new game data
        progress_label.config(text="✓ Initializing game data...")
        self.root.update()
        self.game_data.reset_to_defaults()
        self.game_data.set(studio_name, 'player_data', 'studio_name')
        self.game_data.set(player_name, 'player_data', 'player_name')
        self.game_data.set("Normal", 'settings', 'difficulty')  # Default difficulty

        # Generate competitor companies
        status_label.config(text="Calling AI to generate unique competitor companies...")
        progress_label.config(text="This may take a moment...")
        self.root.update()

        print("Generating competitor companies via API...")
        competitors = get_competitor_companies()
        self.game_data.data['competitors'] = {
            'companies': competitors,
            'generated_date': datetime.now().isoformat()
        }

        # Update status
        status_label.config(text=f"✓ Created {len(competitors)} competitor companies")
        progress_label.config(text="Generating backstory and finalizing setup...")
        self.root.update()
        print(f"Created {len(competitors)} competitor companies")

        # Brief delay to show the message
        self.root.after(500, self.show_studio_room)

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

    def apply_dev_args(self, args):
        """Apply development command line arguments"""
        # Create a quick development game
        self.game_data.data = {
            'game_time': {
                'start_date': f'{args.year or 1984}-01-01',
                'current_date': f'{args.year or 1984}-01-01',
                'speed': 1
            },
            'player_data': {
                'studio_name': 'Dev Test Studio',
                'founder_name': 'Developer',
                'starting_funds': args.money or 1530,
                'starting_year': args.year or 1984,
                'difficulty': 'normal'
            },
            'money': {
                'cash_on_hand': 30,
                'bank_balance': (args.money or 1530) - 30,
                'monthly_rent': 150,
                'transaction_history': [],
                'recurring_expenses': [
                    {'name': 'Apartment Rent', 'amount': 150, 'day_of_month': 1}
                ],
                'last_rent_paid': None
            }
        }

        # Jump to specific development screen if requested
        if args.screen:
            self.jump_to_dev_screen(args.screen)
        else:
            # Just start normally with the dev data
            self.start_game()

    def jump_to_dev_screen(self, screen):
        """Jump directly to a development screen for testing"""
        # Start the game first
        self.start_game()

        # Then open the appropriate development screen
        if screen == 'planning' or screen == 'select-planner':
            # Open game engine and start development
            from desktop.development_stages import MultiStageDevelopment
            multi_stage = MultiStageDevelopment(
                self.root,
                self.game_data,
                "Test Game",
                "Action",
                "Sci-Fi"
            )
        # Add more screen options as needed

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Game Dev Studio Tycoon')
    parser.add_argument('--year', type=int, default=None, help='Start year (e.g., 1978)')
    parser.add_argument('--money', type=int, default=None, help='Starting money amount')
    parser.add_argument('--screen', type=str, default=None,
                       choices=['planning', 'select-planner', 'development', 'production', 'bug-squashing'],
                       help='Jump to specific screen for development')
    parser.add_argument('--dev', action='store_true', help='Enable developer menu')

    args = parser.parse_args()

    app = GameDevStudioApp()

    # Apply development arguments if provided
    if args.year or args.money or args.screen:
        app.apply_dev_args(args)

    app.run()