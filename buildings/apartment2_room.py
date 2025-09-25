import tkinter as tk
from tkinter import Canvas, messagebox, ttk
import math
from systems.game_systems import TimeSystem, EnergySystem, SleepSchedule, HygieneSystem, HappinessSystem
from buildings.base_room import BaseRoom
from desktop.desktop_system import DesktopScreen

class ApartmentRoom2(BaseRoom):
    """Two bedroom apartment with 3 desks (2 for NPCs)"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)

        # Room dimensions (larger than studio)
        self.room_width = 600
        self.room_height = 400

        # Player position and properties
        self.player_x = 300
        self.player_y = 200
        self.player_radius = 10
        self.player_speed = 3

        # Target position for movement
        self.target_x = self.player_x
        self.target_y = self.player_y
        self.is_moving = False

        # Furniture items for interaction
        self.furniture_items = {}

        # Station tracking for collision system
        self.current_station = None
        self.station_names = ['bedroom1', 'bedroom2', 'player_desk', 'npc_desk1', 'npc_desk2', 'bathroom', 'kitchen']

        # Initialize game systems
        self.time_system = TimeSystem(game_data)
        self.energy_system = EnergySystem(game_data)
        self.hygiene_system = HygieneSystem(game_data)
        self.happiness_system = HappinessSystem(game_data)

        self.setup_ui()
        self.draw_room()
        self.start_game_loop()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#2a2a2a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Apartment info frame
        info_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        info_frame.pack(pady=10)

        studio_name = self.game_data.data['player_data']['studio_name']
        player_name = self.game_data.data['player_data']['player_name']

        tk.Label(info_frame, text="Two Bedroom Apartment", font=('Arial', 18, 'bold'),
                bg='#2a2a2a', fg='white').pack()
        tk.Label(info_frame, text=f"Studio: {studio_name} | Player: {player_name}", font=('Arial', 12),
                bg='#2a2a2a', fg='white').pack()

        # Status display frame
        status_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        status_frame.pack(pady=5, fill='x')

        # Time display (left)
        self.time_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                  bg='#2a2a2a', fg='#90EE90')
        self.time_label.pack(side='left', padx=20)

        # Energy display
        self.energy_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                    bg='#2a2a2a', fg='white')
        self.energy_label.pack(side='left', padx=10)

        # Hygiene display
        self.hygiene_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                     bg='#2a2a2a', fg='white')
        self.hygiene_label.pack(side='left', padx=10)

        # Happiness display
        self.happiness_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                       bg='#2a2a2a', fg='white')
        self.happiness_label.pack(side='left', padx=10)

        # Speed control button (right)
        self.speed_button = tk.Button(status_frame, text="⏩ 1x",
                                     command=self.cycle_speed,
                                     font=('Arial', 12, 'bold'), bg='#444', fg='white',
                                     padx=15, pady=5)
        self.speed_button.pack(side='right', padx=20)

        self.update_status_display()

        # Canvas for room
        self.canvas = Canvas(self.main_frame, width=self.room_width, height=self.room_height,
                           bg='#4a4a4a', highlightthickness=3, highlightbackground='#333')
        self.canvas.pack(pady=10)

        # Bind mouse click for movement
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Bind keyboard events
        self.root.bind('<KeyPress>', self.on_key_press)

        # Action buttons frame
        button_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        button_frame.pack(pady=10)

        # Back button
        tk.Button(button_frame, text="Back to Menu", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(side='left', padx=5)

    def draw_room(self):
        """Draw the two bedroom apartment layout"""
        self.canvas.delete("all")

        # Draw floor
        self.canvas.create_rectangle(0, 0, self.room_width, self.room_height,
                                    fill='#8B7355', outline='#654321', width=3)

        # Draw walls between rooms
        # Vertical wall separating bedrooms from main area
        self.canvas.create_line(200, 0, 200, self.room_height, fill='#654321', width=4)
        # Horizontal wall separating two bedrooms
        self.canvas.create_line(0, 200, 200, 200, fill='#654321', width=4)

        # Bedroom 1 (top left)
        bed1 = self.canvas.create_rectangle(20, 30, 100, 120, fill='#4169E1', outline='#000080', width=2)
        self.canvas.create_text(60, 75, text="Bed 1", fill='white', font=('Arial', 10, 'bold'))
        self.furniture_items['bedroom1'] = bed1

        # Bedroom 2 (bottom left)
        bed2 = self.canvas.create_rectangle(20, 230, 100, 320, fill='#4169E1', outline='#000080', width=2)
        self.canvas.create_text(60, 275, text="Bed 2", fill='white', font=('Arial', 10, 'bold'))
        self.furniture_items['bedroom2'] = bed2

        # Player desk (center)
        player_desk = self.canvas.create_rectangle(250, 150, 350, 200, fill='#8B4513', outline='#654321', width=2)
        self.canvas.create_text(300, 175, text="Your Desk", fill='white', font=('Arial', 10, 'bold'))
        self.furniture_items['player_desk'] = player_desk

        # NPC Desk 1 (top right)
        npc_desk1 = self.canvas.create_rectangle(450, 50, 550, 100, fill='#696969', outline='#2F4F4F', width=2)
        self.canvas.create_text(500, 75, text="NPC Desk 1", fill='white', font=('Arial', 10, 'bold'))
        self.furniture_items['npc_desk1'] = npc_desk1

        # NPC Desk 2 (middle right)
        npc_desk2 = self.canvas.create_rectangle(450, 150, 550, 200, fill='#696969', outline='#2F4F4F', width=2)
        self.canvas.create_text(500, 175, text="NPC Desk 2", fill='white', font=('Arial', 10, 'bold'))
        self.furniture_items['npc_desk2'] = npc_desk2

        # Bathroom (bottom center)
        bathroom = self.canvas.create_rectangle(250, 320, 350, 380, fill='#87CEEB', outline='#4682B4', width=2)
        self.canvas.create_text(300, 350, text="Bathroom", fill='black', font=('Arial', 10, 'bold'))
        self.furniture_items['bathroom'] = bathroom

        # Kitchen area (bottom right)
        kitchen = self.canvas.create_rectangle(450, 300, 580, 380, fill='#FFD700', outline='#B8860B', width=2)
        self.canvas.create_text(515, 340, text="Kitchen", fill='black', font=('Arial', 10, 'bold'))
        self.furniture_items['kitchen'] = kitchen

        # Draw player
        self.player_sprite = self.canvas.create_oval(
            self.player_x - self.player_radius, self.player_y - self.player_radius,
            self.player_x + self.player_radius, self.player_y + self.player_radius,
            fill='#90EE90', outline='#228B22', width=2
        )

    def on_canvas_click(self, event):
        """Handle mouse click for movement"""
        self.target_x = event.x
        self.target_y = event.y
        self.is_moving = True

    def on_key_press(self, event):
        """Handle keyboard input"""
        if event.keysym == 'space':
            self.interact_with_station()
        elif event.keysym in ['1', '2', '3', '4']:
            speed_map = {'1': 1, '2': 2, '3': 5, '4': 10}
            self.time_system.set_speed(speed_map[event.keysym])
            self.update_speed_button()

    def interact_with_station(self):
        """Handle interaction with furniture when space is pressed"""
        if not self.current_station:
            return

        if self.current_station == 'player_desk':
            # Open desktop system
            self.open_desktop()
        elif self.current_station == 'bedroom1':
            # Sleep in bedroom 1
            self.sleep_action()
        elif self.current_station == 'bedroom2':
            # Sleep in bedroom 2
            self.sleep_action()
        elif self.current_station == 'bathroom':
            # Use bathroom
            self.shower_action()
        elif self.current_station == 'kitchen':
            # Use kitchen
            self.eat_action()
        elif self.current_station in ['npc_desk1', 'npc_desk2']:
            messagebox.showinfo("NPC Desk", "This desk belongs to an NPC")

    def open_desktop(self):
        """Open the desktop system"""
        # Clear the current UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create desktop screen
        desktop = DesktopScreen(
            self.root,
            self.game_data,
            on_back=lambda: self.__init__(self.root, self.game_data, self.on_back)
        )

    def sleep_action(self):
        """Handle sleep action"""
        sleep_schedule = SleepSchedule(self.game_data)
        hours_slept = sleep_schedule.execute_sleep(self.time_system)

        if hours_slept > 0:
            messagebox.showinfo("Sleep", f"You slept for {hours_slept} hours and recovered energy!")
            self.update_status_display()

    def shower_action(self):
        """Handle shower action"""
        current_hygiene = self.game_data.data['player_data']['hygiene']
        if current_hygiene >= 95:
            messagebox.showinfo("Bathroom", "You're already clean!")
        else:
            self.hygiene_system.take_shower(self.time_system)
            messagebox.showinfo("Bathroom", "You feel refreshed after using the bathroom!")
            self.update_status_display()

    def eat_action(self):
        """Handle eat action"""
        current_energy = self.game_data.data['player_data']['energy']
        if current_energy >= 90:
            messagebox.showinfo("Kitchen", "You're not hungry right now")
        else:
            # Restore some energy
            new_energy = min(100, current_energy + 20)
            self.game_data.data['player_data']['energy'] = new_energy
            self.game_data.save_game()

            # Advance time by 30 minutes
            self.time_system.advance_minutes(30)

            messagebox.showinfo("Kitchen", "You had a meal and feel energized!")
            self.update_status_display()

    def update_player_position(self):
        """Update player movement towards target"""
        if not self.is_moving:
            return

        # Calculate distance to target
        dx = self.target_x - self.player_x
        dy = self.target_y - self.player_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.player_speed:
            # Reached target
            self.player_x = self.target_x
            self.player_y = self.target_y
            self.is_moving = False
        else:
            # Move towards target
            self.player_x += (dx / distance) * self.player_speed
            self.player_y += (dy / distance) * self.player_speed

        # Update player sprite
        self.canvas.coords(self.player_sprite,
                          self.player_x - self.player_radius, self.player_y - self.player_radius,
                          self.player_x + self.player_radius, self.player_y + self.player_radius)

        # Check collisions
        self.check_collisions()

    def check_collisions(self):
        """Check if player is near any interactive furniture"""
        old_station = self.current_station
        self.current_station = None

        for station_name, item_id in self.furniture_items.items():
            bbox = self.canvas.bbox(item_id)
            if bbox:
                x1, y1, x2, y2 = bbox
                # Add proximity margin
                margin = 20
                if (x1 - margin <= self.player_x <= x2 + margin and
                    y1 - margin <= self.player_y <= y2 + margin):
                    self.current_station = station_name
                    break

        # Show interaction hint if near a station
        if self.current_station != old_station:
            if self.current_station:
                self.show_interaction_hint()
            else:
                self.hide_interaction_hint()

    def show_interaction_hint(self):
        """Show hint when near interactive object"""
        self.canvas.delete("hint")
        hint_text = f"Press SPACE to interact with {self.current_station.replace('_', ' ')}"
        self.canvas.create_text(self.room_width // 2, 20, text=hint_text,
                               fill='yellow', font=('Arial', 11, 'bold'), tags="hint")

    def hide_interaction_hint(self):
        """Hide interaction hint"""
        self.canvas.delete("hint")

    def update_status_display(self):
        """Update all status displays"""
        # Update time
        time_str = self.time_system.get_display_string()
        self.time_label.config(text=time_str)

        # Update energy with color coding
        energy = self.energy_system.get_energy()
        energy_color = self.energy_system.get_energy_color()
        self.energy_label.config(text=f"Energy: {energy}%", fg=energy_color)

        # Update hygiene with color coding
        hygiene = self.hygiene_system.get_hygiene()
        hygiene_color = self.hygiene_system.get_hygiene_color()
        self.hygiene_label.config(text=f"Hygiene: {hygiene}%", fg=hygiene_color)

        # Update happiness with color coding
        happiness = self.happiness_system.get_happiness()
        happiness_color = self.happiness_system.get_happiness_color()
        self.happiness_label.config(text=f"Happiness: {happiness}%", fg=happiness_color)

    def cycle_speed(self):
        """Cycle through time speed settings"""
        current_speed = self.time_system.speed_multiplier
        if current_speed == 1:
            self.time_system.set_speed(2)
        elif current_speed == 2:
            self.time_system.set_speed(5)
        elif current_speed == 5:
            self.time_system.set_speed(10)
        else:
            self.time_system.set_speed(1)
        self.update_speed_button()

    def update_speed_button(self):
        """Update speed button display"""
        speed = self.time_system.speed_multiplier
        self.speed_button.config(text=f"⏩ {speed}x")

    def start_game_loop(self):
        """Start the main game update loop"""
        self.update_game_state()

    def update_game_state(self):
        """Main game state update"""
        # Update time
        self.time_system.update()

        # Update energy
        self.energy_system.update(self.time_system)

        # Update hygiene
        self.hygiene_system.update(self.time_system)

        # Update happiness
        self.happiness_system.update(self.time_system, self.energy_system, self.hygiene_system)

        # Update player movement
        self.update_player_position()

        # Update displays
        self.update_status_display()

        # Schedule next update (60 FPS)
        self.root.after(16, self.update_game_state)