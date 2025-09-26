"""
Development Stages System
Handles the multi-stage game development process with animations
"""

import tkinter as tk
from tkinter import ttk
import random
import math
from dataclasses import dataclass
from typing import Dict, Optional, Callable
from enum import Enum
from systems.points_generation import (
    PointsGenerator,
    DeveloperStats,
    create_player_developer,
    DevelopmentStage as PGDevelopmentStage
)
from systems.game_end_manager import GameEndManager, GTGISSScores

class DevelopmentStage(Enum):
    PLANNING = "Planning"
    DEVELOPMENT = "Development"
    PRODUCTION = "Production"
    BUG_SQUASHING = "Bug Squashing"

@dataclass
class StageScores:
    """Scores generated in a specific stage"""
    gameplay: int = 0
    technical: int = 0
    graphics: int = 0
    innovation: int = 0
    sound_audio: int = 0
    story: int = 0
    bugs: int = 0  # Track bugs generated

class DevelopmentStageWindow:
    """Window for handling a single development stage with bouncing animation"""

    def __init__(self, root, game_data, stage: DevelopmentStage, developer_name: str,
                 developer_stats: Optional[DeveloperStats] = None,
                 on_complete: Optional[Callable] = None):
        self.root = root
        self.game_data = game_data
        self.stage = stage
        self.developer_name = developer_name
        self.developer_stats = developer_stats or create_player_developer()
        self.on_complete = on_complete

        # Calculate bounces based on developer stats
        from systems.points_generation import BounceCalculator
        from systems.stage_scoring import StageScoreCalculator

        self.bounce_calculator = BounceCalculator()
        self.max_bounces, self.bounce_details = self.bounce_calculator.calculate_bounces(self.developer_stats)

        # Pre-calculate all scores for this stage
        self.score_calculator = StageScoreCalculator(game_data)

        # Get current year
        current_year = 1984
        if game_data and 'game_time' in game_data.data:
            date_str = game_data.data['game_time'].get('current_date', '1984-01-01')
            current_year = int(date_str.split('-')[0])

        # Convert stage enum for score calculator
        from systems.stage_scoring import DevelopmentStage as ScoreStage
        score_stage = None
        if self.stage == DevelopmentStage.PLANNING:
            score_stage = ScoreStage.PLANNING
        elif self.stage == DevelopmentStage.DEVELOPMENT:
            score_stage = ScoreStage.DEVELOPMENT
        elif self.stage == DevelopmentStage.PRODUCTION:
            score_stage = ScoreStage.PRODUCTION
        else:
            score_stage = ScoreStage.BUG_SQUASHING

        # Pre-calculate all bounce scores
        self.precalculated_scores = self.score_calculator.precalculate_stage_scores(
            score_stage,
            self.developer_stats,
            self.max_bounces,
            current_year
        )

        # Ensure we have at least 1 score (matching max_bounces which is at least 1)
        # and each score is at least 2 points
        if not self.precalculated_scores:
            self.precalculated_scores = [2] * max(1, self.max_bounces)
        else:
            # Ensure each precalculated score is at least 2
            self.precalculated_scores = [max(2, score) for score in self.precalculated_scores]

        # Calculate weighted skill for display
        self.weighted_skill = self.score_calculator.calculate_weighted_skill(
            self.developer_stats,
            score_stage
        )

        self.current_bounce_index = 0
        self.score_stage = score_stage

        # Show calculation menu first
        self.show_calculation_menu()

    def show_calculation_menu(self):
        """Log bounce calculations to console instead of showing UI"""
        print("\n" + "="*60)
        print(f"DEVELOPER PERFORMANCE ANALYSIS - {self.stage.value} Stage")
        print("="*60)
        print(f"Developer: {self.developer_name}")
        print("\n" + "-"*30 + " SKILL BREAKDOWN " + "-"*30)

        # Log each skill
        for skill_name, skill_value in self.bounce_details['skills'].items():
            bar = "█" * int(skill_value) + "░" * (10 - int(skill_value))
            print(f"{skill_name.title():15} [{bar}] {skill_value}/10")

        print("\n" + "-"*30 + " COMPOSITE SCORE " + "-"*30)
        print(f"Composite Score: {self.bounce_details['composite_score']}/{self.bounce_details['max_score']}")
        print(f"Performance Level: {self.bounce_details['percentage']:.1f}%")
        print(f"Weighted Skill: {self.weighted_skill:.1f}/100")
        print(f"Pre-calculated scores: {self.precalculated_scores}")
        if self.precalculated_scores:
            print(f"Expected Avg: {sum(self.precalculated_scores)/len(self.precalculated_scores):.1f} pts/bounce")
        else:
            print("Expected Avg: 0.0 pts/bounce (no scores pre-calculated)")

        print("\n" + "-"*30 + " BOUNCE CALCULATION " + "-"*28)
        print(f"Expected Bounces: {self.bounce_details['expected_bounces']}")
        print(f"Actual Bounces: {self.bounce_details['actual_bounces']} {self.bounce_details['luck_factor']}")
        print(f"Percentile: {self.bounce_details['percentile']:.1f}%")

        # Visual bounce indicator in console
        bounce_visual = ""
        for i in range(10):
            if i < self.max_bounces:
                bounce_visual += "⬤ "
            else:
                bounce_visual += "○ "
        print(f"\nBounces Available: {bounce_visual}")
        print("="*60 + "\n")

        # Skip creating calc_window - just start the stage directly
        self.root.after(500, self.start_stage)
        # Method body removed - replaced by console logging above

    def draw_bell_curve(self, canvas, details):
        """Draw a bell curve visualization showing where the result landed"""
        width = 350
        height = 150

        # Clear canvas
        canvas.delete('all')

        # Draw axes
        canvas.create_line(30, height-20, width-20, height-20, fill='#555', width=2)  # X-axis
        canvas.create_line(30, 20, 30, height-20, fill='#555', width=2)  # Y-axis

        # Draw bell curve
        mean = details['expected_bounces']
        std_dev = 1.5

        # Calculate points for curve
        points = []
        for i in range(100):
            x = i / 10.0  # 0 to 10 bounces
            # Bell curve formula
            y = math.exp(-0.5 * ((x - mean) / std_dev) ** 2)

            # Convert to canvas coordinates
            canvas_x = 30 + (x / 10) * (width - 50)
            canvas_y = height - 20 - (y * (height - 40))
            points.extend([canvas_x, canvas_y])

        # Draw the curve
        if len(points) > 4:
            canvas.create_line(points, fill='#4CAF50', width=2, smooth=True)

        # Draw vertical line for actual result
        actual = details['actual_bounces']
        actual_x = 30 + (actual / 10) * (width - 50)
        canvas.create_line(
            actual_x, 20, actual_x, height-20,
            fill='#FFD700', width=3
        )

        # Draw vertical line for expected
        expected_x = 30 + (mean / 10) * (width - 50)
        canvas.create_line(
            expected_x, 20, expected_x, height-20,
            fill='#888888', width=1, dash=(2,2)
        )

        # X-axis labels
        for i in range(0, 11, 2):
            x_pos = 30 + (i / 10) * (width - 50)
            canvas.create_text(
                x_pos, height-5,
                text=str(i),
                font=('Arial', 8),
                fill='#888'
            )

        # Legend
        canvas.create_line(width-80, 30, width-60, 30, fill='#FFD700', width=3)
        canvas.create_text(width-55, 30, text='Actual', font=('Arial', 8), fill='white', anchor='w')

        canvas.create_line(width-80, 45, width-60, 45, fill='#888888', width=1, dash=(2,2))
        canvas.create_text(width-55, 45, text='Expected', font=('Arial', 8), fill='white', anchor='w')

        # Percentile text
        canvas.create_text(
            actual_x, 10,
            text=f"{details['percentile']:.0f}%ile",
            font=('Arial', 9, 'bold'),
            fill='#FFD700'
        )

    def create_skill_bar(self, parent, skill_name, value):
        """Create a visual skill bar"""
        frame = tk.Frame(parent, bg='#2a2a2a')
        frame.pack(fill='x', padx=20, pady=3)

        # Label
        label = tk.Label(
            frame,
            text=f"{skill_name}:",
            font=('Arial', 10),
            fg='white',
            bg='#2a2a2a',
            width=15,
            anchor='w'
        )
        label.pack(side='left')

        # Progress bar background
        bar_bg = tk.Frame(frame, bg='#444444', height=15, width=100)
        bar_bg.pack(side='left', padx=5)
        bar_bg.pack_propagate(False)

        # Filled bar
        bar_width = int((value / 10) * 100)
        if value >= 8:
            color = '#4CAF50'
        elif value >= 5:
            color = '#FFC107'
        else:
            color = '#F44336'

        bar = tk.Frame(bar_bg, bg=color, height=15, width=bar_width)
        bar.pack(side='left')

        # Value label
        value_label = tk.Label(
            frame,
            text=f"{value}/10",
            font=('Arial', 10),
            fg=color,
            bg='#2a2a2a',
            width=5
        )
        value_label.pack(side='left')

    def start_stage(self):
        """Start the stage"""
        self.window = tk.Toplevel(self.root)
        self.window.title(f"{self.stage.value} Stage - {self.developer_name}")
        self.window.geometry("800x600")
        self.window.configure(bg='#1a1a1a')

        # Position to the right of calculation window
        self.window.update_idletasks()
        x = 500  # To the right of the calculation window
        y = (self.window.winfo_screenheight() // 2) - (300)
        self.window.geometry(f"800x600+{x}+{y}")

        # Animation variables
        self.developer_y = 100
        self.developer_velocity = 0
        self.gravity = 0.5
        self.bounce_force = -12
        self.developer_x = 400
        self.is_bouncing = True
        self.bounce_count = 0
        self.animation_speed = 1.0  # Speed multiplier
        self.animation_delay = 20  # Base delay in ms

        # For bug squashing, show multiple developers
        self.is_team_stage = (self.stage == DevelopmentStage.BUG_SQUASHING)
        if self.is_team_stage:
            self.team_developers = [
                {'x': 200, 'y': 100, 'velocity': 0, 'offset': 0},
                {'x': 400, 'y': 100, 'velocity': 0, 'offset': 10},
                {'x': 600, 'y': 100, 'velocity': 0, 'offset': 20}
            ]

        # Score tracking
        self.stage_scores = StageScores()
        self.score_popups = []  # For animated score displays

        # Points generator for skill-based points
        from systems.points_generation import PointsGenerator
        self.points_generator = PointsGenerator(self.game_data)

        self.setup_ui()
        self.start_animation()

    def setup_ui(self):
        """Setup the UI for the development stage"""
        # Create main canvas that fills most of the window
        self.canvas = tk.Canvas(
            self.window,
            width=780,
            height=500,
            bg='#2a2a2a',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Create category headers at the top
        self.category_positions = {}
        self.category_scores = {}
        self.category_labels = {}

        categories = [
            ('Gameplay', 'gameplay', '#4CAF50'),
            ('Technical', 'technical', '#FF9800'),
            ('Graphics', 'graphics', '#2196F3'),
            ('Innovation', 'innovation', '#9C27B0'),
            ('Sound', 'sound_audio', '#E91E63'),
            ('Story', 'story', '#00BCD4')
        ]

        # Calculate spacing
        spacing = 780 / (len(categories) + 1)

        for i, (display_name, key, color) in enumerate(categories):
            x_pos = spacing * (i + 1)

            # Store position for bubble targeting
            self.category_positions[key] = (x_pos, 50)

            # Create category header box
            self.canvas.create_rectangle(
                x_pos - 40, 20, x_pos + 40, 80,
                fill='#1a1a1a',
                outline=color,
                width=2,
                tags=f'header_{key}'
            )

            # Category name
            self.canvas.create_text(
                x_pos, 35,
                text=display_name,
                font=('Arial', 10, 'bold'),
                fill=color,
                tags=f'header_{key}'
            )

            # Score counter
            score_label = self.canvas.create_text(
                x_pos, 60,
                text='0',
                font=('Arial', 16, 'bold'),
                fill='white',
                tags=f'score_{key}'
            )
            self.category_labels[key] = score_label
            self.category_scores[key] = 0

        # Title in canvas
        self.canvas.create_text(
            390, 110,
            text=f"{self.stage.value} Stage",
            font=('Arial', 20, 'bold'),
            fill='#00ff00',
            tags='title'
        )

        # Developer name
        self.canvas.create_text(
            390, 135,
            text=f"Developer: {self.developer_name}",
            font=('Arial', 12),
            fill='white',
            tags='developer_name'
        )

        # Draw floor (adjusted for taller canvas)
        self.canvas.create_line(
            20, 400, 760, 400,
            fill='#555555',
            width=3,
            tags='floor'
        )

        # Initialize floating bubbles list
        self.floating_bubbles = []

        if self.is_team_stage:
            # Draw multiple developers for team stage
            self.developer_graphics = []
            colors = [
                ('#4CAF50', '#2E7D32', '#FFC107', '#F57C00'),  # Green body, yellow head
                ('#2196F3', '#1976D2', '#FF9800', '#F57C00'),  # Blue body, orange head
                ('#9C27B0', '#7B1FA2', '#E91E63', '#C2185B')   # Purple body, pink head
            ]

            for i, dev in enumerate(self.team_developers):
                body_fill, body_outline, head_fill, head_outline = colors[i % len(colors)]

                # Developer body
                body = self.canvas.create_oval(
                    dev['x'] - 20, dev['y'] - 20,
                    dev['x'] + 20, dev['y'] + 20,
                    fill=body_fill,
                    outline=body_outline,
                    width=2,
                    tags='developer'
                )

                # Developer head
                head = self.canvas.create_oval(
                    dev['x'] - 15, dev['y'] - 35,
                    dev['x'] + 15, dev['y'] - 5,
                    fill=head_fill,
                    outline=head_outline,
                    width=2,
                    tags='developer'
                )

                self.developer_graphics.append({'body': body, 'head': head})
        else:
            # Draw single developer for individual stages
            # Adjust initial Y position for new canvas height
            self.developer_y = 250  # Start higher up on taller canvas

            self.developer_body = self.canvas.create_oval(
                self.developer_x - 20, self.developer_y - 20,
                self.developer_x + 20, self.developer_y + 20,
                fill='#4CAF50',
                outline='#2E7D32',
                width=2,
                tags='developer'
            )

            # Draw developer head
            self.developer_head = self.canvas.create_oval(
                self.developer_x - 15, self.developer_y - 35,
                self.developer_x + 15, self.developer_y - 5,
                fill='#FFC107',
                outline='#F57C00',
                width=2,
                tags='developer'
            )

        # Progress and controls frame
        controls_frame = tk.Frame(self.window, bg='#1a1a1a')
        controls_frame.pack(pady=10)

        # Progress label - hidden for suspense
        self.progress_label = tk.Label(
            controls_frame,
            text="Press SPACE to bounce!",  # Don't show count for suspense
            font=('Arial', 12),
            fg='#888888',
            bg='#1a1a1a'
        )
        self.progress_label.pack(side='left', padx=20)

        # Speed control buttons
        speed_frame = tk.Frame(controls_frame, bg='#1a1a1a')
        speed_frame.pack(side='left', padx=20)

        tk.Label(
            speed_frame,
            text="Speed:",
            font=('Arial', 10),
            fg='white',
            bg='#1a1a1a'
        ).pack(side='left', padx=5)

        # Speed buttons
        speed_buttons = [
            ("1x", 1.0, '#888888'),
            ("2x", 2.0, '#FFC107'),
            ("4x", 4.0, '#FF9800'),
            ("8x", 8.0, '#F44336')
        ]

        self.speed_var = tk.StringVar(value="1x")
        for text, speed, color in speed_buttons:
            btn = tk.Radiobutton(
                speed_frame,
                text=text,
                variable=self.speed_var,
                value=text,
                command=lambda s=speed: self.set_animation_speed(s),
                font=('Arial', 10),
                fg=color,
                bg='#1a1a1a',
                selectcolor='#2a2a2a',
                activebackground='#2a2a2a',
                activeforeground=color,
                indicatoron=0,
                padx=10,
                pady=2
            )
            btn.pack(side='left', padx=2)

        # Bug counter (shows during development)
        self.bug_label = tk.Label(
            controls_frame,
            text="Bugs: 0",
            font=('Arial', 12),
            fg='#F44336',
            bg='#1a1a1a'
        )
        self.bug_label.pack(side='left', padx=20)

    def get_category_color(self, category: str) -> str:
        """Get specific color for each category"""
        colors = {
            'gameplay': '#4CAF50',     # Green
            'technical': '#FF9800',    # Orange
            'graphics': '#2196F3',     # Blue
            'innovation': '#9C27B0',   # Purple
            'sound_audio': '#E91E63',  # Pink
            'story': '#00BCD4',        # Teal/Cyan
            'bugs': '#F44336'          # Red
        }
        return colors.get(category, '#888888')

    def get_stage_color(self, category: str) -> str:
        """Get color based on whether this category is emphasized in this stage"""
        # Just use category colors now
        return self.get_category_color(category)

    def set_animation_speed(self, speed: float):
        """Set the animation speed multiplier"""
        print(f"[DEBUG] Animation speed changed to {speed}x")
        self.animation_speed = speed
        # Adjust animation delay inversely (faster speed = shorter delay)
        self.animation_delay = max(5, int(20 / speed))  # Min 5ms delay

    def start_animation(self):
        """Start the bouncing animation"""
        self.animate()

    def animate(self):
        """Main animation loop"""
        if not self.is_bouncing and len(self.floating_bubbles) == 0:
            print(f"[DEBUG] Animation complete - no bouncing and no bubbles")
            return

        # Check if window still exists
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            print(f"[DEBUG] Animation stopped - window destroyed")
            return

        # Apply speed multiplier to physics
        gravity_adjusted = self.gravity * self.animation_speed
        bounce_force_adjusted = self.bounce_force * (1 + (self.animation_speed - 1) * 0.3)  # Less aggressive scaling for bounce

        if self.is_team_stage:
            # Animate multiple developers
            any_bounced = False
            for i, dev in enumerate(self.team_developers):
                # Update physics with offset for variation
                dev['velocity'] += gravity_adjusted
                dev['y'] += dev['velocity'] * self.animation_speed

                # Check for floor collision with offset timing
                floor_y = 380 - dev['offset'] // 5  # Slight variation in floor level (adjusted for new canvas)
                if dev['y'] >= floor_y:
                    dev['y'] = floor_y
                    # Only bounce if we haven't reached max bounces
                    if self.bounce_count < self.max_bounces:
                        dev['velocity'] = bounce_force_adjusted + (dev['offset'] / 10)  # Variation in bounce
                        if i == 0:  # Only count bounces for the first developer
                            any_bounced = True
                    else:
                        # Stay on the floor after max bounces
                        dev['velocity'] = 0

                # Update developer position
                graphics = self.developer_graphics[i]
                self.canvas.coords(
                    graphics['body'],
                    dev['x'] - 20, dev['y'] - 20,
                    dev['x'] + 20, dev['y'] + 20
                )
                self.canvas.coords(
                    graphics['head'],
                    dev['x'] - 15, dev['y'] - 35,
                    dev['x'] + 15, dev['y'] - 5
                )

            if any_bounced:
                self.on_bounce()
        else:
            # Single developer animation
            self.developer_velocity += gravity_adjusted
            self.developer_y += self.developer_velocity * self.animation_speed

            # Check for floor collision
            floor_y = 380  # Floor position for the developer (adjusted for new canvas)
            if self.developer_y >= floor_y:
                self.developer_y = floor_y
                # Only bounce if we haven't reached max bounces
                if self.bounce_count < self.max_bounces:
                    self.developer_velocity = bounce_force_adjusted
                    self.on_bounce()
                else:
                    # Stay on the floor after max bounces
                    self.developer_velocity = 0

            # Update developer position
            self.canvas.coords(
                self.developer_body,
                self.developer_x - 20, self.developer_y - 20,
                self.developer_x + 20, self.developer_y + 20
            )
            self.canvas.coords(
                self.developer_head,
                self.developer_x - 15, self.developer_y - 35,
                self.developer_x + 15, self.developer_y - 5
            )

        # Update score popup animations
        self.update_score_popups()

        # Continue animation if still bouncing OR if there are floating bubbles
        if self.is_bouncing or len(self.floating_bubbles) > 0:
            self.window.after(self.animation_delay, self.animate)

    def on_bounce(self):
        """Handle bounce event - generate points and possibly bugs"""
        # Check if we've already completed all bounces
        if self.bounce_count >= self.max_bounces:
            print(f"[DEBUG] Ignoring extra bounce - already at max ({self.max_bounces})")
            return

        self.bounce_count += 1
        print(f"[DEBUG] Bounce {self.bounce_count}/{self.max_bounces} - Stage: {self.stage.value}")
        # Don't show exact count for suspense
        if self.bounce_count >= self.max_bounces:
            self.progress_label.config(text="All bounces complete!")
        else:
            encouraging_messages = [
                "Keep bouncing!",
                "More bouncing!",
                "Continue bouncing!",
                "Keep going!",
                "Don't stop!"
            ]
            self.progress_label.config(text=random.choice(encouraging_messages))

        # Reset index for scoring if needed
        if not hasattr(self, 'current_bounce_index'):
            self.current_bounce_index = 0

        # Generate points based on stage
        points = self.generate_stage_points()

        # Chance to generate bugs (including Planning stage!)
        if self.stage != DevelopmentStage.BUG_SQUASHING:
            # Higher chance in Planning stage for more chaos
            bug_chance = 0.20 if self.stage == DevelopmentStage.PLANNING else 0.15
            if random.random() < bug_chance:
                bugs_generated = random.randint(1, 3)
                self.stage_scores.bugs += bugs_generated
                points['bugs'] = bugs_generated
                print(f"[DEBUG] BUGS GENERATED! {bugs_generated} bugs created on bounce {self.bounce_count}")

                # Show bug notification on canvas
                bug_text = self.canvas.create_text(
                    400, 200,
                    text=f"⚠️ {bugs_generated} BUG{'S' if bugs_generated > 1 else ''} CREATED! ⚠️",
                    font=('Arial', 16, 'bold'),
                    fill='#FF0000',
                    tags='bug_notice'
                )
                # Remove after 2 seconds
                self.window.after(2000, lambda: self.canvas.delete(bug_text))

                # Update bug counter
                self.bug_label.config(text=f"Bugs: {self.stage_scores.bugs}")
        else:
            # Bug squashing removes bugs
            if self.stage_scores.bugs > 0:
                bugs_fixed = min(self.stage_scores.bugs, random.randint(2, 5))
                self.stage_scores.bugs -= bugs_fixed
                points['bugs'] = -bugs_fixed  # Negative to show removal
                self.bug_label.config(text=f"Bugs: {self.stage_scores.bugs}")

        # Update stage scores
        for category, value in points.items():
            if category != 'bugs':  # Handle bugs separately
                current = getattr(self.stage_scores, category)
                setattr(self.stage_scores, category, current + value)

            # Create floating bubbles for each point (including bugs)
            if value != 0 and category != 'bugs':
                # Create one bubble for each point
                for _ in range(abs(value)):
                    self.create_floating_bubble(category)

        # Check if complete
        if self.bounce_count >= self.max_bounces:
            print(f"[DEBUG] All bounces complete - waiting for bubbles to clear")
            self.is_bouncing = False
            # Start checking if all bubbles have reached their destinations
            self.check_for_completion()

    def generate_stage_points(self) -> Dict[str, int]:
        """Use pre-calculated points for this bounce"""
        # Get the pre-calculated score for this bounce
        if self.current_bounce_index < len(self.precalculated_scores):
            total_points = self.precalculated_scores[self.current_bounce_index]
            self.current_bounce_index += 1
        else:
            # Fallback if we somehow run out
            total_points = 2

        # Ensure minimum of 2 points per bounce
        total_points = max(2, total_points)

        # Initialize all categories to 0
        all_points = {
            'gameplay': 0,
            'technical': 0,
            'graphics': 0,
            'innovation': 0,
            'sound_audio': 0,
            'story': 0
        }

        # If we have 2 or fewer points, distribute them randomly
        if total_points <= 2:
            categories = list(all_points.keys())
            if total_points == 1:
                # Give 1 point to a random category
                chosen = random.choice(categories)
                all_points[chosen] = 1
            else:  # total_points == 2
                # Either give 2 to one category or 1 each to two categories
                if random.random() < 0.5:
                    # Give 2 points to one category
                    chosen = random.choice(categories)
                    all_points[chosen] = 2
                else:
                    # Give 1 point each to two different categories
                    chosen_cats = random.sample(categories, 2)
                    all_points[chosen_cats[0]] = 1
                    all_points[chosen_cats[1]] = 1
        else:
            # Use the normal distribution for higher point values
            points = self.score_calculator.distribute_points_to_categories(
                total_points,
                self.score_stage
            )
            # Update with actual points
            for category, value in points.items():
                all_points[category] = value

        return all_points

    def show_event_popup(self, event):
        """Show a popup for random events"""
        if hasattr(self, 'canvas'):
            # Create event notification on canvas
            event_text = self.canvas.create_text(
                400, 50,
                text=f"{event['name']}: {event['description']}",
                font=('Arial', 14, 'bold'),
                fill='#FFD700',
                tags='event'
            )
            # Remove after 3 seconds
            self.window.after(3000, lambda: self.canvas.delete(event_text))

    def create_floating_bubble(self, category: str):
        """Create a bubble that floats to the category header"""
        # Get starting position near developer
        if self.is_team_stage:
            dev = random.choice(self.team_developers)
            start_x = dev['x'] + random.randint(-20, 20)
            start_y = dev['y'] - 40
        else:
            start_x = self.developer_x + random.randint(-20, 20)
            start_y = self.developer_y - 40

        # Get target position (category header)
        if category in self.category_positions:
            target_x, target_y = self.category_positions[category]
        else:
            return  # Skip if category not found

        # Get color
        color = self.get_category_color(category)

        # Create bubble circle
        bubble = self.canvas.create_oval(
            start_x - 8, start_y - 8,
            start_x + 8, start_y + 8,
            fill=color,
            outline='white',
            width=1,
            tags='bubble'
        )

        # Add to floating bubbles list with increased speed and life
        self.floating_bubbles.append({
            'id': bubble,
            'x': start_x,
            'y': start_y,
            'target_x': target_x,
            'target_y': target_y,
            'category': category,
            'speed': 8.0,  # Increased from 3.0 for faster movement
            'life': 200  # Increased from 100 to give more time to reach target
        })

    def update_score_popups(self):
        """Update floating bubbles to move toward category headers"""
        # Check if window still exists
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            return

        to_remove = []

        # Update floating bubbles
        for bubble in self.floating_bubbles:
            # Calculate direction to target
            dx = bubble['target_x'] - bubble['x']
            dy = bubble['target_y'] - bubble['y']
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 5:
                # Normalize and apply speed
                bubble['x'] += (dx / distance) * bubble['speed'] * self.animation_speed
                bubble['y'] += (dy / distance) * bubble['speed'] * self.animation_speed

                # Update bubble position
                try:
                    self.canvas.coords(
                        bubble['id'],
                        bubble['x'] - 8, bubble['y'] - 8,
                        bubble['x'] + 8, bubble['y'] + 8
                    )
                except:
                    # Canvas item might be deleted already
                    print(f"[DEBUG] Failed to update bubble {bubble['id']} - removing")
                    to_remove.append(bubble)
            else:
                # Reached target - update score and remove
                if bubble['category'] in self.category_scores:
                    self.category_scores[bubble['category']] += 1
                    # Update score display
                    if bubble['category'] in self.category_labels:
                        self.canvas.itemconfig(
                            self.category_labels[bubble['category']],
                            text=str(self.category_scores[bubble['category']])
                        )

                self.canvas.delete(bubble['id'])
                to_remove.append(bubble)
                print(f"[DEBUG] Bubble reached target - {bubble['category']}")

            bubble['life'] -= 1
            if bubble['life'] <= 0:
                print(f"[DEBUG] Bubble expired - removing {bubble['category']}")
                self.canvas.delete(bubble['id'])
                to_remove.append(bubble)

        # Clean up removed bubbles
        for bubble in to_remove:
            if bubble in self.floating_bubbles:
                self.floating_bubbles.remove(bubble)

    def check_for_completion(self):
        """Check if all bubbles have reached their destinations before completing stage"""
        # Check if window still exists
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            return

        # If there are still bubbles floating, check again in 100ms
        if len(self.floating_bubbles) > 0:
            # Log details about stuck bubbles
            stuck_info = []
            for bubble in self.floating_bubbles[:3]:  # Just log first 3 to avoid spam
                dx = bubble['target_x'] - bubble['x']
                dy = bubble['target_y'] - bubble['y']
                distance = math.sqrt(dx**2 + dy**2)
                stuck_info.append(f"{bubble['category']}(dist:{distance:.1f},life:{bubble['life']})")

            print(f"[DEBUG] Waiting for {len(self.floating_bubbles)} bubbles: {', '.join(stuck_info)}")
            self.window.after(100, self.check_for_completion)
        else:
            # All bubbles have reached their destinations, show summary first
            print(f"[DEBUG] All bubbles cleared - showing summary")
            self.show_stage_summary()

    def show_stage_summary(self):
        """Show summary of scores on the existing canvas"""
        print(f"[DEBUG] show_stage_summary called for {self.stage.value}")

        # Check if window and canvas still exist
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            print(f"[DEBUG] Window doesn't exist, cannot show summary")
            return

        if not hasattr(self, 'canvas'):
            print(f"[DEBUG] Canvas doesn't exist, cannot show summary")
            return

        # Stop bouncing completely
        self.is_bouncing = False

        # Clear any remaining animations
        try:
            self.canvas.delete("bubble")
        except:
            print(f"[DEBUG] Failed to delete bubbles")

        # For Planning stage, show special planning complete screen
        if self.stage == DevelopmentStage.PLANNING:
            print(f"[DEBUG] Creating Planning stage summary")
            # Create semi-transparent overlay
            overlay = self.canvas.create_rectangle(
                0, 0, 800, 600,
                fill='#000000',
                stipple='gray50',
                tags='summary'
            )
            print(f"[DEBUG] Created overlay: {overlay}")

            # Create large summary box for planning complete
            summary_box = self.canvas.create_rectangle(
                100, 50, 700, 550,
                fill='#2a2a2a',
                outline='#4CAF50',
                width=3,
                tags='summary'
            )
            print(f"[DEBUG] Created summary box: {summary_box}")

            # Get game info - self.game_data is a GameData object, access .data
            if hasattr(self.game_data, 'data'):
                current_game = self.game_data.data.get('current_game', {})
            else:
                # self.game_data is already a dict
                current_game = self.game_data.get('current_game', {})

            game_name = current_game.get('name', 'Untitled Game')
            game_type = current_game.get('type', 'Unknown')
            topic = current_game.get('topic', 'Unknown')

            # Log what we're about to display
            print(f"\n" + "="*60)
            print("PLANNING SUMMARY - WHAT SHOULD BE DISPLAYED:")
            print("="*60)
            print(f"Game Name: {game_name.upper()}")
            print(f"Type/Topic: {game_type} - {topic}")
            print("Status: PLANNING COMPLETE")
            print("\nPLANNING SCORES:")

            # Large Game Name Title
            title_id = self.canvas.create_text(
                400, 100,
                text=game_name.upper(),
                font=('Arial', 28, 'bold'),
                fill='#FFD700',
                tags='summary'
            )
            print(f"[DEBUG] Created title text: {title_id}")

            # Game Type and Topic
            type_id = self.canvas.create_text(
                400, 135,
                text=f"{game_type} - {topic}",
                font=('Arial', 16),
                fill='#888888',
                tags='summary'
            )
            print(f"[DEBUG] Created type/topic text: {type_id}")

            # PLANNING COMPLETE text
            complete_id = self.canvas.create_text(
                400, 180,
                text="PLANNING COMPLETE",
                font=('Arial', 24, 'bold'),
                fill='#4CAF50',
                tags='summary'
            )
            print(f"[DEBUG] Created complete text: {complete_id}")

            # Divider line
            divider_id = self.canvas.create_line(
                150, 210, 650, 210,
                fill='#555555',
                width=2,
                tags='summary'
            )
            print(f"[DEBUG] Created divider: {divider_id}")

            # PLANNING SCORES header
            scores_header_id = self.canvas.create_text(
                400, 235,
                text="PLANNING SCORES",
                font=('Arial', 18, 'bold'),
                fill='white',
                tags='summary'
            )
            print(f"[DEBUG] Created scores header: {scores_header_id}")

            # Make sure window and canvas are visible
            self.window.lift()
            self.window.focus_force()
            self.canvas.update()
            print(f"[DEBUG] Summary should now be visible on canvas")
        else:
            # Original summary for other stages
            # Create semi-transparent overlay
            overlay = self.canvas.create_rectangle(
                0, 0, 800, 600,
                fill='#000000',
                stipple='gray50',
                tags='summary'
            )

            # Create summary box in center
            summary_box = self.canvas.create_rectangle(
                200, 150, 600, 450,
                fill='#2a2a2a',
                outline='#4CAF50',
                width=3,
                tags='summary'
            )

            # Title
            self.canvas.create_text(
                400, 180,
                text=f"{self.stage.value} Complete!",
                font=('Arial', 20, 'bold'),
                fill='#4CAF50',
                tags='summary'
            )

        # Display score boxes with values
        categories = [
            ('Gameplay', self.category_scores.get('gameplay', 0), '#FF6B6B'),
            ('Technical', self.category_scores.get('technical', 0), '#4ECDC4'),
            ('Graphics', self.category_scores.get('graphics', 0), '#45B7D1'),
            ('Innovation', self.category_scores.get('innovation', 0), '#96CEB4'),
            ('Sound', self.category_scores.get('sound_audio', 0), '#FECA57'),
            ('Story', self.category_scores.get('story', 0), '#DDA0DD')
        ]

        # Log the scores
        if self.stage == DevelopmentStage.PLANNING:
            for cat_name, score, color in categories:
                print(f"  {cat_name}: {score}")
            print(f"\nTOTAL PLANNING POINTS: {sum(self.category_scores.values())}")
            print("="*60 + "\n")

        # Different layouts for Planning vs other stages
        if self.stage == DevelopmentStage.PLANNING:
            # Larger score boxes for Planning stage
            x_start = 200
            y_start = 280
            box_width = 100
            box_height = 80
            spacing = 20
        else:
            # Original size for other stages
            x_start = 250
            y_start = 230
            box_width = 60
            box_height = 60
            spacing = 10

        for i, (category, score, color) in enumerate(categories):
            col = i % 3
            row = i // 3

            x = x_start + col * (box_width + spacing * 2) if not self.stage == DevelopmentStage.PLANNING else x_start + col * (box_width + spacing)
            y = y_start + row * (box_height + spacing * 2) if not self.stage == DevelopmentStage.PLANNING else y_start + row * (box_height + spacing)

            if self.stage == DevelopmentStage.PLANNING:
                # Larger, more detailed boxes for Planning stage
                # Score box with colored border
                self.canvas.create_rectangle(
                    x, y,
                    x + box_width, y + box_height,
                    fill='#3a3a3a',
                    outline=color,
                    width=3,
                    tags='summary'
                )

                # Category label at top
                self.canvas.create_text(
                    x + box_width // 2, y + 20,
                    text=category,
                    font=('Arial', 11),
                    fill='#cccccc',
                    tags='summary'
                )

                # Large score value
                self.canvas.create_text(
                    x + box_width // 2, y + 50,
                    text=str(score),
                    font=('Arial', 24, 'bold'),
                    fill=color,
                    tags='summary'
                )
            else:
                # Original style for other stages
                # Score box
                self.canvas.create_rectangle(
                    x, y,
                    x + box_width, y + box_height,
                    fill=color,
                    outline='white',
                    width=2,
                    tags='summary'
                )

                # Score value
                self.canvas.create_text(
                    x + box_width // 2, y + box_height // 2 - 5,
                    text=str(score),
                    font=('Arial', 18, 'bold'),
                    fill='white',
                    tags='summary'
                )

                # Category label
                self.canvas.create_text(
                    x + box_width // 2, y + box_height + 10,
                    text=category[:4],  # First 4 letters
                    font=('Arial', 9),
                    fill=color,
                    tags='summary'
                )

        # Total score
        total = sum(self.category_scores.values())

        if self.stage == DevelopmentStage.PLANNING:
            # Another divider for Planning stage
            self.canvas.create_line(
                150, 470, 650, 470,
                fill='#555555',
                width=2,
                tags='summary'
            )

            # Large total score display for Planning
            self.canvas.create_text(
                400, 495,
                text="TOTAL PLANNING POINTS",
                font=('Arial', 14),
                fill='#888888',
                tags='summary'
            )
            self.canvas.create_text(
                400, 525,
                text=str(total),
                font=('Arial', 32, 'bold'),
                fill='#4CAF50',
                tags='summary'
            )

            button_y = 510  # Moved down to not overlap with total score
            button_text = "CONTINUE"
            button_font = ('Arial', 18, 'bold')
            button_width = 15
            button_height = 2
            print(f"[DEBUG] Continue button will be placed at y={button_y}")
        else:
            # Original display for other stages
            self.canvas.create_text(
                400, 380,
                text=f"Total: {total} points",
                font=('Arial', 18, 'bold'),
                fill='#FFD700',
                tags='summary'
            )

            button_y = 420
            button_text = "▶ Continue"
            button_font = ('Arial', 14, 'bold')
            button_width = 20
            button_height = 1

        # Continue button frame
        button_frame = tk.Frame(self.window, bg='#2a2a2a')
        button_window = self.canvas.create_window(400, button_y, window=button_frame, tags='summary')

        # Continue button
        continue_btn = tk.Button(
            button_frame,
            text=button_text,
            font=button_font,
            bg='#4CAF50',
            fg='white',
            activebackground='#5CBF60',
            width=button_width,
            height=button_height,
            command=lambda: self.proceed_from_summary()
        )
        continue_btn.pack()

        print(f"[DEBUG] Created continue button window: {button_window}")

        # Force canvas to update to ensure all items are rendered
        self.canvas.update_idletasks()

        # List all canvas items to verify they exist
        all_items = self.canvas.find_withtag('summary')
        print(f"[DEBUG] Total summary items on canvas: {len(all_items)}")

    def proceed_from_summary(self):
        """Clear summary and proceed to next stage"""
        print("\n" + "="*60)
        print("[CONTINUE BUTTON PRESSED]")

        if self.stage == DevelopmentStage.PLANNING:
            # Get game info properly
            if hasattr(self.game_data, 'data'):
                current_game = self.game_data.data.get('current_game', {})
            else:
                current_game = self.game_data.get('current_game', {})

            game_type = current_game.get('type', 'Unknown')
            game_topic = current_game.get('topic', 'Unknown')
            game_name = current_game.get('name', 'Unknown')

            print(f"Stage: {self.stage.value}")
            print(f"Planning complete for: {game_name}")
            print(f"Game Type: {game_type}")
            print(f"Topic: {game_topic}")
            print(f"Total Score: {sum(self.category_scores.values())}")
            print(f"Bugs Generated: {self.stage_scores.bugs}")
            print("\nScore Breakdown:")
            for category, score in self.category_scores.items():
                if score > 0:
                    print(f"  {category}: {score}")
            print(f"\nAction: Launching {game_type} minigame...")
            print("="*60 + "\n")

            # Clear summary elements
            self.canvas.delete("summary")

            # Launch minigame
            self.launch_minigame(game_type, game_topic)
        else:
            # Clear summary elements
            self.canvas.delete("summary")
            # Now complete the stage
            self.complete_stage()

    def complete_stage(self):
        """Complete the current stage"""
        # Show completion screen for Planning stage
        if self.stage == DevelopmentStage.PLANNING:
            self.show_planning_complete_screen()
        else:
            # For other stages, proceed as normal
            self.finish_stage_completion()

    def show_planning_complete_screen(self):
        """Show the planning complete screen with scores and continue button"""
        # Clear the canvas
        self.canvas.delete("all")

        # Dark background
        self.canvas.configure(bg='#1a1a1a')

        # Get game info if available
        game_name = self.game_data.get('current_game', {}).get('name', 'Untitled Game')
        game_type = self.game_data.get('current_game', {}).get('type', 'Unknown')
        game_topic = self.game_data.get('current_game', {}).get('topic', 'Unknown')

        # Title - Game Name
        self.canvas.create_text(
            400, 80,
            text=game_name,
            font=('Arial', 32, 'bold'),
            fill='#4CAF50',
            tags='complete'
        )

        # Stage Complete text
        self.canvas.create_text(
            400, 130,
            text="PLANNING COMPLETE",
            font=('Arial', 24, 'bold'),
            fill='white',
            tags='complete'
        )

        # Scores header
        self.canvas.create_text(
            400, 180,
            text="Planning Scores:",
            font=('Arial', 18, 'bold'),
            fill='#FFC107',
            tags='complete'
        )

        # Display scores
        score_y = 220
        categories = [
            ('Gameplay', self.category_scores.get('gameplay', 0), '#FF6B6B'),
            ('Technical', self.category_scores.get('technical', 0), '#4ECDC4'),
            ('Graphics', self.category_scores.get('graphics', 0), '#45B7D1'),
            ('Innovation', self.category_scores.get('innovation', 0), '#96CEB4'),
            ('Sound/Audio', self.category_scores.get('sound_audio', 0), '#FECA57'),
            ('Story', self.category_scores.get('story', 0), '#DDA0DD')
        ]

        for category, score, color in categories:
            self.canvas.create_text(
                300, score_y,
                text=f"{category}:",
                font=('Arial', 14),
                fill=color,
                anchor='e',
                tags='complete'
            )
            self.canvas.create_text(
                320, score_y,
                text=str(score),
                font=('Arial', 16, 'bold'),
                fill='white',
                anchor='w',
                tags='complete'
            )
            score_y += 30

        # Total score
        total = sum(self.category_scores.values())
        self.canvas.create_text(
            400, score_y + 20,
            text=f"Total Points: {total}",
            font=('Arial', 20, 'bold'),
            fill='#4CAF50',
            tags='complete'
        )

        # Continue button frame
        button_frame = tk.Frame(self.window, bg='#1a1a1a')
        button_window = self.canvas.create_window(400, 480, window=button_frame, tags='complete')

        # Continue button
        continue_btn = tk.Button(
            button_frame,
            text="▶ Continue to Development",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#5CBF60',
            width=25,
            height=2,
            command=lambda: self.launch_minigame(game_type, game_topic)
        )
        continue_btn.pack(pady=10)

        # Skip minigame button (for testing)
        skip_btn = tk.Button(
            button_frame,
            text="Skip Minigame",
            font=('Arial', 10),
            bg='#666666',
            fg='white',
            command=self.finish_stage_completion
        )
        skip_btn.pack(pady=5)

    def launch_minigame(self, game_type: str, game_topic: str):
        """Launch the appropriate minigame based on game type and topic"""
        print("\n" + "="*60)
        print(f"[MINIGAME] Launching Development Minigame")
        print(f"[MINIGAME] Game Type: {game_type}")
        print(f"[MINIGAME] Topic: {game_topic}")
        print(f"[MINIGAME] Planning Score: {sum(self.category_scores.values())}")
        print("="*60 + "\n")

        # Prepare GameEndManager with current scores
        manager = GameEndManager()
        current_gtgiss = GTGISSScores(
            gameplay=self.category_scores.get('gameplay', 0),
            technical=self.category_scores.get('technical', 0),
            graphics=self.category_scores.get('graphics', 0),
            innovation=self.category_scores.get('innovation', 0),
            sound=self.category_scores.get('sound_audio', 0),
            story=self.category_scores.get('story', 0)
        )

        # Get game name
        if hasattr(self.game_data, 'data'):
            current_game = self.game_data.data.get('current_game', {})
        else:
            current_game = self.game_data.get('current_game', {})
        game_name = current_game.get('name', 'Untitled Game')

        manager.set_game_info(game_name, game_type, game_topic, current_gtgiss)

        try:
            import subprocess
            import sys
            import os

            # Map game type + topic combinations to specific minigames
            minigame_path = None

            if game_type.lower() == "arcade":
                # Map arcade topics to their games
                if "table tennis" in game_topic.lower():
                    minigame_path = "DevelopmentGames/arcade/TableTennisArcade.py"
                    print(f"[MINIGAME] Selected: Table Tennis Arcade")
                elif "temple" in game_topic.lower():
                    minigame_path = "DevelopmentGames/arcade/TempleArcade.py"
                    print(f"[MINIGAME] Selected: Temple Arcade")
                elif "space" in game_topic.lower():
                    # Check if SpaceArcade exists, otherwise use TempleArcade
                    if os.path.exists("DevelopmentGames/arcade/SpaceArcade.py"):
                        minigame_path = "DevelopmentGames/arcade/SpaceArcade.py"
                        print(f"[MINIGAME] Selected: Space Arcade")
                    else:
                        minigame_path = "DevelopmentGames/arcade/TempleArcade.py"
                        print(f"[MINIGAME] Space game not found, using Temple Arcade")
                elif "bugs" in game_topic.lower() or "bug" in game_topic.lower():
                    # Use BugsArcade for bug-themed games
                    if os.path.exists("DevelopmentGames/arcade/BugsArcade.py"):
                        minigame_path = "DevelopmentGames/arcade/BugsArcade.py"
                        print(f"[MINIGAME] Selected: Bugs Arcade (Centipede-style)")
                    else:
                        minigame_path = "DevelopmentGames/arcade/TempleArcade.py"
                        print(f"[MINIGAME] Bugs game not found, using Temple Arcade")
                else:
                    # Default arcade game
                    minigame_path = "DevelopmentGames/arcade/TempleArcade.py"
                    print(f"[MINIGAME] No specific match, using Temple Arcade")

                if minigame_path and os.path.exists(minigame_path):
                    print(f"[MINIGAME] Launching: {minigame_path}")
                    # Hide current window while minigame runs
                    if hasattr(self, 'window') and self.window:
                        self.window.withdraw()

                    # Run minigame
                    result = subprocess.run(
                        [sys.executable, minigame_path],
                        capture_output=False,  # Let it show its own window
                        text=True
                    )

                    # Show window again
                    if hasattr(self, 'window') and self.window:
                        self.window.deiconify()

                    # The minigame will handle its own scoring via GameEndManager
                    # Set callback to receive updated scores
                    manager.return_callback = self.on_minigame_scores_updated

                    # For now, continue directly
                    self.finish_stage_completion()
                else:
                    print(f"[MINIGAME] File not found: {minigame_path}")
                    self.distribute_minigame_score_to_gtgiss(30)  # Default score

            elif game_type.lower() in ["text adventure", "adventure"]:
                # Launch DeepAdventure as a subprocess
                print(f"[MINIGAME] Starting Text Adventure for topic: {game_topic}")
                minigame_path = "DevelopmentGames/textadventure/DeepAdventure.py"

                if os.path.exists(minigame_path):
                    print(f"[MINIGAME] Launching: {minigame_path}")
                    # Pass topic as command line argument
                    result = subprocess.run(
                        [sys.executable, minigame_path, "--topic", game_topic],
                        capture_output=True,
                        text=True
                    )
                    # Parse score from output or use default
                    score = self.parse_minigame_score(result.stdout)
                    print(f"[MINIGAME] Completed with score: {score}")
                    self.distribute_minigame_score_to_gtgiss(score)
                else:
                    print(f"[MINIGAME] File not found: {minigame_path}")
                    self.distribute_minigame_score_to_gtgiss(30)  # Default score

            else:
                # No minigame for this type yet
                print(f"[DEBUG] No minigame available for {game_type}")
                self.finish_stage_completion()

        except Exception as e:
            print(f"[ERROR] Failed to launch minigame: {e}")
            self.finish_stage_completion()

    def parse_minigame_score(self, output: str) -> int:
        """Parse score from minigame output"""
        # Look for "SCORE:" or "Final Score:" in output
        import re
        score_patterns = [
            r"SCORE:\s*(\d+)",
            r"Final Score:\s*(\d+)",
            r"Score:\s*(\d+)",
            r"Points:\s*(\d+)"
        ]

        for pattern in score_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                print(f"[MINIGAME] Parsed score from output: {score}")
                return score

        print(f"[MINIGAME] No score found in output, using default")
        return 30  # Default score if not found

    def on_minigame_scores_updated(self, updated_scores: GTGISSScores):
        """Handle updated scores from minigame"""
        print(f"\n[MINIGAME] Received updated scores from GameEndManager")

        # Update our category scores
        self.category_scores['gameplay'] = updated_scores.gameplay
        self.category_scores['technical'] = updated_scores.technical
        self.category_scores['graphics'] = updated_scores.graphics
        self.category_scores['innovation'] = updated_scores.innovation
        self.category_scores['sound_audio'] = updated_scores.sound
        self.category_scores['story'] = updated_scores.story

        print(f"[MINIGAME] New total score: {sum(self.category_scores.values())}\n")

        # Update stage scores as well
        self.stage_scores.gameplay = updated_scores.gameplay
        self.stage_scores.technical = updated_scores.technical
        self.stage_scores.graphics = updated_scores.graphics
        self.stage_scores.innovation = updated_scores.innovation
        self.stage_scores.sound_audio = updated_scores.sound
        self.stage_scores.story = updated_scores.story

        # Continue with stage completion
        if hasattr(self, 'window') and self.window:
            self.window.deiconify()
        self.finish_stage_completion()

    def on_minigame_complete(self, minigame_score: int):
        """Handle minigame completion"""
        print(f"[DEBUG] Minigame complete with score: {minigame_score}")
        self.distribute_minigame_score_to_gtgiss(minigame_score)

    def finish_stage_completion(self):
        """Finish the stage completion process"""
        # Advance time by 1 week if this is the planning stage
        if self.stage == DevelopmentStage.PLANNING:
            from systems.game_systems import TimeSystem
            time_system = TimeSystem(self.game_data)
            # Advance by 1 week (7 days * 24 hours)
            time_system.advance_time(7 * 24)

        if self.on_complete:
            self.on_complete(self.stage_scores)

        # Close window
        self.window.destroy()


class MultiStageDevelopment:
    """Manages the full multi-stage development process"""

    def __init__(self, root, game_data, game_name: str, game_type: str, game_topic: str, preloaded_adventure_data=None):
        self.root = root
        self.game_data = game_data
        self.game_name = game_name
        self.game_type = game_type
        self.game_topic = game_topic
        self.preloaded_adventure_data = preloaded_adventure_data

        # Total scores across all stages
        self.total_scores = StageScores()

        # Track total bugs accumulated
        self.total_bugs = 0

        # Current stage
        self.current_stage_index = 0
        self.stages = list(DevelopmentStage)

        # Start first stage
        self.start_next_stage()

    def start_next_stage(self):
        """Start the next development stage"""
        if self.current_stage_index >= len(self.stages):
            # All stages complete
            self.finish_development()
            return

        current_stage = self.stages[self.current_stage_index]

        # Bug Squashing doesn't need developer selection - uses all team
        if current_stage == DevelopmentStage.BUG_SQUASHING:
            self.start_bug_squashing_stage()
        else:
            # Show developer selection window for other stages
            self.show_developer_selection(current_stage)

    def show_developer_selection(self, stage: DevelopmentStage):
        """Show window to select developer for this stage"""
        selection_window = tk.Toplevel(self.root)
        selection_window.title(f"Select Developer for {stage.value}")
        selection_window.geometry("400x300")
        selection_window.configure(bg='#1a1a1a')

        # Center window
        selection_window.update_idletasks()
        x = (selection_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (selection_window.winfo_screenheight() // 2) - (300 // 2)
        selection_window.geometry(f"400x300+{x}+{y}")

        # Title
        title = tk.Label(
            selection_window,
            text=f"{stage.value} Stage",
            font=('Arial', 18, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack(pady=20)

        # Description
        descriptions = {
            DevelopmentStage.PLANNING: "Planning focuses on Gameplay, Innovation, and Story. Choose your lead designer to shape the game's core concepts.",
            DevelopmentStage.DEVELOPMENT: "Development focuses on Technical and Graphics. Choose your lead programmer to build the game's foundation.",
            DevelopmentStage.PRODUCTION: "Production focuses on Sound and Story. Choose your lead artist to polish the experience.",
            DevelopmentStage.BUG_SQUASHING: "Bug Squashing improves Technical quality and Gameplay. The entire team works together to fix issues."
        }

        desc_label = tk.Label(
            selection_window,
            text=descriptions.get(stage, ""),
            font=('Arial', 10),
            fg='#888888',
            bg='#1a1a1a',
            wraplength=350
        )
        desc_label.pack(pady=10)

        # Developer selection
        dev_frame = tk.Frame(selection_window, bg='#1a1a1a')
        dev_frame.pack(pady=20)

        tk.Label(
            dev_frame,
            text="Lead Developer:",
            font=('Arial', 12),
            fg='white',
            bg='#1a1a1a'
        ).grid(row=0, column=0, padx=10, sticky='w')

        # Developer dropdown (for now just player)
        dev_var = tk.StringVar(value="You (Player)")
        dev_dropdown = ttk.Combobox(
            dev_frame,
            textvariable=dev_var,
            values=["You (Player)"],  # Will expand with hired developers
            state='readonly',
            width=20
        )
        dev_dropdown.grid(row=0, column=1, padx=10)

        # Start button
        def start_stage():
            developer = dev_var.get()
            selection_window.destroy()

            # Get or create developer stats
            developer_stats = create_player_developer() if developer == "You (Player)" else DeveloperStats(name=developer)

            # Update game_data with current game information
            if hasattr(self.game_data, 'data'):
                self.game_data.data['current_game'] = {
                    'name': self.game_name,
                    'type': self.game_type,
                    'topic': self.game_topic
                }
                # Store preloaded adventure data if available
                if self.preloaded_adventure_data:
                    self.game_data.data['preloaded_adventure_data'] = self.preloaded_adventure_data
            else:
                self.game_data['current_game'] = {
                    'name': self.game_name,
                    'type': self.game_type,
                    'topic': self.game_topic
                }
                # Store preloaded adventure data if available
                if self.preloaded_adventure_data:
                    self.game_data['preloaded_adventure_data'] = self.preloaded_adventure_data

            # Create stage window with animation
            stage_window = DevelopmentStageWindow(
                self.root,
                self.game_data,
                stage,
                developer,
                developer_stats=developer_stats,
                on_complete=self.on_stage_complete
            )

        start_btn = tk.Button(
            selection_window,
            text=f"Start {stage.value}",
            command=start_stage,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10
        )
        start_btn.pack(pady=20)

        # Skip button (for testing)
        skip_btn = tk.Button(
            selection_window,
            text="Skip Stage",
            command=lambda: self.skip_stage(selection_window),
            font=('Arial', 10),
            bg='#666666',
            fg='white'
        )
        skip_btn.pack()

    def start_bug_squashing_stage(self):
        """Start bug squashing stage with all available developers"""
        # For now, use "Entire Team" as the developer name
        # In the future, this would list all hired developers
        developer_name = "Entire Team"

        # For bug squashing, use average team stats
        team_stats = create_player_developer()
        team_stats.name = "Entire Team"
        # Could average multiple developers here in the future

        # Update game_data with current game information
        if hasattr(self.game_data, 'data'):
            self.game_data.data['current_game'] = {
                'name': self.game_name,
                'type': self.game_type,
                'topic': self.game_topic
            }
        else:
            self.game_data['current_game'] = {
                'name': self.game_name,
                'type': self.game_type,
                'topic': self.game_topic
            }

        # Create stage window directly without selection
        stage_window = DevelopmentStageWindow(
            self.root,
            self.game_data,
            DevelopmentStage.BUG_SQUASHING,
            developer_name,
            developer_stats=team_stats,
            on_complete=self.on_stage_complete
        )

    def skip_stage(self, window):
        """Skip current stage (for testing)"""
        print(f"[DEBUG] Skip Stage button clicked - skipping {self.stage.value}")
        window.destroy()
        # Generate minimal points
        scores = StageScores()
        scores.gameplay = random.randint(5, 10)
        scores.technical = random.randint(5, 10)
        self.on_stage_complete(scores)

    def on_stage_complete(self, stage_scores: StageScores):
        """Handle completion of a development stage"""
        # Add stage scores to total
        self.total_scores.gameplay += stage_scores.gameplay
        self.total_scores.technical += stage_scores.technical
        self.total_scores.graphics += stage_scores.graphics
        self.total_scores.innovation += stage_scores.innovation
        self.total_scores.sound_audio += stage_scores.sound_audio
        self.total_scores.story += stage_scores.story

        # Track bugs - carry over to next stage or final count
        self.total_scores.bugs = stage_scores.bugs

        # If this was bug squashing, apply bug penalty to final scores
        if self.current_stage_index == len(self.stages) - 1:  # Last stage (bug squashing)
            # Each remaining bug reduces technical score
            if self.total_scores.bugs > 0:
                bug_penalty = self.total_scores.bugs * 2
                self.total_scores.technical = max(0, self.total_scores.technical - bug_penalty)

        # After Planning stage, show IDE
        if self.current_stage_index == 0:  # Just completed Planning (index 0)
            self.show_ide()
        else:
            # Move to next stage
            self.current_stage_index += 1
            self.start_next_stage()

    def show_ide(self):
        """Show the IDE interface after planning stage"""
        from desktop.ide_interface import IDEInterface

        # Create IDE window
        ide = IDEInterface(
            self.root,
            self.game_data,
            on_back=self.on_ide_close
        )

    def on_ide_close(self):
        """Called when IDE is closed"""
        # Move to next stage
        self.current_stage_index += 1
        self.start_next_stage()

    def finish_development(self):
        """Complete the development process and show results"""
        # Import here to avoid circular imports
        from systems.game_development import GameDevelopment, GameScore

        # Convert StageScores to GameScore
        final_score = GameScore(
            gameplay=self.total_scores.gameplay,
            technical=self.total_scores.technical,
            graphics=self.total_scores.graphics,
            innovation=self.total_scores.innovation,
            sound_audio=self.total_scores.sound_audio,
            story=self.total_scores.story
        )

        # Get rating
        game_dev = GameDevelopment(self.game_data)
        rating = game_dev.get_game_rating(final_score)
        description = game_dev.get_rating_description(rating)

        # Show results window
        self.show_results(final_score, rating, description)

    def show_results(self, score, rating, description):
        """Show the final game development results"""
        results_window = tk.Toplevel(self.root)
        results_window.title("Development Complete!")
        results_window.geometry("600x700")
        results_window.configure(bg='#1a1a1a')

        # Center window
        results_window.update_idletasks()
        x = (results_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (results_window.winfo_screenheight() // 2) - (700 // 2)
        results_window.geometry(f"600x700+{x}+{y}")

        # Title
        title = tk.Label(
            results_window,
            text="Game Development Complete!",
            font=('Arial', 20, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack(pady=20)

        # Game name
        name_label = tk.Label(
            results_window,
            text=f'"{self.game_name}"',
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#1a1a1a'
        )
        name_label.pack()

        # Type and topic
        info_label = tk.Label(
            results_window,
            text=f"{self.game_type} - {self.game_topic}",
            font=('Arial', 12),
            fg='#888888',
            bg='#1a1a1a'
        )
        info_label.pack(pady=5)

        # Rating
        rating_colors = {
            'Masterpiece': '#FFD700',
            'Legendary': '#FF6B35',
            'Outstanding': '#9C27B0',
            'Excellent': '#2196F3',
            'Notable': '#4CAF50',
            'Good': '#8BC34A',
            'Fun': '#CDDC39',
            'Decent': '#FFC107',
            'Meh': '#FF9800',
            'Poor': '#F44336'
        }

        rating_label = tk.Label(
            results_window,
            text=rating.value,
            font=('Arial', 24, 'bold'),
            fg=rating_colors.get(rating.value, 'white'),
            bg='#1a1a1a'
        )
        rating_label.pack(pady=10)

        # Description
        desc_label = tk.Label(
            results_window,
            text=description,
            font=('Arial', 10),
            fg='#aaaaaa',
            bg='#1a1a1a',
            wraplength=500
        )
        desc_label.pack(pady=10)

        # Scores frame
        scores_frame = tk.Frame(results_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        scores_frame.pack(pady=20, padx=40, fill='x')

        tk.Label(
            scores_frame,
            text="Final Scores",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=10)

        # Individual scores
        categories = [
            ('Gameplay', score.gameplay),
            ('Technical', score.technical),
            ('Graphics', score.graphics),
            ('Innovation', score.innovation),
            ('Sound/Audio', score.sound_audio),
            ('Story', score.story)
        ]

        for category, value in categories:
            self.create_score_bar(scores_frame, category, value)

        # Total score and bugs
        total_frame = tk.Frame(results_window, bg='#1a1a1a')
        total_frame.pack(pady=20)

        tk.Label(
            total_frame,
            text="Total Score:",
            font=('Arial', 14),
            fg='white',
            bg='#1a1a1a'
        ).pack(side='left', padx=10)

        tk.Label(
            total_frame,
            text=str(score.total),
            font=('Arial', 18, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        ).pack(side='left')

        # Show remaining bugs if any
        if self.total_scores.bugs > 0:
            tk.Label(
                total_frame,
                text=f"   Remaining Bugs: {self.total_scores.bugs}",
                font=('Arial', 12),
                fg='#F44336',
                bg='#1a1a1a'
            ).pack(side='left', padx=20)

        # OK button
        ok_btn = tk.Button(
            results_window,
            text="OK",
            command=results_window.destroy,
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            padx=30,
            pady=10
        )
        ok_btn.pack(pady=20)

    def create_score_bar(self, parent, category, value):
        """Create a visual score bar"""
        frame = tk.Frame(parent, bg='#2a2a2a')
        frame.pack(fill='x', padx=20, pady=5)

        # Label
        label = tk.Label(
            frame,
            text=f"{category}:",
            font=('Arial', 10),
            fg='white',
            bg='#2a2a2a',
            width=12,
            anchor='w'
        )
        label.pack(side='left')

        # Progress bar
        bar_frame = tk.Frame(frame, bg='#444444', height=20, width=200)
        bar_frame.pack(side='left', padx=10)
        bar_frame.pack_propagate(False)

        # Calculate bar width (max 40 points for display)
        bar_width = min(200, int((value / 40) * 200))

        # Color based on score
        if value >= 30:
            color = '#4CAF50'
        elif value >= 20:
            color = '#FFC107'
        elif value >= 10:
            color = '#FF9800'
        else:
            color = '#F44336'

        bar = tk.Frame(bar_frame, bg=color, height=20, width=bar_width)
        bar.pack(side='left')

        # Value label
        value_label = tk.Label(
            frame,
            text=str(value),
            font=('Arial', 10, 'bold'),
            fg=color,
            bg='#2a2a2a',
            width=5
        )
        value_label.pack(side='left')