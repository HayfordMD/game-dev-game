"""
Drum Rhythm Game - A simple 4-lane rhythm game using WASD keys
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Lane configuration
LANE_WIDTH = 100
LANE_COUNT = 4
LANES_START_X = (SCREEN_WIDTH - (LANE_WIDTH * LANE_COUNT)) // 2
HIT_LINE_Y = SCREEN_HEIGHT - 100

# Note configuration
NOTE_WIDTH = 80
NOTE_HEIGHT = 20
NOTE_SPEED = 5
HIT_TOLERANCE = 30  # Pixels above/below hit line for successful hit

# Lane colors
LANE_COLORS = [
    (255, 100, 100),  # A - Red
    (100, 255, 100),  # W - Green
    (100, 100, 255),  # S - Blue
    (255, 255, 100),  # D - Yellow
]

class Note:
    """A note that falls down a specific lane"""

    def __init__(self, lane):
        self.lane = lane
        self.x = LANES_START_X + (lane * LANE_WIDTH) + (LANE_WIDTH - NOTE_WIDTH) // 2
        self.y = -NOTE_HEIGHT
        self.hit = False
        self.missed = False

    def update(self):
        """Move the note down"""
        self.y += NOTE_SPEED

        # Check if note was missed
        if self.y > HIT_LINE_Y + HIT_TOLERANCE:
            self.missed = True

    def draw(self, screen):
        """Draw the note"""
        if not self.hit and not self.missed:
            color = LANE_COLORS[self.lane]
            pygame.draw.rect(screen, color, (self.x, self.y, NOTE_WIDTH, NOTE_HEIGHT))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, NOTE_WIDTH, NOTE_HEIGHT), 2)

    def check_hit(self):
        """Check if note can be hit"""
        if abs(self.y + NOTE_HEIGHT/2 - HIT_LINE_Y) <= HIT_TOLERANCE:
            return True
        return False

class DrumRhythmGame:
    """Main game class"""

    def __init__(self, year=1978):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Drum Rhythm Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        # Year-based scoring
        self.year = year
        self.points_per_hit = self.calculate_points_per_hit(year)

        # Game state
        self.notes = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.misses = 0
        self.max_misses = 5
        self.note_spawn_timer = 0
        self.note_spawn_delay = 30  # Frames between notes

        # Key mapping
        self.key_lanes = {
            pygame.K_a: 0,
            pygame.K_w: 1,
            pygame.K_s: 2,
            pygame.K_d: 3
        }

        # Visual feedback
        self.lane_flash = [0, 0, 0, 0]  # Flash timer for each lane
        self.hit_particles = []

        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)

    def calculate_points_per_hit(self, year):
        """Calculate points per hit based on year"""
        if year <= 1978:
            return 1
        elif year == 1979:
            return 2
        elif year == 1980:
            return 3
        elif year == 1981:
            return 4
        elif year == 1982:
            return 5
        elif year == 1983:
            return 6
        elif year == 1984:
            return 7
        elif year == 1985:
            return 8
        elif year == 1986:
            return 9
        elif year >= 1987:
            # 10 points from 1987 onwards, +1 per year after
            return 10 + max(0, year - 1987)

    def spawn_note(self):
        """Spawn a new note in a random lane"""
        lane = random.randint(0, LANE_COUNT - 1)
        self.notes.append(Note(lane))

    def handle_key_press(self, key):
        """Handle drum key press"""
        if self.game_over:
            return

        if key in self.key_lanes:
            lane = self.key_lanes[key]
            self.lane_flash[lane] = 10  # Flash for 10 frames

            # Check for hit
            hit = False
            for note in self.notes:
                if note.lane == lane and not note.hit and note.check_hit():
                    note.hit = True
                    hit = True
                    self.score += self.points_per_hit  # Use year-based scoring
                    self.combo += 1
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo

                    # Create hit particle effect
                    self.create_hit_particle(lane)
                    break

            if not hit:
                self.combo = 0  # Reset combo on miss

    def create_hit_particle(self, lane):
        """Create particle effect for successful hit"""
        x = LANES_START_X + (lane * LANE_WIDTH) + LANE_WIDTH // 2
        for _ in range(10):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            self.hit_particles.append({
                'x': x,
                'y': HIT_LINE_Y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 30,
                'color': LANE_COLORS[lane]
            })

    def update_particles(self):
        """Update particle effects"""
        for particle in self.hit_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.hit_particles.remove(particle)

    def draw_lanes(self):
        """Draw the lanes"""
        for i in range(LANE_COUNT):
            x = LANES_START_X + (i * LANE_WIDTH)

            # Draw lane background
            if self.lane_flash[i] > 0:
                alpha = self.lane_flash[i] * 25
                color = (*LANE_COLORS[i], min(255, alpha))
                s = pygame.Surface((LANE_WIDTH, SCREEN_HEIGHT))
                s.set_alpha(alpha)
                s.fill(LANE_COLORS[i])
                self.screen.blit(s, (x, 0))
                self.lane_flash[i] -= 1

            # Draw lane borders
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 2)

        # Draw rightmost border
        pygame.draw.line(self.screen, GRAY,
                        (LANES_START_X + LANE_COUNT * LANE_WIDTH, 0),
                        (LANES_START_X + LANE_COUNT * LANE_WIDTH, SCREEN_HEIGHT), 2)

    def draw_hit_line(self):
        """Draw the hit line and key indicators"""
        # Draw hit line
        pygame.draw.line(self.screen, WHITE,
                        (LANES_START_X, HIT_LINE_Y),
                        (LANES_START_X + LANE_COUNT * LANE_WIDTH, HIT_LINE_Y), 3)

        # Draw key indicators
        keys = ['A', 'W', 'S', 'D']
        for i, key in enumerate(keys):
            x = LANES_START_X + (i * LANE_WIDTH) + LANE_WIDTH // 2

            # Draw circle for key
            pygame.draw.circle(self.screen, DARK_GRAY, (x, HIT_LINE_Y + 40), 25)
            pygame.draw.circle(self.screen, LANE_COLORS[i], (x, HIT_LINE_Y + 40), 25, 3)

            # Draw key letter
            text = self.font.render(key, True, WHITE)
            text_rect = text.get_rect(center=(x, HIT_LINE_Y + 40))
            self.screen.blit(text, text_rect)

    def draw_ui(self):
        """Draw score and combo"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Combo
        combo_color = WHITE
        if self.combo > 10:
            combo_color = YELLOW
        elif self.combo > 5:
            combo_color = GREEN

        combo_text = self.font.render(f"Combo: {self.combo}", True, combo_color)
        self.screen.blit(combo_text, (10, 50))

        # Max combo
        max_combo_text = self.small_font.render(f"Max: {self.max_combo}", True, GRAY)
        self.screen.blit(max_combo_text, (10, 90))

        # Year and points per hit
        year_text = self.small_font.render(f"Year: {self.year} (+{self.points_per_hit} pts/hit)", True, YELLOW)
        self.screen.blit(year_text, (10, 120))

        # Misses
        miss_color = WHITE
        if self.misses >= 4:
            miss_color = RED
        elif self.misses >= 2:
            miss_color = YELLOW

        miss_text = self.font.render(f"Misses: {self.misses}/{self.max_misses}", True, miss_color)
        miss_rect = miss_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(miss_text, miss_rect)

        # Instructions
        inst_text = self.small_font.render("Press A W S D to hit the notes!", True, GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(inst_text, inst_rect)

        # Game over screen
        if self.game_over:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)

            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(final_score_text, final_score_rect)

            restart_text = self.small_font.render("Press ESC to quit", True, GRAY)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(restart_text, restart_rect)

    def draw_particles(self):
        """Draw particle effects"""
        for particle in self.hit_particles:
            alpha = particle['life'] * 8
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             max(2, particle['life'] // 5))

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.handle_key_press(event.key)

            # Only spawn notes if not game over
            if not self.game_over:
                # Spawn notes
                self.note_spawn_timer += 1
                if self.note_spawn_timer >= self.note_spawn_delay:
                    self.spawn_note()
                    self.note_spawn_timer = 0

                    # Gradually increase difficulty
                    if self.score > 100 and self.note_spawn_delay > 20:
                        self.note_spawn_delay = 20
                    elif self.score > 200 and self.note_spawn_delay > 15:
                        self.note_spawn_delay = 15

            # Update notes
            for note in self.notes[:]:
                note.update()
                if note.hit or note.missed:
                    if note.missed and not note.hit:
                        self.combo = 0  # Reset combo on missed note
                        self.misses += 1

                        # Check for game over
                        if self.misses >= self.max_misses:
                            self.game_over = True

                    self.notes.remove(note)

            # Update particles
            self.update_particles()

            # Draw everything
            self.screen.fill(BLACK)
            self.draw_lanes()
            self.draw_hit_line()

            # Draw notes
            for note in self.notes:
                note.draw(self.screen)

            self.draw_particles()
            self.draw_ui()

            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# Main execution
if __name__ == "__main__":
    import sys

    # Get year from command line or use default
    year = 1978
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f"Invalid year '{sys.argv[1]}', using 1978")
            year = 1978

    game = DrumRhythmGame(year)
    game.run()