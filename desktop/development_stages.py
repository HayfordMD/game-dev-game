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
        """Show pre-bounce calculation menu on the side"""
        self.calc_window = tk.Toplevel(self.root)
        self.calc_window.title(f"{self.stage.value} - Bounce Calculation")
        self.calc_window.geometry("400x800")
        self.calc_window.configure(bg='#1a1a1a')

        # Position on the left side of the screen
        self.calc_window.update_idletasks()
        x = 50  # Left side
        y = (self.calc_window.winfo_screenheight() // 2) - (400)
        self.calc_window.geometry(f"400x800+{x}+{y}")

        # Title
        title = tk.Label(
            self.calc_window,
            text="Developer Performance Analysis",
            font=('Arial', 18, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack(pady=20)

        # Developer name
        dev_label = tk.Label(
            self.calc_window,
            text=f"Developer: {self.developer_name}",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#1a1a1a'
        )
        dev_label.pack()

        # Skills breakdown frame
        skills_frame = tk.Frame(self.calc_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        skills_frame.pack(pady=20, padx=40, fill='x')

        tk.Label(
            skills_frame,
            text="Skill Breakdown",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=10)

        # Show each skill
        for skill_name, skill_value in self.bounce_details['skills'].items():
            self.create_skill_bar(skills_frame, skill_name.title(), skill_value)

        # Composite score section
        composite_frame = tk.Frame(self.calc_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        composite_frame.pack(pady=20, padx=40, fill='x')

        tk.Label(
            composite_frame,
            text=f"Composite Score: {self.bounce_details['composite_score']}/{self.bounce_details['max_score']}",
            font=('Arial', 14, 'bold'),
            fg='#4CAF50',
            bg='#2a2a2a'
        ).pack(pady=10)

        tk.Label(
            composite_frame,
            text=f"Performance Level: {self.bounce_details['percentage']:.1f}%",
            font=('Arial', 12),
            fg='white',
            bg='#2a2a2a'
        ).pack()

        tk.Label(
            composite_frame,
            text=f"Weighted Skill: {self.weighted_skill:.1f}/100",
            font=('Arial', 11),
            fg='#888888',
            bg='#2a2a2a'
        ).pack()

        # Pre-calculated scores preview
        tk.Label(
            composite_frame,
            text=f"Pre-calculated: {self.precalculated_scores}",
            font=('Arial', 9),
            fg='#666666',
            bg='#2a2a2a'
        ).pack(pady=5)

        tk.Label(
            composite_frame,
            text=f"Expected Avg: {sum(self.precalculated_scores)/len(self.precalculated_scores):.1f} pts/bounce",
            font=('Arial', 10),
            fg='#FFC107',
            bg='#2a2a2a'
        ).pack()

        # Bounce calculation frame
        bounce_frame = tk.Frame(self.calc_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        bounce_frame.pack(pady=20, padx=40, fill='x')

        tk.Label(
            bounce_frame,
            text="Bounce Calculation",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=10)

        # Expected vs Actual
        tk.Label(
            bounce_frame,
            text=f"Expected Bounces: {self.bounce_details['expected_bounces']}",
            font=('Arial', 11),
            fg='#888888',
            bg='#2a2a2a'
        ).pack(pady=2)

        # Actual bounces with color based on luck
        bounce_color = '#4CAF50' if self.bounce_details['luck_factor'] == 'Lucky!' else '#F44336' if self.bounce_details['luck_factor'] == 'Unlucky' else '#FFC107'

        tk.Label(
            bounce_frame,
            text=f"Actual Bounces: {self.bounce_details['actual_bounces']}",
            font=('Arial', 14, 'bold'),
            fg=bounce_color,
            bg='#2a2a2a'
        ).pack(pady=5)

        tk.Label(
            bounce_frame,
            text=f"Percentile: {self.bounce_details['percentile']:.1f}%",
            font=('Arial', 11),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=2)

        tk.Label(
            bounce_frame,
            text=self.bounce_details['luck_factor'],
            font=('Arial', 12, 'bold'),
            fg=bounce_color,
            bg='#2a2a2a'
        ).pack(pady=5)

        # Bell curve visualization
        curve_frame = tk.Frame(self.calc_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        curve_frame.pack(pady=15, padx=20, fill='x')

        tk.Label(
            curve_frame,
            text="Bell Curve Distribution",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=5)

        # Create canvas for bell curve
        curve_canvas = tk.Canvas(
            curve_frame,
            width=350,
            height=150,
            bg='#1a1a1a',
            highlightthickness=0
        )
        curve_canvas.pack(pady=10)

        # Draw bell curve
        self.draw_bell_curve(curve_canvas, self.bounce_details)

        # Visual bounce indicator
        visual_frame = tk.Frame(self.calc_window, bg='#1a1a1a')
        visual_frame.pack(pady=10)

        # Create two rows for 10 bounces
        for i in range(10):
            row = 0 if i < 5 else 1
            col = i if i < 5 else i - 5

            color = '#4CAF50' if i < self.max_bounces else '#333333'
            bounce_indicator = tk.Frame(
                visual_frame,
                width=35,
                height=35,
                bg=color,
                relief=tk.RAISED if i < self.max_bounces else tk.SUNKEN,
                bd=2
            )
            bounce_indicator.grid(row=row, column=col, padx=3, pady=3)

            tk.Label(
                bounce_indicator,
                text=str(i+1),
                font=('Arial', 9, 'bold'),
                fg='white' if i < self.max_bounces else '#666666',
                bg=color
            ).place(relx=0.5, rely=0.5, anchor='center')

        # Auto-start message
        tk.Label(
            self.calc_window,
            text="Development Starting...",
            font=('Arial', 12, 'italic'),
            fg='#4CAF50',
            bg='#1a1a1a'
        ).pack(pady=20)

        # Start the stage automatically after short delay
        self.calc_window.after(500, self.start_stage)

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
        """Start the stage while keeping calculation window open on the side"""
        # Don't destroy calc_window - keep it visible

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

        # Progress label
        self.progress_label = tk.Label(
            controls_frame,
            text=f"Bounce: 0/{self.max_bounces}",
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
        self.animation_speed = speed
        # Adjust animation delay inversely (faster speed = shorter delay)
        self.animation_delay = max(5, int(20 / speed))  # Min 5ms delay

    def start_animation(self):
        """Start the bouncing animation"""
        self.animate()

    def animate(self):
        """Main animation loop"""
        if not self.is_bouncing:
            return

        # Check if window still exists
        if not hasattr(self, 'window') or not self.window.winfo_exists():
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
                    dev['velocity'] = bounce_force_adjusted + (dev['offset'] / 10)  # Variation in bounce
                    if i == 0:  # Only count bounces for the first developer
                        any_bounced = True

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
                self.developer_velocity = bounce_force_adjusted
                self.on_bounce()

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

        # Continue animation with adjusted delay
        if self.is_bouncing:
            self.window.after(self.animation_delay, self.animate)

    def on_bounce(self):
        """Handle bounce event - generate points and possibly bugs"""
        self.bounce_count += 1
        self.progress_label.config(text=f"Bounce: {self.bounce_count}/{self.max_bounces}")

        # Reset index for scoring if needed
        if not hasattr(self, 'current_bounce_index'):
            self.current_bounce_index = 0

        # Generate points based on stage
        points = self.generate_stage_points()

        # Chance to generate bugs (except during bug squashing)
        if self.stage != DevelopmentStage.BUG_SQUASHING:
            bug_chance = 0.15  # 15% chance per bounce
            if random.random() < bug_chance:
                bugs_generated = random.randint(1, 3)
                self.stage_scores.bugs += bugs_generated
                points['bugs'] = bugs_generated
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
            total_points = 1

        # Distribute points to appropriate categories
        points = self.score_calculator.distribute_points_to_categories(
            total_points,
            self.score_stage
        )

        # Initialize all categories to 0
        all_points = {
            'gameplay': 0,
            'technical': 0,
            'graphics': 0,
            'innovation': 0,
            'sound_audio': 0,
            'story': 0
        }

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

        # Add to floating bubbles list
        self.floating_bubbles.append({
            'id': bubble,
            'x': start_x,
            'y': start_y,
            'target_x': target_x,
            'target_y': target_y,
            'category': category,
            'speed': 3.0,
            'life': 100
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
                self.canvas.coords(
                    bubble['id'],
                    bubble['x'] - 8, bubble['y'] - 8,
                    bubble['x'] + 8, bubble['y'] + 8
                )
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

            bubble['life'] -= 1
            if bubble['life'] <= 0:
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
            self.window.after(100, self.check_for_completion)
        else:
            # All bubbles have reached their destinations, wait a bit then complete
            self.window.after(500, self.complete_stage)

    def complete_stage(self):
        """Complete the current stage"""
        # Advance time by 1 week if this is the planning stage
        if self.stage == DevelopmentStage.PLANNING:
            from systems.game_systems import TimeSystem
            time_system = TimeSystem(self.game_data)
            # Advance by 1 week (7 days * 24 hours)
            time_system.advance_time(7 * 24)

        if self.on_complete:
            self.on_complete(self.stage_scores)

        # Close both windows
        if hasattr(self, 'calc_window') and self.calc_window:
            try:
                self.calc_window.destroy()
            except:
                pass
        self.window.destroy()


class MultiStageDevelopment:
    """Manages the full multi-stage development process"""

    def __init__(self, root, game_data, game_name: str, game_type: str, game_topic: str):
        self.root = root
        self.game_data = game_data
        self.game_name = game_name
        self.game_type = game_type
        self.game_topic = game_topic

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