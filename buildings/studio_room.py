import tkinter as tk
from tkinter import Canvas, messagebox, ttk
import math
from game_systems import TimeSystem, EnergySystem, SleepSchedule

class StudioRoomScreen:
    def __init__(self, root, game_data, on_back=None):
        self.root = root
        self.game_data = game_data
        self.on_back = on_back

        # Room dimensions (4x smaller - cramped)
        self.room_width = 400
        self.room_height = 300

        # Player position and properties
        self.player_x = 200
        self.player_y = 150
        self.player_radius = 10
        self.player_speed = 2

        # Target position for movement
        self.target_x = self.player_x
        self.target_y = self.player_y
        self.is_moving = False

        # Furniture items for interaction
        self.furniture_items = {}

        # Station tracking for collision system
        self.current_station = None
        self.station_names = ['bed', 'desk', 'shower', 'fridge', 'microwave']

        # Initialize game systems
        self.time_system = TimeSystem(game_data)
        self.energy_system = EnergySystem(game_data)

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

        # Studio info frame
        info_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        info_frame.pack(pady=10)

        studio_name = self.game_data.data['player_data']['studio_name']
        player_name = self.game_data.data['player_data']['player_name']

        tk.Label(info_frame, text=studio_name, font=('Arial', 18, 'bold'),
                bg='#2a2a2a', fg='white').pack()
        tk.Label(info_frame, text=f"Player: {player_name}", font=('Arial', 12),
                bg='#2a2a2a', fg='white').pack()

        # Status display frame
        status_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        status_frame.pack(pady=5, fill='x')

        # Time display (left)
        self.time_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                  bg='#2a2a2a', fg='#90EE90')
        self.time_label.pack(side='left', padx=20)

        # Energy display (center)
        self.energy_label = tk.Label(status_frame, text="", font=('Arial', 11, 'bold'),
                                    bg='#2a2a2a', fg='white')
        self.energy_label.pack(side='left', padx=20)

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
        self.canvas.pack(pady=20)

        # Controls hint
        controls_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        controls_frame.pack()
        tk.Label(controls_frame, text="Click to move | Click on bed to sleep",
                font=('Arial', 10), bg='#2a2a2a', fg='white').pack()

        # Back button
        tk.Button(self.main_frame, text="Back to Menu", command=self.back_to_menu,
                 font=('Arial', 10), bg='#555', fg='white', padx=20, pady=5).pack(pady=10)

        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def draw_room(self):
        # Clear canvas
        self.canvas.delete("all")

        # Draw floor
        self.canvas.create_rectangle(0, 0, self.room_width, self.room_height,
                                    fill='#5a5a5a', outline='#333', width=2)

        # Draw front door (bottom center)
        door_x = self.room_width // 2 - 20
        door_y = self.room_height - 40
        door_width = 40
        door_height = 40

        # Door frame
        self.canvas.create_rectangle(door_x, door_y, door_x + door_width, door_y + door_height,
                                    fill='#8B4513', outline='#654321', width=3, tags="door")
        # Door
        self.canvas.create_rectangle(door_x + 5, door_y + 5, door_x + door_width - 5, door_y + door_height - 10,
                                    fill='#A0522D', outline='#654321', width=2, tags="door")
        # Door handle
        self.canvas.create_oval(door_x + door_width - 20, door_y + 35, door_x + door_width - 10, door_y + 45,
                              fill='#FFD700', outline='#B8860B', tags="door")

        self.furniture_items['door'] = {
            'x': door_x, 'y': door_y,
            'width': door_width, 'height': door_height
        }

        # Draw bed (top left) - store as clickable item
        bed_x, bed_y = 10, 10
        bed_width, bed_height = 60, 80
        # Mattress
        bed_id = self.canvas.create_rectangle(bed_x, bed_y, bed_x + bed_width, bed_y + bed_height,
                                    fill='#8B4513', outline='#654321', width=2, tags="bed")
        # Pillow
        pillow_id = self.canvas.create_rectangle(bed_x + 5, bed_y + 5, bed_x + bed_width - 5, bed_y + 25,
                                    fill='#D2B48C', outline='#A0522D', tags="bed")

        # Get current sleep schedule
        schedule = self.game_data.data.get('time', {}).get('sleep_schedule', 'Normal')
        schedule_text = schedule.replace("Crunch Time", "Crunch")  # Shorten for display

        # Add text on pillow showing sleep schedule
        self.pillow_text = self.canvas.create_text(bed_x + bed_width//2, bed_y + 15,
                                                   text=schedule_text,
                                                   font=('Arial', 8, 'bold'),
                                                   fill='#654321',
                                                   tags="bed")

        # Store bed info for interaction
        self.furniture_items['bed'] = {
            'x': bed_x, 'y': bed_y,
            'width': bed_width, 'height': bed_height,
            'ids': [bed_id, pillow_id, self.pillow_text]
        }

        # Draw desk (top right)
        desk_x, desk_y = self.room_width - 80, 10
        desk_width, desk_height = 70, 50
        # Desk surface
        self.canvas.create_rectangle(desk_x, desk_y, desk_x + desk_width, desk_y + desk_height,
                                    fill='#654321', outline='#4a3218', width=2)
        # Monitor
        monitor_width, monitor_height = 30, 20
        monitor_x = desk_x + (desk_width - monitor_width) // 2
        self.canvas.create_rectangle(monitor_x, desk_y + 5, monitor_x + monitor_width, desk_y + 25,
                                    fill='#333', outline='#222', width=3)
        # Monitor stand
        self.canvas.create_rectangle(monitor_x + 12, desk_y + 25, monitor_x + 18, desk_y + 30,
                                    fill='#222', outline='#111')
        # Desk label
        self.canvas.create_text(desk_x + desk_width//2, desk_y + desk_height + 5,
                               text="DESK", font=('Arial', 6), fill='#999')

        # Draw shower (bottom left)
        shower_x, shower_y = 10, self.room_height - 80
        shower_width, shower_height = 50, 60
        # Shower base
        self.canvas.create_rectangle(shower_x, shower_y, shower_x + shower_width, shower_y + shower_height,
                                    fill='#87CEEB', outline='#4682B4', width=2)
        # Shower head
        self.canvas.create_oval(shower_x + 15, shower_y + 5, shower_x + 35, shower_y + 20,
                               fill='#C0C0C0', outline='#808080')
        # Shower door (glass effect)
        self.canvas.create_rectangle(shower_x + 3, shower_y + 25, shower_x + shower_width - 3, shower_y + shower_height - 3,
                                    fill='#B0E0E6', outline='#4682B4', stipple='gray50')
        # Shower label
        self.canvas.create_text(shower_x + shower_width//2, shower_y + shower_height + 5,
                               text="SHOWER", font=('Arial', 6), fill='#999')

        # Draw fridge (bottom right)
        fridge_x, fridge_y = self.room_width - 100, self.room_height - 90
        fridge_width, fridge_height = 40, 70
        # Fridge body
        self.canvas.create_rectangle(fridge_x, fridge_y, fridge_x + fridge_width, fridge_y + fridge_height,
                                    fill='#D3D3D3', outline='#A9A9A9', width=2)
        # Fridge door line
        self.canvas.create_line(fridge_x, fridge_y + 40, fridge_x + fridge_width, fridge_y + 40,
                               fill='#A9A9A9', width=2)
        # Handle
        self.canvas.create_rectangle(fridge_x + fridge_width - 10, fridge_y + 10,
                                    fridge_x + fridge_width - 5, fridge_y + 25,
                                    fill='#696969', outline='#4a4a4a')
        # Fridge label (on the fridge)
        self.canvas.create_text(fridge_x + fridge_width//2, fridge_y + fridge_height//2,
                               text="FRIDGE", font=('Arial', 6), fill='#555')

        # Draw microwave (near fridge)
        microwave_x, microwave_y = self.room_width - 50, self.room_height - 110
        microwave_width, microwave_height = 35, 20
        # Microwave body
        self.canvas.create_rectangle(microwave_x, microwave_y, microwave_x + microwave_width,
                                    microwave_y + microwave_height,
                                    fill='#2F4F4F', outline='#1C1C1C', width=2)
        # Microwave door
        self.canvas.create_rectangle(microwave_x + 2, microwave_y + 2,
                                    microwave_x + microwave_width - 8, microwave_y + microwave_height - 2,
                                    fill='#1C1C1C', outline='#000')
        # Control panel
        self.canvas.create_rectangle(microwave_x + microwave_width - 6, microwave_y + 2,
                                    microwave_x + microwave_width - 2, microwave_y + microwave_height - 2,
                                    fill='#4a4a4a', outline='#2a2a2a')
        # Microwave label
        self.canvas.create_text(microwave_x + microwave_width//2, microwave_y + microwave_height + 4,
                               text="MW", font=('Arial', 6), fill='#999')

        # Draw player (red circle) - drawn last to appear on top
        self.player_obj = self.canvas.create_oval(
            self.player_x - self.player_radius, self.player_y - self.player_radius,
            self.player_x + self.player_radius, self.player_y + self.player_radius,
            fill='#ff0000', outline='#cc0000', width=2
        )

    def on_canvas_click(self, event):
        """Handle canvas clicks for movement and interaction"""
        click_x, click_y = event.x, event.y

        # Check if click is on bed
        bed = self.furniture_items['bed']
        if (bed['x'] <= click_x <= bed['x'] + bed['width'] and
            bed['y'] <= click_y <= bed['y'] + bed['height']):
            self.sleep_in_bed()
            return

        # Otherwise, set as movement target
        self.target_x = click_x
        self.target_y = click_y
        self.is_moving = True

    def sleep_in_bed(self):
        """Handle sleeping in bed with schedule selection"""
        # Create sleep dialog
        sleep_window = tk.Toplevel(self.root)
        sleep_window.title("Sleep Options")
        sleep_window.geometry("600x500")
        sleep_window.transient(self.root)
        sleep_window.grab_set()

        # Center the window
        sleep_window.update_idletasks()
        x = (sleep_window.winfo_screenwidth() // 2) - (300)
        y = (sleep_window.winfo_screenheight() // 2) - (250)
        sleep_window.geometry(f"600x500+{x}+{y}")

        # Title
        tk.Label(sleep_window, text="Choose Sleep Schedule", font=('Arial', 18, 'bold')).pack(pady=15)

        # Current status
        energy = self.energy_system.get_energy()
        schedule = self.game_data.data['time'].get('sleep_schedule', 'Normal')
        crunch_weeks = self.game_data.data['time'].get('crunch_weeks', 0)

        status_frame = tk.Frame(sleep_window, bg='#f0f0f0', relief='ridge', bd=2)
        status_frame.pack(pady=15, padx=20, fill='x')

        tk.Label(status_frame, text=f"Current Energy: {energy}%", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        tk.Label(status_frame, text=f"Current Schedule: {schedule}", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=5)
        if crunch_weeks > 0:
            tk.Label(status_frame, text=f"Crunch Weeks: {crunch_weeks}/5", font=('Arial', 12, 'bold'), fg='red', bg='#f0f0f0').pack(pady=5)

        # Schedule options
        options_frame = tk.Frame(sleep_window)
        options_frame.pack(pady=20, padx=30, fill='both', expand=True)

        schedules = {
            SleepSchedule.CRUNCH.value: "5 hours sleep, 16 hours work\n+30% productivity, -3 energy/hour\nMax 5 weeks",
            SleepSchedule.NORMAL.value: "8 hours sleep, 8 hours work\nBalanced lifestyle",
            SleepSchedule.RESTORATIVE.value: "10 hours sleep, 6 hours work\n-20% productivity, +stress relief"
        }

        selected_schedule = tk.StringVar(value=schedule)

        def on_schedule_select(schedule_type):
            """Handle schedule selection (without sleeping)"""
            new_schedule = schedule_type

            # Set new schedule
            success, message = self.time_system.set_schedule(new_schedule)
            if not success:
                messagebox.showwarning("Cannot Change Schedule", message)
                return

            # Update pillow text
            schedule_text = new_schedule.replace("Crunch Time", "Crunch")
            self.canvas.itemconfig(self.pillow_text, text=schedule_text)

            sleep_window.destroy()
            messagebox.showinfo("Schedule Changed", f"Sleep schedule set to: {new_schedule}\nClick bed again to sleep.")

        for sched_type, description in schedules.items():
            frame = tk.Frame(options_frame, relief='groove', bd=2, padx=10, pady=10, cursor="hand2")
            frame.pack(anchor='w', pady=10, fill='x')

            # Make entire frame clickable
            frame.bind("<Button-1>", lambda e, s=sched_type: on_schedule_select(s))

            rb = tk.Radiobutton(frame, text=sched_type, variable=selected_schedule,
                          value=sched_type, font=('Arial', 14, 'bold'), cursor="hand2",
                          command=lambda s=sched_type: on_schedule_select(s))
            rb.pack(side='left')

            lbl = tk.Label(frame, text=f"  {description}", font=('Arial', 11), cursor="hand2")
            lbl.pack(side='left', padx=10)
            # Make label clickable too
            lbl.bind("<Button-1>", lambda e, s=sched_type: on_schedule_select(s))

        # Buttons for sleep and cancel
        button_frame = tk.Frame(sleep_window)
        button_frame.pack(pady=30)

        def sleep_now():
            """Sleep with current schedule"""
            schedule_info = self.time_system.get_schedule_info()

            # Sleep and advance time
            self.time_system.advance_time(schedule_info['sleep_hours'])

            # Restore energy based on sleep hours
            base_restoration = schedule_info['sleep_hours'] * 12
            self.energy_system.set_energy(min(100, base_restoration))

            # Reduce stress
            stress_reduction = 10
            current_schedule = self.game_data.data['time'].get('sleep_schedule', 'Normal')
            if current_schedule == SleepSchedule.RESTORATIVE.value:
                stress_reduction = schedule_info.get('stress_reduction', 5) + 10

            current_stress = self.game_data.data['player_data'].get('stress_level', 0)
            self.game_data.data['player_data']['stress_level'] = max(0, current_stress - stress_reduction)

            # Daily update for energy system
            self.energy_system.daily_update()

            sleep_window.destroy()
            self.update_status_display()

            messagebox.showinfo("Good Morning!",
                              f"You slept for {schedule_info['sleep_hours']} hours\n"
                              f"Energy: {self.energy_system.get_energy()}%\n"
                              f"Schedule: {current_schedule}")

        tk.Button(button_frame, text="Sleep Now", command=sleep_now,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=sleep_window.destroy,
                 bg='#555', fg='white', font=('Arial', 12),
                 padx=30, pady=10).pack(side='left', padx=10)

    def update_player_position(self):
        """Update player position based on target"""
        if not self.is_moving:
            return

        # Calculate distance to target
        dx = self.target_x - self.player_x
        dy = self.target_y - self.player_y
        distance = math.sqrt(dx**2 + dy**2)

        # If close enough to target, stop
        if distance < self.player_speed:
            self.player_x = self.target_x
            self.player_y = self.target_y
            self.is_moving = False
        else:
            # Move towards target
            move_x = (dx / distance) * self.player_speed
            move_y = (dy / distance) * self.player_speed

            new_x = self.player_x + move_x
            new_y = self.player_y + move_y

            # Keep player within room bounds
            new_x = max(self.player_radius, min(self.room_width - self.player_radius, new_x))
            new_y = max(self.player_radius, min(self.room_height - self.player_radius, new_y))

            # Check collision with furniture
            if not self.check_collision(new_x, new_y):
                # Update position if no collision
                dx = new_x - self.player_x
                dy = new_y - self.player_y

                self.player_x = new_x
                self.player_y = new_y

                # Move player on canvas
                self.canvas.move(self.player_obj, dx, dy)
            else:
                # Try sliding along the obstacle
                # Try horizontal movement only
                if not self.check_collision(new_x, self.player_y):
                    dx = new_x - self.player_x
                    self.player_x = new_x
                    self.canvas.move(self.player_obj, dx, 0)
                # Try vertical movement only
                elif not self.check_collision(self.player_x, new_y):
                    dy = new_y - self.player_y
                    self.player_y = new_y
                    self.canvas.move(self.player_obj, 0, dy)
                else:
                    # Can't slide, stop moving
                    self.is_moving = False

        # Check if player reached a station
        self.check_station_reached()

    def check_collision(self, x, y):
        # Define furniture boundaries for cramped room with proximity buffer
        proximity_distance = 15  # Stop 15 pixels away from furniture

        furniture = [
            # Bed
            {'name': 'bed', 'x': 10, 'y': 10, 'width': 60, 'height': 80},
            # Desk
            {'name': 'desk', 'x': self.room_width - 80, 'y': 10, 'width': 70, 'height': 50},
            # Shower
            {'name': 'shower', 'x': 10, 'y': self.room_height - 80, 'width': 50, 'height': 60},
            # Fridge
            {'name': 'fridge', 'x': self.room_width - 100, 'y': self.room_height - 90, 'width': 40, 'height': 70},
            # Microwave
            {'name': 'microwave', 'x': self.room_width - 50, 'y': self.room_height - 110, 'width': 35, 'height': 20}
        ]

        # Check proximity to each furniture piece
        for item in furniture:
            # Skip collision check for current station
            if item['name'] == self.current_station:
                continue

            # Expand the collision box by proximity_distance
            if (x + self.player_radius + proximity_distance > item['x'] and
                x - self.player_radius - proximity_distance < item['x'] + item['width'] and
                y + self.player_radius + proximity_distance > item['y'] and
                y - self.player_radius - proximity_distance < item['y'] + item['height']):
                return True
        return False

    def check_station_reached(self):
        """Check if player has reached a station"""
        interaction_distance = 25  # Distance to interact with station

        furniture = [
            {'name': 'bed', 'x': 10, 'y': 10, 'width': 60, 'height': 80},
            {'name': 'desk', 'x': self.room_width - 80, 'y': 10, 'width': 70, 'height': 50},
            {'name': 'shower', 'x': 10, 'y': self.room_height - 80, 'width': 50, 'height': 60},
            {'name': 'fridge', 'x': self.room_width - 100, 'y': self.room_height - 90, 'width': 40, 'height': 70},
            {'name': 'microwave', 'x': self.room_width - 50, 'y': self.room_height - 110, 'width': 35, 'height': 20}
        ]

        # Check if player is near any station
        for item in furniture:
            # Calculate center of furniture
            center_x = item['x'] + item['width'] / 2
            center_y = item['y'] + item['height'] / 2

            # Calculate distance from player to center
            dist = math.sqrt((self.player_x - center_x)**2 + (self.player_y - center_y)**2)

            # Check if within interaction range
            if dist < interaction_distance + max(item['width'], item['height']) / 2:
                # If this is a new station
                if self.current_station != item['name']:
                    previous_station = self.current_station
                    self.current_station = item['name']

                    # If we were inside previous station's hitbox, push out
                    if previous_station:
                        self.push_out_of_station(previous_station)
                return

        # No station in range, clear current station
        if self.current_station:
            self.current_station = None

    def push_out_of_station(self, station_name):
        """Push player out of station's hitbox when switching stations"""
        furniture = {
            'bed': {'x': 10, 'y': 10, 'width': 60, 'height': 80},
            'desk': {'x': self.room_width - 80, 'y': 10, 'width': 70, 'height': 50},
            'shower': {'x': 10, 'y': self.room_height - 80, 'width': 50, 'height': 60},
            'fridge': {'x': self.room_width - 100, 'y': self.room_height - 90, 'width': 40, 'height': 70},
            'microwave': {'x': self.room_width - 50, 'y': self.room_height - 110, 'width': 35, 'height': 20}
        }

        if station_name not in furniture:
            return

        item = furniture[station_name]
        buffer = 5  # Small buffer to ensure we're outside

        # Check if player is inside the station's hitbox
        if (self.player_x > item['x'] - self.player_radius and
            self.player_x < item['x'] + item['width'] + self.player_radius and
            self.player_y > item['y'] - self.player_radius and
            self.player_y < item['y'] + item['height'] + self.player_radius):

            # Find closest edge and push player out
            distances = [
                (self.player_x - item['x'], -1, 0),  # Left edge
                (item['x'] + item['width'] - self.player_x, 1, 0),  # Right edge
                (self.player_y - item['y'], 0, -1),  # Top edge
                (item['y'] + item['height'] - self.player_y, 0, 1)  # Bottom edge
            ]

            # Find minimum distance edge
            min_dist, dx, dy = min(distances, key=lambda x: abs(x[0]))

            # Push player out
            if dx != 0:
                if dx < 0:
                    self.player_x = item['x'] - self.player_radius - buffer
                else:
                    self.player_x = item['x'] + item['width'] + self.player_radius + buffer
            else:
                if dy < 0:
                    self.player_y = item['y'] - self.player_radius - buffer
                else:
                    self.player_y = item['y'] + item['height'] + self.player_radius + buffer

            # Update canvas position
            self.canvas.coords(self.player_obj,
                             self.player_x - self.player_radius,
                             self.player_y - self.player_radius,
                             self.player_x + self.player_radius,
                             self.player_y + self.player_radius)

    def start_game_loop(self):
        self.update_player_position()
        # Update real-time clock
        self.time_system.update_real_time()
        self.update_status_display()
        # Schedule next update (60 FPS)
        self.root.after(16, self.start_game_loop)

    def cycle_speed(self):
        """Cycle through speed presets"""
        # Speed presets: 1x, Quick Day, Quick Week, Quick Month, Quick Quarter, MAX
        speed_cycles = [
            (1, "1x"),           # Real-time
            (960, "2x"),         # Quick Day (shown as 2x)
            (6720, "3x"),        # Quick Week (shown as 3x)
            (25920, "4x"),       # Quick Month (shown as 4x)
            (64800, "5x"),       # Quick Quarter (shown as 5x)
            (60500, "MAX")       # Maximum speed (10% faster than before)
        ]

        # Find current speed in cycle
        current_speed = self.time_system.time_scale
        next_index = 0

        for i, (speed, label) in enumerate(speed_cycles):
            if abs(current_speed - speed) < 10:  # Allow small tolerance for float comparison
                next_index = (i + 1) % len(speed_cycles)
                break

        # Set new speed
        new_speed, new_label = speed_cycles[next_index]
        self.time_system.time_scale = new_speed

        # Update button text
        self.speed_button.config(text=f"⏩ {new_label}")

        # Update status display
        self.update_status_display()

    def update_status_display(self):
        """Update the status display labels"""
        # Time display based on speed
        current_speed = self.time_system.time_scale
        time_data = self.game_data.data['time']

        if current_speed <= 960:  # 1x or 2x speed - show seconds
            hour = int(time_data.get('hour', 8))
            minute = int(time_data.get('minute', 0))
            second = int(time_data.get('second', 0))
            am_pm = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0:
                display_hour = 12
            time_str = f"{display_hour:02d}:{minute:02d}:{second:02d} {am_pm}"
            date_str = self.time_system.get_date_string()
            self.time_label.config(text=f"{date_str} - {time_str}")
        elif current_speed >= 60000:  # MAX speed - only show date
            date_str = self.time_system.get_date_string()
            self.time_label.config(text=date_str)
        elif current_speed >= 64800:  # 5x speed - show day and AM/PM
            hour = int(time_data.get('hour', 8))
            am_pm = "AM" if hour < 12 else "PM"
            date_str = self.time_system.get_date_string()
            self.time_label.config(text=f"{date_str} {am_pm}")
        else:  # 3x, 4x speed - normal display
            time_str = self.time_system.get_time_string()
            date_str = self.time_system.get_date_string()
            self.time_label.config(text=f"{date_str} - {time_str}")

        # Energy display
        energy = self.energy_system.get_energy()
        productivity = self.energy_system.get_productivity_modifier()
        energy_color = '#90EE90' if energy >= 50 else '#FFA500' if energy >= 30 else '#FF6B6B'
        self.energy_label.config(text=f"Energy: {energy}% (Prod: {int(productivity*100)}%)", fg=energy_color)

    def back_to_menu(self):
        if self.on_back:
            self.on_back()