"""
Temple Runner - A Prince of Persia inspired platformer
Rendered in retro green terminal style
"""

import tkinter as tk
from tkinter import Canvas
import random
import math


class TempleRunner:
    """A side-scrolling platformer game in terminal green style"""

    def __init__(self, root):
        self.root = root
        self.root.title("Temple Runner - Terminal Edition")
        self.root.geometry("1200x600")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)

        # Terminal colors
        self.bg_color = '#000000'
        self.fg_color = '#00ff00'
        self.dim_color = '#008800'
        self.danger_color = '#00ff00'  # Still green but we'll use patterns

        # Game state
        self.running = False
        self.game_over = False
        self.score = 0
        self.distance = 0
        self.immunity_frames = 0  # Immunity at start

        # Physics
        self.gravity = 0.8
        self.jump_power = -19  # Moderate starting jump height
        self.base_jump_power = -19
        self.jump_count = 0  # Track number of jumps for degradation
        self.jump_decrease = 1.0  # Decrease by 1 per jump

        # Player properties
        self.player = {
            'x': 150,
            'y': 400,
            'width': 20,
            'height': 40,
            'vel_y': 0,
            'on_ground': False,
            'jumping': False,
            'running_frame': 0,
            'jump_frame': 0,
            'state': 'idle'  # idle, running, jumping, falling
        }

        # Level data
        self.scroll_speed = 6  # Start with faster speed
        self.base_scroll_speed = 6
        self.world_offset = 0
        self.time_elapsed = 0  # Track time for difficulty scaling
        self.platforms = []
        self.trenches = []
        self.obstacles = []

        # Animation timing
        self.animation_tick = 0

        # Generate initial level
        self.generate_level()

        # Setup UI
        self.setup_ui()

        # Start game loop
        self.start_game()

    def setup_ui(self):
        """Setup the game interface"""
        # Main canvas
        self.canvas = Canvas(
            self.root,
            width=1200,
            height=600,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack()

        # Draw terminal border
        self.draw_terminal_border()

        # Score display
        self.score_text = self.canvas.create_text(
            50, 30,
            text=f"SCORE: {self.score:06d}",
            font=('Courier', 14, 'bold'),
            fill=self.fg_color,
            anchor='w'
        )

        # Distance display
        self.distance_text = self.canvas.create_text(
            50, 50,
            text=f"DISTANCE: {self.distance:04d}m",
            font=('Courier', 14, 'bold'),
            fill=self.fg_color,
            anchor='w'
        )

        # Instructions
        self.canvas.create_text(
            1150, 30,
            text="[SPACE] JUMP",
            font=('Courier', 10),
            fill=self.dim_color,
            anchor='e'
        )
        self.canvas.create_text(
            1150, 50,
            text="[ESC] EXIT",
            font=('Courier', 10),
            fill=self.dim_color,
            anchor='e'
        )

        # Bind keys
        self.root.bind('<space>', self.jump)
        self.root.bind('<Escape>', self.quit_game)

        # Start screen
        self.start_screen()

    def draw_terminal_border(self):
        """Draw a terminal-style border"""
        # Top and bottom borders
        for y in [10, 590]:
            for x in range(0, 1200, 20):
                self.canvas.create_text(
                    x, y,
                    text="═",
                    font=('Courier', 12),
                    fill=self.dim_color,
                    anchor='w'
                )

        # Side borders
        for y in range(10, 590, 20):
            self.canvas.create_text(
                10, y,
                text="║",
                font=('Courier', 12),
                fill=self.dim_color,
                anchor='w'
            )
            self.canvas.create_text(
                1180, y,
                text="║",
                font=('Courier', 12),
                fill=self.dim_color,
                anchor='w'
            )

    def start_screen(self):
        """Show start screen"""
        self.start_text = self.canvas.create_text(
            600, 250,
            text="TEMPLE RUNNER",
            font=('Courier', 24, 'bold'),
            fill=self.fg_color
        )
        self.start_info = self.canvas.create_text(
            600, 300,
            text="Press SPACE to start",
            font=('Courier', 14),
            fill=self.dim_color
        )

        # ASCII art temple
        temple_art = """
           ╔═══╗
           ║▲▲▲║
         ╔═╬═══╬═╗
         ║ ║   ║ ║
         ║ ╠═══╣ ║
         ╚═╩═══╩═╝
        """
        self.canvas.create_text(
            600, 400,
            text=temple_art,
            font=('Courier', 10),
            fill=self.dim_color,
            justify='center'
        )

    def generate_level(self):
        """Generate level segments with increasing difficulty"""
        # Ground level
        ground_y = 450

        # Calculate difficulty-scaled sizes
        # Gaps get progressively wider (100 to 150 pixels)
        gap_width = min(100 + int(self.time_elapsed / 100), 150)

        # Platform width stays reasonable
        platform_width = 300

        # Generate new segments at the end
        if len(self.platforms) == 0:
            current_x = 0
        else:
            # Find the furthest platform/trench
            max_x = 0
            for p in self.platforms:
                max_x = max(max_x, p['x'] + p['width'])
            for t in self.trenches:
                max_x = max(max_x, t['x'] + t['width'])
            current_x = max_x

        # Generate until we have enough level ahead
        while current_x < self.world_offset + 2000:
            # Increase obstacle frequency - more obstacles and trenches
            segment_weights = ['platform', 'platform', 'trench', 'trench', 'obstacle', 'obstacle', 'obstacle']
            segment_type = random.choice(segment_weights)

            if segment_type == 'platform':
                # Solid ground platform
                self.platforms.append({
                    'x': current_x,
                    'y': ground_y,
                    'width': platform_width,
                    'height': 150
                })
                current_x += platform_width

            elif segment_type == 'trench':
                # Gap to jump over - gets wider over time
                self.trenches.append({
                    'x': current_x,
                    'y': ground_y,
                    'width': gap_width
                })
                current_x += gap_width

            elif segment_type == 'obstacle':
                # Platform with obstacle
                self.platforms.append({
                    'x': current_x,
                    'y': ground_y,
                    'width': platform_width,
                    'height': 150
                })

                # Add spikes - start larger (60px) and increase over time (up to 120px)
                spike_width = min(60 + int(self.time_elapsed / 100), 120)
                if random.random() > 0.2:  # 80% chance of spikes
                    self.obstacles.append({
                        'type': 'spikes',
                        'x': current_x + platform_width // 2 - spike_width // 2,
                        'y': ground_y - 25,  # Slightly taller spikes
                        'width': spike_width,
                        'height': 25
                    })

                current_x += platform_width

        # Clean up old platforms that are way behind
        self.platforms = [p for p in self.platforms if p['x'] + p['width'] > self.world_offset - 500]
        self.trenches = [t for t in self.trenches if t['x'] + t['width'] > self.world_offset - 500]
        self.obstacles = [o for o in self.obstacles if o['x'] + o['width'] > self.world_offset - 500]

    def start_game(self):
        """Start the game loop"""
        self.running = True
        self.game_over = False
        self.immunity_frames = 60  # 2 seconds at 30 FPS

        # Remove start screen
        if hasattr(self, 'start_text'):
            self.canvas.delete(self.start_text)
            self.canvas.delete(self.start_info)

        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        if not self.running:
            return

        # Clear canvas (except UI elements)
        self.canvas.delete('game_object')

        # Update game state
        self.update_physics()
        self.update_world()
        self.check_collisions()

        # Draw everything
        self.draw_world()
        self.draw_player()

        # Update UI
        self.update_ui()

        # Check game over
        if self.game_over:
            self.show_game_over()
            return

        # Continue loop
        self.root.after(33, self.game_loop)  # ~30 FPS

    def update_physics(self):
        """Update player physics"""
        # Apply gravity
        if not self.player['on_ground']:
            self.player['vel_y'] += self.gravity
            if self.player['vel_y'] > 20:
                self.player['vel_y'] = 20

        # Update vertical position
        self.player['y'] += self.player['vel_y']

        # Update player state
        if not self.player['on_ground']:
            if self.player['vel_y'] < 0:
                self.player['state'] = 'jumping'
            else:
                self.player['state'] = 'falling'
        else:
            self.player['state'] = 'running'

        # Update animation
        self.animation_tick += 1
        if self.animation_tick % 3 == 0:
            if self.player['state'] == 'running':
                self.player['running_frame'] = (self.player['running_frame'] + 1) % 8
            elif self.player['state'] == 'jumping':
                self.player['jump_frame'] = min(self.player['jump_frame'] + 1, 3)

    def update_world(self):
        """Update world with auto-scrolling and difficulty scaling"""
        if not self.game_over:
            # Auto-scroll the world
            self.world_offset += self.scroll_speed
            self.distance += self.scroll_speed / 10
            self.time_elapsed += 1

            # Decrease immunity frames
            if self.immunity_frames > 0:
                self.immunity_frames -= 1

            # Gradually increase scroll speed (caps at 12)
            if self.time_elapsed % 200 == 0:
                self.scroll_speed = min(self.scroll_speed + 0.3, 12)

            # Generate more level as needed
            self.generate_level()

    def check_collisions(self):
        """Check player collisions with world"""
        player_rect = {
            'x': self.player['x'],
            'y': self.player['y'],
            'right': self.player['x'] + self.player['width'],
            'bottom': self.player['y'] + self.player['height']
        }

        # Reset ground flag
        self.player['on_ground'] = False

        # Check platform collisions
        for platform in self.platforms:
            plat_x = platform['x'] - self.world_offset
            if (plat_x < player_rect['right'] and
                plat_x + platform['width'] > player_rect['x']):

                # Check if standing on platform
                if (player_rect['bottom'] >= platform['y'] and
                    player_rect['bottom'] <= platform['y'] + 20 and
                    self.player['vel_y'] >= 0):

                    self.player['on_ground'] = True
                    self.player['jumping'] = False  # Reset jumping flag when landing
                    self.player['y'] = platform['y'] - self.player['height']
                    self.player['vel_y'] = 0
                    self.player['state'] = 'running'
                    self.player['jump_frame'] = 0

        # Check if fallen into trench (no immunity for falling)
        if not self.player['on_ground'] and self.player['y'] > 500:
            if self.immunity_frames <= 0:
                self.game_over = True

        # Check obstacle collisions (respect immunity)
        if self.immunity_frames <= 0:
            for obstacle in self.obstacles:
                obs_x = obstacle['x'] - self.world_offset
                if (obs_x < player_rect['right'] and
                    obs_x + obstacle['width'] > player_rect['x'] and
                    obstacle['y'] < player_rect['bottom'] and
                    obstacle['y'] + obstacle['height'] > player_rect['y']):
                    # Hit obstacle
                    self.game_over = True

    def draw_world(self):
        """Draw the game world"""
        # Draw wall candles every 150 pixels
        for x in range(0, 2400, 150):
            candle_x = x - (self.world_offset % 150)
            if candle_x >= 0 and candle_x <= 1200:
                # Upper wall candles
                self.draw_candle(candle_x, 150)
                # Lower wall candles
                self.draw_candle(candle_x, 350)

        # Draw platforms
        for platform in self.platforms:
            x = platform['x'] - self.world_offset
            if x > -platform['width'] and x < 1200:
                # Platform surface
                for px in range(0, platform['width'], 20):
                    self.canvas.create_text(
                        x + px, platform['y'],
                        text='▓',
                        font=('Courier', 12),
                        fill=self.fg_color,
                        anchor='w',
                        tags='game_object'
                    )

                # Platform edge markers
                self.canvas.create_text(
                    x, platform['y'],
                    text='╔',
                    font=('Courier', 12),
                    fill=self.fg_color,
                    anchor='w',
                    tags='game_object'
                )
                self.canvas.create_text(
                    x + platform['width'] - 10, platform['y'],
                    text='╗',
                    font=('Courier', 12),
                    fill=self.fg_color,
                    anchor='w',
                    tags='game_object'
                )

        # Draw trenches
        for trench in self.trenches:
            x = trench['x'] - self.world_offset
            if x > -trench['width'] and x < 1200:
                # Trench bottom
                for tx in range(0, trench['width'], 15):
                    self.canvas.create_text(
                        x + tx, 550,
                        text='▼',
                        font=('Courier', 10),
                        fill=self.dim_color,
                        anchor='w',
                        tags='game_object'
                    )

        # Draw obstacles
        for obstacle in self.obstacles:
            x = obstacle['x'] - self.world_offset
            if x > -obstacle['width'] and x < 1200:
                if obstacle['type'] == 'spikes':
                    # Draw base to show full hitbox width
                    base_chars = '═' * (obstacle['width'] // 10)
                    self.canvas.create_text(
                        x, obstacle['y'] + obstacle['height'],
                        text=base_chars,
                        font=('Courier', 10),
                        fill=self.dim_color,
                        anchor='w',
                        tags='game_object'
                    )

                    # Draw spikes spread across the full width
                    num_spikes = obstacle['width'] // 12
                    for i in range(num_spikes):
                        spike_x = x + (i * 12) + 4
                        # Alternating heights for visual variety
                        spike_y = obstacle['y'] + (5 if i % 2 == 0 else 8)
                        self.canvas.create_text(
                            spike_x, spike_y,
                            text='▲',
                            font=('Courier', 12, 'bold'),
                            fill=self.fg_color,
                            anchor='w',
                            tags='game_object'
                        )

                    # Draw danger zone box outline to show exact hitbox
                    # Left edge
                    self.canvas.create_text(
                        x, obstacle['y'] + 5,
                        text='[',
                        font=('Courier', 16, 'bold'),
                        fill='#ff8800',
                        anchor='w',
                        tags='game_object'
                    )
                    # Right edge
                    self.canvas.create_text(
                        x + obstacle['width'] - 8, obstacle['y'] + 5,
                        text=']',
                        font=('Courier', 16, 'bold'),
                        fill='#ff8800',
                        anchor='w',
                        tags='game_object'
                    )

    def draw_candle(self, x, y):
        """Draw an animated flame candle"""
        # Candle holder
        self.canvas.create_text(
            x, y + 20,
            text='╒╕',
            font=('Courier', 8),
            fill=self.dim_color,
            anchor='w',
            tags='game_object'
        )
        self.canvas.create_text(
            x, y + 30,
            text='│││',
            font=('Courier', 8),
            fill=self.dim_color,
            anchor='w',
            tags='game_object'
        )

        # Animated flame (use animation tick for flicker effect)
        flame_chars = ['▲', '♦', '◊', '▼']
        flame_index = (self.animation_tick // 5) % len(flame_chars)

        # Flame colors that alternate
        flame_colors = ['#ffff00', '#ff8800', '#ffaa00', '#ff6600']
        color_index = (self.animation_tick // 3) % len(flame_colors)

        # Draw flame
        self.canvas.create_text(
            x + 3, y + 10,
            text=flame_chars[flame_index],
            font=('Courier', 10),
            fill=flame_colors[color_index],
            anchor='w',
            tags='game_object'
        )

        # Inner flame
        self.canvas.create_text(
            x + 4, y + 12,
            text='•',
            font=('Courier', 6),
            fill='#ffffff',
            anchor='w',
            tags='game_object'
        )

    def draw_player(self):
        """Draw the player character"""
        x = self.player['x']
        y = self.player['y']

        # ASCII representation based on state
        if self.player['state'] == 'running':
            # Running animation frames
            frames = [
                ["  O  ", " /|\\ ", " / \\ "],
                ["  O  ", " /|\\ ", " |\\ "],
                ["  O  ", " /|\\ ", " | | "],
                ["  O  ", " /|\\ ", " /| "],
                ["  O  ", " \\|/ ", " / \\ "],
                ["  O  ", " \\|/ ", " |\\ "],
                ["  O  ", " \\|/ ", " | | "],
                ["  O  ", " \\|/ ", " /| "]
            ]
            frame = frames[self.player['running_frame']]

        elif self.player['state'] == 'jumping' or not self.player['on_ground']:
            # Jumping animation
            frame = ["  O  ", " \\|/ ", " / \\ "]
            if self.player['vel_y'] > 5:  # Falling
                frame = ["  O  ", " /|\\ ", " | | "]

        else:  # Idle
            frame = ["  O  ", " /|\\ ", " | | "]

        # Draw character (with immunity flashing)
        player_color = self.fg_color
        if self.immunity_frames > 0:
            # Flash between colors when immune
            if (self.immunity_frames // 5) % 2 == 0:
                player_color = '#ffff00'  # Yellow flash
            else:
                player_color = '#00ffff'  # Cyan flash

        for i, line in enumerate(frame):
            self.canvas.create_text(
                x, y + i * 13,
                text=line,
                font=('Courier', 10, 'bold'),
                fill=player_color,
                anchor='w',
                tags='game_object'
            )

    def jump(self, event=None):
        """Handle jump input"""
        if not self.running and not self.game_over:
            self.start_game()
            return

        if self.game_over:
            self.restart_game()
            return

        if self.player['on_ground']:
            # Calculate jump power with linear decrease per jump
            # More negative = higher jump, so we need to move toward 0
            # Start at -30, then -29, -28, etc.
            current_jump_power = self.base_jump_power + (self.jump_count * self.jump_decrease)
            current_jump_power = min(current_jump_power, 0)  # Cap at 0 (no jump)
            self.jump_count += 1

            self.player['vel_y'] = current_jump_power
            self.player['jumping'] = True
            self.player['on_ground'] = False
            self.player['state'] = 'jumping'
            self.player['jump_frame'] = 0

    def update_ui(self):
        """Update score and distance displays"""
        self.score = int(self.distance // 10)
        self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score:06d}")
        self.canvas.itemconfig(self.distance_text, text=f"DISTANCE: {int(self.distance):04d}m")

    def show_game_over(self):
        """Show game over screen"""
        self.running = False

        # Game over text
        self.canvas.create_text(
            600, 250,
            text="GAME OVER",
            font=('Courier', 24, 'bold'),
            fill=self.fg_color,
            tags='game_over'
        )
        self.canvas.create_text(
            600, 300,
            text=f"Final Score: {self.score}",
            font=('Courier', 16),
            fill=self.fg_color,
            tags='game_over'
        )
        self.canvas.create_text(
            600, 350,
            text="Press SPACE to restart",
            font=('Courier', 12),
            fill=self.dim_color,
            tags='game_over'
        )

    def restart_game(self):
        """Restart the game"""
        # Reset game state
        self.score = 0
        self.distance = 0
        self.world_offset = 0
        self.time_elapsed = 0
        self.scroll_speed = self.base_scroll_speed
        self.jump_power = self.base_jump_power
        self.jump_count = 0  # Reset jump counter
        self.immunity_frames = 60  # Give immunity on restart too
        self.player['x'] = 150
        self.player['y'] = 400
        self.player['vel_y'] = 0
        self.player['on_ground'] = False
        self.player['jumping'] = False
        self.player['state'] = 'idle'

        # Clear existing level
        self.platforms = []
        self.trenches = []
        self.obstacles = []

        # Clear game over screen
        self.canvas.delete('game_over')

        # Generate new level
        self.generate_level()

        # Restart
        self.start_game()

    def quit_game(self, event=None):
        """Quit the game"""
        self.running = False
        self.root.destroy()


# Allow running as standalone
if __name__ == "__main__":
    root = tk.Tk()
    game = TempleRunner(root)
    root.mainloop()