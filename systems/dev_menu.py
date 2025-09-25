import tkinter as tk
from tkinter import ttk, messagebox

class DevMenu:
    def __init__(self, app):
        self.app = app
        self.window = None

    def show(self):
        """Show the development menu"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.app.root)
        self.window.title("Development Menu")
        self.window.geometry("400x500")

        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 200
        y = (self.window.winfo_screenheight() // 2) - 250
        self.window.geometry(f"400x500+{x}+{y}")

        # Title
        title_label = tk.Label(self.window, text="DEVELOPMENT MENU",
                              font=('Arial', 16, 'bold'), fg='red')
        title_label.pack(pady=10)

        # Warning
        warning_label = tk.Label(self.window, text="Debug tools - May break game state!",
                                font=('Arial', 10, 'italic'), fg='orange')
        warning_label.pack()

        # Separator
        ttk.Separator(self.window, orient='horizontal').pack(fill='x', pady=10)

        # Quick Start Section
        quick_frame = ttk.LabelFrame(self.window, text="Quick Start", padding=10)
        quick_frame.pack(fill='x', padx=20, pady=10)

        tk.Button(quick_frame, text="Skip to Studio Room\n(Test Game Studio/Test Game Player)",
                 command=self.skip_to_studio_room,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                 padx=10, pady=10, wraplength=200).pack(pady=5)

        tk.Button(quick_frame, text="TEST: PLANNING\n(Test Bouncing & Summary Screen)",
                 command=self.test_planning_stage,
                 bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                 padx=10, pady=10, wraplength=200).pack(pady=5)

        # Game State Section
        state_frame = ttk.LabelFrame(self.window, text="Game State", padding=10)
        state_frame.pack(fill='x', padx=20, pady=10)

        tk.Button(state_frame, text="Add $10,000",
                 command=lambda: self.add_money(10000),
                 bg='#2196F3', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(pady=2)

        tk.Button(state_frame, text="Set Energy to 100%",
                 command=self.max_energy,
                 bg='#2196F3', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(pady=2)

        tk.Button(state_frame, text="Add 5 Energy Drinks",
                 command=self.add_energy_drinks,
                 bg='#2196F3', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(pady=2)

        tk.Button(state_frame, text="Reset Stress to 0",
                 command=self.reset_stress,
                 bg='#2196F3', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(pady=2)

        # Time Control Section
        time_frame = ttk.LabelFrame(self.window, text="Time Control", padding=10)
        time_frame.pack(fill='x', padx=20, pady=10)

        # Time skip buttons
        skip_frame = tk.Frame(time_frame)
        skip_frame.pack(fill='x', pady=5)

        tk.Button(skip_frame, text="Skip 1 Hour",
                 command=lambda: self.skip_time(1),
                 bg='#FF9800', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(side='left', padx=2)

        tk.Button(skip_frame, text="Skip 1 Day",
                 command=lambda: self.skip_time(24),
                 bg='#FF9800', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(side='left', padx=2)

        tk.Button(skip_frame, text="Skip 1 Week",
                 command=lambda: self.skip_time(168),
                 bg='#FF9800', fg='white', font=('Arial', 10),
                 padx=10, pady=5).pack(side='left', padx=2)

        # Time speed controls
        speed_frame = tk.Frame(time_frame)
        speed_frame.pack(fill='x', pady=5)

        tk.Label(speed_frame, text="Time Speed:", font=('Arial', 10)).pack(side='left', padx=5)

        # Row 1 of speed buttons
        speed_row1 = tk.Frame(speed_frame)
        speed_row1.pack(side='left')

        tk.Button(speed_row1, text="Real-time (1:1)",
                 command=lambda: self.set_time_speed(1),
                 bg='#4CAF50', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        tk.Button(speed_row1, text="Quick Day",
                 command=lambda: self.set_time_speed(960),
                 bg='#2196F3', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        tk.Button(speed_row1, text="Quick Week",
                 command=lambda: self.set_time_speed(6720),
                 bg='#FF9800', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        # Row 2 of speed buttons
        speed_row2 = tk.Frame(time_frame)
        speed_row2.pack(fill='x', pady=2)

        tk.Label(speed_row2, text="      ", font=('Arial', 10)).pack(side='left', padx=5)

        tk.Button(speed_row2, text="Quick Month",
                 command=lambda: self.set_time_speed(25920),
                 bg='#9C27B0', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        tk.Button(speed_row2, text="Quick Quarter",
                 command=lambda: self.set_time_speed(64800),
                 bg='#E91E63', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        tk.Button(speed_row2, text="MAX (x55000)",
                 command=lambda: self.set_time_speed(55000),
                 bg='#F44336', fg='white', font=('Arial', 9),
                 padx=8, pady=3).pack(side='left', padx=2)

        # Info Display
        info_frame = ttk.LabelFrame(self.window, text="Current State", padding=10)
        info_frame.pack(fill='x', padx=20, pady=10)

        self.info_text = tk.Text(info_frame, height=5, width=40, font=('Courier', 9))
        self.info_text.pack()
        self.update_info()

        # Close button
        tk.Button(self.window, text="Close", command=self.window.destroy,
                 bg='#555', fg='white', font=('Arial', 10),
                 padx=20, pady=5).pack(pady=10)

        # Make sure window stays on top
        self.window.attributes('-topmost', True)

    def skip_to_studio_room(self):
        """Skip intro and go directly to studio room with test data"""
        # Set test data
        self.app.game_data.reset_to_defaults()
        self.app.game_data.set("Test Game Studio", 'player_data', 'studio_name')
        self.app.game_data.set("Test Game Player", 'player_data', 'player_name')
        self.app.game_data.set("Normal", 'settings', 'difficulty')

        # Close dev menu
        if self.window:
            self.window.destroy()

        # Go to studio room
        self.app.show_studio_room()

        messagebox.showinfo("Dev Mode", "Skipped to Studio Room with test data!")

    def test_planning_stage(self):
        """Launch the planning stage directly for testing"""
        from desktop.development_stages import DevelopmentStageWindow, DevelopmentStage

        # Setup test game data
        if 'current_game' not in self.app.game_data.data:
            self.app.game_data.data['current_game'] = {}

        # Set test game info
        self.app.game_data.data['current_game']['name'] = "Test Game"
        self.app.game_data.data['current_game']['type'] = "Action"
        self.app.game_data.data['current_game']['topic'] = "Space"

        # Close dev menu
        if self.window:
            self.window.destroy()

        # Create and show planning stage window
        planning_window = DevelopmentStageWindow(
            self.app.root,
            self.app.game_data,  # Pass the game_data object, not .data
            DevelopmentStage.PLANNING,
            "Test Player",
            None,  # Will use default developer stats
            on_complete=lambda: messagebox.showinfo("Test Complete", "Planning stage test completed!")
        )

        messagebox.showinfo("Dev Mode", "Launching Planning Stage Test!\nClick space to bounce the developer.")

    def add_money(self, amount):
        """Add money to player"""
        current = self.app.game_data.data['player_data'].get('current_money', 0)
        self.app.game_data.data['player_data']['current_money'] = current + amount
        self.update_info()
        messagebox.showinfo("Dev Mode", f"Added ${amount}!")

    def max_energy(self):
        """Set energy to maximum"""
        if 'energy_system' in self.app.game_data.data:
            self.app.game_data.data['energy_system']['current_energy'] = 100
        else:
            self.app.game_data.data['player_data']['energy'] = 100
        self.update_info()
        messagebox.showinfo("Dev Mode", "Energy set to 100%!")

    def add_energy_drinks(self):
        """Add energy drinks"""
        if 'energy_system' not in self.app.game_data.data:
            self.app.game_data.data['energy_system'] = {
                'current_energy': 100,
                'max_energy': 100,
                'energy_drinks': 5,
                'adderall': 0,
                'adderall_cooldown': 0,
                'caffeine_tolerance': 0
            }
        else:
            current = self.app.game_data.data['energy_system'].get('energy_drinks', 0)
            self.app.game_data.data['energy_system']['energy_drinks'] = current + 5
        self.update_info()
        messagebox.showinfo("Dev Mode", "Added 5 energy drinks!")

    def reset_stress(self):
        """Reset stress to 0"""
        self.app.game_data.data['player_data']['stress_level'] = 0
        self.update_info()
        messagebox.showinfo("Dev Mode", "Stress reset to 0!")

    def set_time_speed(self, speed):
        """Set the time speed multiplier"""
        try:
            # Access the time system if it exists in the current screen
            if hasattr(self.app, 'studio_room'):
                self.app.studio_room.time_system.time_scale = speed
                messagebox.showinfo("Dev Mode", f"Time speed set to x{speed}")

                # Calculate real-time to game-time
                if speed == 1:
                    info = "Real-time (1:1)"
                elif speed == 960:
                    info = "1 day per 90 seconds"
                elif speed == 6720:
                    info = "1 week per 90 seconds"
                elif speed == 25920:
                    info = "1 month per 100 seconds"
                elif speed == 64800:
                    info = "3 months per 120 seconds"
                elif speed == 55000:
                    info = "Maximum speed (1 year ~10 minutes)"
                else:
                    info = f"x{speed} speed"

                messagebox.showinfo("Time Speed", f"Time now moves at {info}")
            else:
                # Set it in game data for when studio room loads
                if 'time' not in self.app.game_data.data:
                    self.app.game_data.data['time'] = {}
                self.app.game_data.data['time']['time_scale'] = speed
                messagebox.showinfo("Dev Mode", f"Time speed will be x{speed} when game starts")
        except Exception as e:
            messagebox.showerror("Error", f"Could not set time speed: {e}")

    def skip_time(self, hours):
        """Skip time by specified hours"""
        if 'time' not in self.app.game_data.data:
            self.app.game_data.data['time'] = {
                'current_hour': 8,
                'current_day': 1,
                'current_week': 1,
                'current_month': 1,
                'total_days': 0,
                'sleep_schedule': 'Normal',
                'crunch_weeks': 0,
                'hours_worked_today': 0,
                'breaks_taken_today': 0
            }

        from game_systems import TimeSystem
        time_system = TimeSystem(self.app.game_data)
        time_system.advance_time(hours)
        self.update_info()

        if hours == 1:
            messagebox.showinfo("Dev Mode", "Skipped 1 hour!")
        elif hours == 24:
            messagebox.showinfo("Dev Mode", "Skipped 1 day!")
        else:
            messagebox.showinfo("Dev Mode", "Skipped 1 week!")

    def update_info(self):
        """Update the info display"""
        if not self.window or not self.window.winfo_exists():
            return

        info = []

        # Player data
        player_data = self.app.game_data.data.get('player_data', {})
        info.append(f"Studio: {player_data.get('studio_name', 'None')}")
        info.append(f"Player: {player_data.get('player_name', 'None')}")
        info.append(f"Money: ${player_data.get('current_money', 0)}")

        # Energy
        if 'energy_system' in self.app.game_data.data:
            energy = self.app.game_data.data['energy_system'].get('current_energy', 100)
        else:
            energy = player_data.get('energy', 100)
        info.append(f"Energy: {energy}%")

        # Stress
        stress = player_data.get('stress_level', 0)
        info.append(f"Stress: {stress}")

        # Time
        if 'time' in self.app.game_data.data:
            time_data = self.app.game_data.data['time']
            info.append(f"Day {time_data.get('current_day', 1)}, Hour {time_data.get('current_hour', 8)}")

        # Update text widget
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, '\n'.join(info))