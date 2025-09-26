import pygame
import random
import math
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -12
BALL_SPEED = 4
BALL_SIZE = 15
HOLE_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BLUE = (64, 164, 223)
YELLOW = (255, 223, 0)
RED = (220, 20, 60)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
SAND = (238, 203, 173)
DARK_GRAY = (64, 64, 64)

class GolfBall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_SIZE
        self.on_ground = False
        self.total_jumps = 0  # Track total jumps used
        self.max_jumps = 10  # Maximum jumps per course
        self.in_sand = False
        self.level_width = SCREEN_WIDTH * 3  # Will be set by game

    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.vy += GRAVITY

        # Apply sand trap effect (slower movement)
        speed_mult = 0.3 if self.in_sand else 1.0

        # Update position
        self.x += self.vx * speed_mult
        self.y += self.vy

        # Ground collision
        if self.y >= SCREEN_HEIGHT - 100 - self.radius:
            self.y = SCREEN_HEIGHT - 100 - self.radius
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Level boundaries (not screen boundaries)
        self.x = max(self.radius, min(self.level_width - self.radius, self.x))

    def jump(self):
        if self.on_ground and self.total_jumps < self.max_jumps:
            self.vy = JUMP_STRENGTH
            self.total_jumps += 1
            self.on_ground = False
            return True
        return False

    def draw(self, screen, camera_x):
        # Draw shadow
        shadow_y = SCREEN_HEIGHT - 95
        pygame.draw.ellipse(screen, (0, 0, 0, 50),
                          (self.x - camera_x - self.radius, shadow_y,
                           self.radius * 2, self.radius // 2))

        # Draw ball with dimples pattern
        pygame.draw.circle(screen, WHITE,
                         (int(self.x - camera_x), int(self.y)),
                         self.radius)
        pygame.draw.circle(screen, GRAY,
                         (int(self.x - camera_x), int(self.y)),
                         self.radius, 1)

        # Dimples
        for angle in range(0, 360, 60):
            dx = int(self.radius * 0.5 * math.cos(math.radians(angle)))
            dy = int(self.radius * 0.5 * math.sin(math.radians(angle)))
            pygame.draw.circle(screen, (220, 220, 220),
                             (int(self.x - camera_x + dx), int(self.y + dy)), 2)

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        self.vx = 0
        self.vy = 0
        self.animation_frame = 0
        self.animation_timer = 0

        # Set movement for certain obstacles
        if self.type == "bird":
            self.vy = random.choice([-2, -1, 1, 2])
            self.original_y = y
        elif self.type == "golf_cart":
            self.vx = random.choice([-2, 2])
        elif self.type == "golfer":
            self.swing_timer = random.randint(0, 100)

    def update(self):
        self.animation_timer += 1

        if self.type == "bird":
            self.y += self.vy
            # Reverse direction at boundaries
            if abs(self.y - self.original_y) > 50:
                self.vy *= -1

        elif self.type == "golf_cart":
            self.x += self.vx
            # Reverse at screen edges
            if self.x <= 0 or self.x >= SCREEN_WIDTH * 3:
                self.vx *= -1

        elif self.type == "golfer":
            self.swing_timer += 1
            if self.swing_timer > 120:
                self.swing_timer = 0

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x

        if self.type == "sand_trap":
            # Draw sand trap
            pygame.draw.ellipse(screen, SAND,
                              (screen_x, self.y, self.width, self.height))
            # Add texture
            for i in range(5):
                dot_x = screen_x + random.randint(5, self.width - 5)
                dot_y = self.y + random.randint(5, self.height - 5)
                pygame.draw.circle(screen, (228, 193, 163), (dot_x, dot_y), 1)

        elif self.type == "water":
            # Draw water hazard with waves
            pygame.draw.rect(screen, BLUE,
                           (screen_x, self.y, self.width, self.height))
            wave_offset = (self.animation_timer // 10) % 10
            for i in range(0, self.width, 20):
                pygame.draw.arc(screen, (100, 200, 255),
                              (screen_x + i - wave_offset, self.y + 5, 20, 10),
                              0, math.pi, 2)

        elif self.type == "rock":
            # Draw rock
            points = [
                (screen_x + self.width//2, self.y),
                (screen_x + self.width, self.y + self.height//2),
                (screen_x + self.width - 5, self.y + self.height),
                (screen_x + 5, self.y + self.height),
                (screen_x, self.y + self.height//2)
            ]
            pygame.draw.polygon(screen, GRAY, points)
            pygame.draw.polygon(screen, DARK_GRAY, points, 2)

        elif self.type == "bird":
            # Draw bird
            body_rect = pygame.Rect(screen_x, self.y, self.width, self.height)
            pygame.draw.ellipse(screen, BLACK, body_rect)
            # Wings
            wing_flap = math.sin(self.animation_timer * 0.2) * 5
            pygame.draw.ellipse(screen, BLACK,
                              (screen_x - 10, self.y + wing_flap, 15, 8))
            pygame.draw.ellipse(screen, BLACK,
                              (screen_x + self.width - 5, self.y - wing_flap, 15, 8))
            # Eye
            pygame.draw.circle(screen, WHITE,
                             (screen_x + self.width - 5, self.y + 5), 2)

        elif self.type == "golf_cart":
            # Draw golf cart
            # Body
            pygame.draw.rect(screen, WHITE,
                           (screen_x, self.y, self.width, self.height - 10))
            # Roof
            pygame.draw.rect(screen, GREEN,
                           (screen_x - 5, self.y - 10, self.width + 10, 15))
            # Wheels
            pygame.draw.circle(screen, BLACK,
                             (screen_x + 10, self.y + self.height - 5), 8)
            pygame.draw.circle(screen, BLACK,
                             (screen_x + self.width - 10, self.y + self.height - 5), 8)

        elif self.type == "golfer":
            # Draw golfer (simplified stick figure)
            # Body
            pygame.draw.line(screen, BLACK,
                           (screen_x + self.width//2, self.y + 15),
                           (screen_x + self.width//2, self.y + self.height - 15), 3)
            # Head
            pygame.draw.circle(screen, BLACK,
                             (screen_x + self.width//2, self.y + 10), 8)
            # Arms with golf club
            swing_angle = math.sin(self.swing_timer * 0.05) * 30
            club_end_x = screen_x + self.width//2 + int(25 * math.cos(math.radians(swing_angle - 45)))
            club_end_y = self.y + 25 + int(25 * math.sin(math.radians(swing_angle - 45)))
            pygame.draw.line(screen, BLACK,
                           (screen_x + self.width//2, self.y + 25),
                           (club_end_x, club_end_y), 3)
            # Legs
            pygame.draw.line(screen, BLACK,
                           (screen_x + self.width//2, self.y + self.height - 15),
                           (screen_x + self.width//2 - 8, self.y + self.height), 3)
            pygame.draw.line(screen, BLACK,
                           (screen_x + self.width//2, self.y + self.height - 15),
                           (screen_x + self.width//2 + 8, self.y + self.height), 3)

    def check_collision(self, ball):
        # Simple rectangular collision
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius,
                               ball.radius * 2, ball.radius * 2)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        return ball_rect.colliderect(obstacle_rect)

class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = HOLE_SIZE

    def draw(self, screen, camera_x):
        # Draw hole
        pygame.draw.circle(screen, BLACK,
                         (int(self.x - camera_x), int(self.y)),
                         self.radius)
        pygame.draw.circle(screen, DARK_GREEN,
                         (int(self.x - camera_x), int(self.y)),
                         self.radius + 2, 2)

        # Draw flag pole
        pole_x = self.x - camera_x + self.radius - 5
        pygame.draw.line(screen, BROWN,
                       (pole_x, self.y),
                       (pole_x, self.y - 40), 2)

        # Draw flag
        flag_points = [
            (pole_x, self.y - 40),
            (pole_x + 20, self.y - 35),
            (pole_x, self.y - 30)
        ]
        pygame.draw.polygon(screen, RED, flag_points)

    def check_win(self, ball):
        distance = math.sqrt((ball.x - self.x)**2 + (ball.y - self.y)**2)
        return distance < self.radius

class GolfPlatformerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Golf Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        self.ball = GolfBall(100, SCREEN_HEIGHT - 200)
        self.camera_x = 0
        self.level_width = SCREEN_WIDTH * 3
        self.ball.level_width = self.level_width  # Pass level width to ball
        self.hole = Hole(self.level_width - 200, SCREEN_HEIGHT - 100)
        self.obstacles = []
        self.score = 0.0  # Float for fractional points
        self.max_distance = 0  # Track furthest distance for points
        self.game_over = False
        self.game_won = False
        self.death_reason = ""
        self.immunity_timer = 120  # 2 seconds at 60 FPS

        self.generate_level()

    def generate_level(self):
        # Generate obstacles throughout the level
        obstacle_types = ["sand_trap", "water", "rock", "bird", "golf_cart", "golfer"]

        for i in range(150, self.level_width - 300, 100):
            if random.random() < 0.7:  # 70% chance of obstacle
                obstacle_type = random.choice(obstacle_types)

                if obstacle_type == "sand_trap":
                    self.obstacles.append(Obstacle(
                        i, SCREEN_HEIGHT - 100,
                        random.randint(60, 120), 30,
                        "sand_trap"
                    ))
                elif obstacle_type == "water":
                    self.obstacles.append(Obstacle(
                        i, SCREEN_HEIGHT - 100,
                        random.randint(80, 150), 35,
                        "water"
                    ))
                elif obstacle_type == "rock":
                    self.obstacles.append(Obstacle(
                        i, SCREEN_HEIGHT - 130,
                        random.randint(30, 50), random.randint(30, 50),
                        "rock"
                    ))
                elif obstacle_type == "bird":
                    self.obstacles.append(Obstacle(
                        i, random.randint(200, 400),
                        25, 15,
                        "bird"
                    ))
                elif obstacle_type == "golf_cart":
                    self.obstacles.append(Obstacle(
                        i, SCREEN_HEIGHT - 140,
                        60, 40,
                        "golf_cart"
                    ))
                elif obstacle_type == "golfer":
                    self.obstacles.append(Obstacle(
                        i, SCREEN_HEIGHT - 150,
                        20, 50,
                        "golfer"
                    ))

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.ball.vx = -BALL_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.ball.vx = BALL_SPEED
        else:
            self.ball.vx *= 0.9  # Friction

    def update(self):
        if self.game_over or self.game_won:
            return

        # Update ball
        self.ball.update()

        # Update camera to follow ball
        target_camera = self.ball.x - SCREEN_WIDTH // 2
        self.camera_x += (target_camera - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.level_width - SCREEN_WIDTH, self.camera_x))

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update()

        # Update immunity timer
        if self.immunity_timer > 0:
            self.immunity_timer -= 1

        # Check collisions (only after immunity expires)
        self.ball.in_sand = False
        if self.immunity_timer <= 0:
            for obstacle in self.obstacles:
                if obstacle.check_collision(self.ball):
                    # Hit any obstacle = game over
                    self.game_over = True
                    if obstacle.type == "sand_trap":
                        self.death_reason = "Stuck in sand trap!"
                    elif obstacle.type == "water":
                        self.death_reason = "Splashed into water hazard!"
                    elif obstacle.type == "rock":
                        self.death_reason = "Crashed into a rock!"
                    elif obstacle.type == "golfer":
                        self.death_reason = "Hit by a golfer!"
                    elif obstacle.type == "golf_cart":
                        self.death_reason = "Run over by golf cart!"
                    elif obstacle.type == "bird":
                        self.death_reason = "Bird strike!"
                    break

        # Update score based on distance (0.1 point per 50 yards)
        current_distance = int(self.ball.x / 50)  # 50 pixels = 1 yard for scoring
        if current_distance > self.max_distance:
            points_gained = (current_distance - self.max_distance) * 0.1  # 10x less points
            self.score += points_gained
            self.max_distance = current_distance

        # Check win condition
        if self.hole.check_win(self.ball):
            self.game_won = True
            self.score += 0.5  # Bonus points for reaching hole (also 10x less)

        # Check game over (out of jumps)
        if self.ball.total_jumps >= self.ball.max_jumps and self.ball.on_ground:
            # Check if we can still reach the hole
            if self.ball.x < self.hole.x - 100:  # Too far from hole
                self.game_over = True
                self.death_reason = "Out of jumps!"

    def draw_background(self, screen):
        # Sky gradient
        for i in range(SCREEN_HEIGHT - 100):
            color_value = int(135 + (i / (SCREEN_HEIGHT - 100)) * 80)
            pygame.draw.line(screen, (color_value, color_value + 20, 255),
                           (0, i), (SCREEN_WIDTH, i))

        # Ground
        pygame.draw.rect(screen, GREEN,
                       (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

        # Grass texture
        for i in range(0, SCREEN_WIDTH, 20):
            for j in range(SCREEN_HEIGHT - 100, SCREEN_HEIGHT, 10):
                if random.random() < 0.3:
                    pygame.draw.line(screen, DARK_GREEN,
                                   (i + random.randint(-5, 5), j),
                                   (i + random.randint(-5, 5), j + 5), 1)

    def draw(self):
        # Background
        self.draw_background(self.screen)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.camera_x)

        # Draw hole
        self.hole.draw(self.screen, self.camera_x)

        # Draw ball (with immunity effect)
        if self.immunity_timer > 0:
            # Flashing effect during immunity
            if self.immunity_timer % 10 < 5:
                self.ball.draw(self.screen, self.camera_x)
        else:
            self.ball.draw(self.screen, self.camera_x)

        # UI
        score_text = self.font.render(f"Score: {self.score:.1f}",
                                      True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Jump indicator
        jumps_remaining = self.ball.max_jumps - self.ball.total_jumps
        jumps_text = self.small_font.render(f"Jumps: {jumps_remaining}/{self.ball.max_jumps}",
                                           True, YELLOW if jumps_remaining > 3 else RED)
        self.screen.blit(jumps_text, (10, 50))

        # Distance to hole
        distance = int(abs(self.hole.x - self.ball.x) / 10)
        dist_text = self.small_font.render(f"Distance to hole: {distance}m",
                                          True, WHITE)
        self.screen.blit(dist_text, (10, 80))

        # Instructions
        if self.ball.x < 200:
            inst_text = self.small_font.render("Arrow Keys/WASD: Move | Space: Jump | R: Reset",
                                              True, WHITE)
            self.screen.blit(inst_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 30))

        # Immunity indicator
        if self.immunity_timer > 0:
            immunity_text = self.font.render(f"IMMUNITY: {self.immunity_timer // 60 + 1}s",
                                            True, YELLOW)
            self.screen.blit(immunity_text, (SCREEN_WIDTH//2 - 80, 50))

        # Game over/win screen
        if self.game_won:
            win_surface = pygame.Surface((400, 200))
            win_surface.fill(GREEN)
            win_surface.set_alpha(230)
            self.screen.blit(win_surface, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100))

            win_text = self.font.render("GOAL REACHED!", True, WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))

            score_text = self.font.render(f"Final Score: {self.score:.1f}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))

            restart_text = self.small_font.render("Press R to play again", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 40))

        elif self.game_over:
            over_surface = pygame.Surface((400, 200))
            over_surface.fill(RED)
            over_surface.set_alpha(230)
            self.screen.blit(over_surface, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100))

            over_text = self.font.render("GAME OVER!", True, WHITE)
            self.screen.blit(over_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50))

            reason_text = self.small_font.render(self.death_reason, True, WHITE)
            self.screen.blit(reason_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

            score_text = self.small_font.render(f"Score: {self.score:.1f}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 + 25))

            restart_text = self.small_font.render("Press R to retry", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 50))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.jump()
                    elif event.key == pygame.K_r:
                        self.reset_game()

            self.handle_input()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GolfPlatformerGame()
    game.run()