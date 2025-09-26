import pygame
import random
import sys
import os
import math
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from systems.game_end_manager import GameEndManager

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
HORIZON_Y = SCREEN_HEIGHT // 2 - 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
BLUE = (100, 149, 237)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (205, 133, 63)
ORANGE = (255, 165, 0)

class House3D:
    def __init__(self, x, z, side):
        self.x = x  # Horizontal position
        self.z = z  # Distance from camera
        self.side = side  # -1 for left, 1 for right
        self.width = 200
        self.height = 250
        self.has_mailbox = True
        self.mailbox_hit = False
        self.window_hit = False
        self.has_cat = random.choice([True, False])
        self.cat_hit = False

        # Random house appearance
        self.wall_color = random.choice([
            (200, 180, 140),
            (180, 140, 100),
            (220, 200, 160),
            (160, 140, 120),
            (210, 210, 210),
            (255, 248, 220)
        ])

        self.roof_color = random.choice([
            (139, 69, 19),
            (160, 82, 45),
            (128, 0, 0),
            (105, 105, 105)
        ])

        self.door_color = random.choice([BROWN, DARK_GRAY, (128, 0, 0)])
        self.has_garage = random.choice([True, False])
        self.window_lights = random.choice([True, False, False])  # Some windows lit
        self.window_open = random.choice([True, False])  # Open windows are targets

    def get_screen_position(self, camera_z, bob_offset=0, tilt_offset=0):
        # Calculate relative position
        relative_z = self.z - camera_z

        if relative_z <= 0:
            return None, None, 0

        # Perspective projection
        perspective_scale = 300 / relative_z
        screen_x = SCREEN_WIDTH // 2 + (self.x * perspective_scale) + tilt_offset
        screen_y = HORIZON_Y + bob_offset

        return screen_x, screen_y, perspective_scale

    def draw(self, screen, camera_z, bob_offset=0, tilt_offset=0):
        screen_x, screen_y, scale = self.get_screen_position(camera_z, bob_offset, tilt_offset)

        if screen_x is None or scale <= 0:
            return

        # Don't draw if too far away
        if scale < 0.1:
            return

        # Calculate sizes based on perspective
        house_width = int(self.width * scale)
        house_height = int(self.height * scale)

        # Don't draw tiny houses
        if house_width < 5 or house_height < 5:
            return

        # Draw house main structure
        house_rect = pygame.Rect(
            screen_x - house_width // 2,
            screen_y - house_height,
            house_width,
            house_height
        )

        # Only draw if on screen
        if house_rect.right < 0 or house_rect.left > SCREEN_WIDTH:
            return

        # Main wall
        pygame.draw.rect(screen, self.wall_color, house_rect)
        pygame.draw.rect(screen, BLACK, house_rect, max(1, int(scale)))

        # Roof
        roof_height = int(house_height * 0.3)
        roof_points = [
            (house_rect.left - int(10 * scale), house_rect.top + roof_height),
            (house_rect.centerx, house_rect.top - int(20 * scale)),
            (house_rect.right + int(10 * scale), house_rect.top + roof_height)
        ]
        pygame.draw.polygon(screen, self.roof_color, roof_points)
        pygame.draw.polygon(screen, BLACK, roof_points, max(1, int(scale)))

        # Door
        door_width = int(house_width * 0.15)
        door_height = int(house_height * 0.3)
        door_x = house_rect.centerx - door_width // 2
        door_y = house_rect.bottom - door_height

        if door_width > 2 and door_height > 2:
            pygame.draw.rect(screen, self.door_color,
                           (door_x, door_y, door_width, door_height))

        # Windows
        if house_width > 30:
            window_width = int(house_width * 0.15)
            window_height = int(house_height * 0.15)

            if window_width > 2 and window_height > 2:
                window_y = house_rect.top + int(house_height * 0.35)

                # Left window
                if self.window_open and not self.window_hit:
                    # Open window - target!
                    pygame.draw.rect(screen, BLACK,
                                   (house_rect.left + int(house_width * 0.15),
                                    window_y, window_width, window_height))
                    pygame.draw.rect(screen, WHITE,
                                   (house_rect.left + int(house_width * 0.15),
                                    window_y, window_width, window_height), 2)
                elif self.window_hit:
                    # Hit window - show paper
                    pygame.draw.rect(screen, WHITE,
                                   (house_rect.left + int(house_width * 0.15),
                                    window_y, window_width, window_height))
                else:
                    # Normal closed window
                    window_color = YELLOW if self.window_lights else DARK_GRAY
                    pygame.draw.rect(screen, window_color,
                                   (house_rect.left + int(house_width * 0.15),
                                    window_y, window_width, window_height))

                # Right window (always normal)
                window_color = YELLOW if self.window_lights else DARK_GRAY
                pygame.draw.rect(screen, window_color,
                               (house_rect.right - int(house_width * 0.15) - window_width,
                                window_y, window_width, window_height))

        # Garage
        if self.has_garage and house_width > 40:
            garage_width = int(house_width * 0.35)
            garage_height = int(house_height * 0.25)
            garage_x = house_rect.left + int(house_width * 0.6)
            garage_y = house_rect.bottom - garage_height

            if garage_width > 3 and garage_height > 3:
                pygame.draw.rect(screen, WHITE,
                               (garage_x, garage_y, garage_width, garage_height))
                pygame.draw.rect(screen, DARK_GRAY,
                               (garage_x, garage_y, garage_width, garage_height), 1)

        # Mailbox
        if self.has_mailbox and scale > 0.3:
            mailbox_offset = int(50 * self.side * scale)
            mailbox_x = screen_x + mailbox_offset
            mailbox_y = screen_y - int(30 * scale)
            mailbox_size = max(3, int(15 * scale))

            if self.mailbox_hit:
                mailbox_color = YELLOW  # Hit mailbox!
            else:
                mailbox_color = GREEN  # Target

            # Mailbox post
            pygame.draw.rect(screen, DARK_GRAY,
                           (mailbox_x - 1, mailbox_y, 3, int(25 * scale)))

            # Mailbox
            pygame.draw.rect(screen, mailbox_color,
                           (mailbox_x - mailbox_size // 2, mailbox_y - mailbox_size // 2,
                            mailbox_size, int(mailbox_size * 0.7)))

            # Draw target indicator if not hit
            if not self.mailbox_hit and scale > 0.5:
                pygame.draw.circle(screen, RED, (mailbox_x, mailbox_y - mailbox_size // 2),
                                 max(2, int(5 * scale)), 1)

        # Cat on porch
        if self.has_cat and scale > 0.4:
            cat_x = screen_x + int(30 * self.side * scale)
            cat_y = screen_y - int(10 * scale)
            cat_size = max(3, int(12 * scale))

            if not self.cat_hit:
                # Draw cat
                pygame.draw.ellipse(screen, ORANGE,
                                  (cat_x - cat_size // 2, cat_y - cat_size // 2,
                                   cat_size, int(cat_size * 0.6)))
                # Cat head
                pygame.draw.circle(screen, ORANGE,
                                 (cat_x - int(cat_size * 0.3), cat_y - int(cat_size * 0.2)),
                                 max(2, int(cat_size * 0.3)))
                # Ears
                if scale > 0.6:
                    pygame.draw.polygon(screen, ORANGE,
                                      [(cat_x - int(cat_size * 0.4), cat_y - int(cat_size * 0.3)),
                                       (cat_x - int(cat_size * 0.5), cat_y - int(cat_size * 0.5)),
                                       (cat_x - int(cat_size * 0.3), cat_y - int(cat_size * 0.4))])
            else:
                # Cat ran away - show motion lines
                for i in range(3):
                    pygame.draw.line(screen, GRAY,
                                   (cat_x - i * 5, cat_y),
                                   (cat_x - i * 5 - 10, cat_y), 1)

class Tree3D:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.height = random.randint(150, 300)
        self.trunk_color = random.choice([BROWN, (101, 67, 33)])
        self.leaf_color = random.choice([DARK_GREEN, GREEN, (34, 139, 34)])

    def draw(self, screen, camera_z, bob_offset=0, tilt_offset=0):
        relative_z = self.z - camera_z

        if relative_z <= 0:
            return

        scale = 300 / relative_z
        screen_x = SCREEN_WIDTH // 2 + (self.x * scale) + tilt_offset
        screen_y = HORIZON_Y + bob_offset

        if scale < 0.1:
            return

        # Draw trunk
        trunk_width = max(2, int(20 * scale))
        trunk_height = int(self.height * scale * 0.4)

        if trunk_width > 1 and trunk_height > 1:
            pygame.draw.rect(screen, self.trunk_color,
                           (screen_x - trunk_width // 2, screen_y - trunk_height,
                            trunk_width, trunk_height))

        # Draw leaves (circle for simplicity)
        leaf_radius = max(3, int(self.height * scale * 0.3))
        leaf_y = screen_y - trunk_height - leaf_radius

        if leaf_radius > 2:
            pygame.draw.circle(screen, self.leaf_color,
                             (int(screen_x), int(leaf_y)), leaf_radius)

class Newspaper3D:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.rotation = 0
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vy += 0.5  # Gravity
        self.rotation += 10

        # Hit ground
        if self.y > 0:
            self.y = 0
            self.vy = 0
            self.vx *= 0.8
            self.vz *= 0.8

        # Stop if slow enough
        if abs(self.vx) < 0.1 and abs(self.vz) < 0.1:
            self.active = False

    def draw(self, screen, camera_z):
        if not self.active:
            return

        relative_z = self.z - camera_z
        if relative_z <= 0:
            return

        scale = 300 / relative_z
        screen_x = SCREEN_WIDTH // 2 + (self.x * scale)
        screen_y = HORIZON_Y - (self.y * scale)

        paper_size = max(2, int(10 * scale))

        if paper_size > 1:
            # Draw spinning paper
            stretched_width = int(paper_size * abs(math.cos(math.radians(self.rotation))))
            if stretched_width > 0:
                pygame.draw.rect(screen, WHITE,
                               (screen_x - stretched_width // 2,
                                screen_y - paper_size // 2,
                                stretched_width, paper_size))

class FirstPersonStreetGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("First Person Newspaper Delivery")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.score = 0
        self.papers = 15
        self.camera_z = 0
        self.camera_x = 0
        self.move_speed = 8  # Faster auto movement
        self.strafe_speed = 5
        self.game_over = False
        self.papers_delivered = 0
        self.misses = 0
        self.max_misses = 5

        # Head bob for biking effect
        self.bob_angle = 0
        self.bob_speed = 0.15
        self.bob_amount = 5
        self.tilt_angle = 0

        # Mouse aiming
        self.mouse_x = SCREEN_WIDTH // 2
        self.mouse_y = SCREEN_HEIGHT // 2
        self.aim_offset_x = 0
        self.aim_offset_y = 0
        pygame.mouse.set_visible(False)

        # Objects
        self.houses = []
        self.trees = []
        self.newspapers = []

        # Generate level
        self.generate_level()

    def generate_level(self):
        # Generate houses on both sides of the street
        house_spacing = 300

        for i in range(20):
            # Left side houses
            if random.random() > 0.2:
                house = House3D(-400, 200 + i * house_spacing, -1)
                self.houses.append(house)

            # Right side houses
            if random.random() > 0.2:
                house = House3D(400, 200 + i * house_spacing, 1)
                self.houses.append(house)

        # Add trees
        for i in range(40):
            side = random.choice([-1, 1])
            tree_x = random.randint(500, 700) * side
            tree_z = random.randint(100, 6000)
            self.trees.append(Tree3D(tree_x, tree_z))

        # Count subscribers
        subscriber_count = sum(1 for h in self.houses if h.needs_delivery)
        self.papers = subscriber_count + 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        return False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1 and self.papers > 0:  # Left click
                    # Determine throw direction based on mouse position
                    if self.mouse_x < SCREEN_WIDTH // 2 - 50:
                        self.throw_paper(-1)  # Throw left
                    elif self.mouse_x > SCREEN_WIDTH // 2 + 50:
                        self.throw_paper(1)  # Throw right
                    else:
                        # Throw straight based on slight mouse offset
                        direction = 1 if self.mouse_x > SCREEN_WIDTH // 2 else -1
                        self.throw_paper(direction)

        return True

    def throw_paper(self, direction):
        if self.papers <= 0:
            return

        self.papers -= 1

        # Create newspaper projectile with higher arc
        paper = Newspaper3D(
            self.camera_x + direction * 50,  # Start position
            -80,  # Start height (higher arc)
            self.camera_z + 50,  # Slightly ahead
            direction * 20,  # Horizontal velocity
            -25,  # Strong upward velocity for high arc
            25  # Forward velocity
        )
        self.newspapers.append(paper)

        # Check for delivery
        hit_something = self.check_delivery(direction)

        # Track misses
        if not hit_something:
            self.misses += 1
            if self.misses >= self.max_misses:
                self.game_over = True

    def check_delivery(self, direction):
        # Check if paper will hit any target
        hit_something = False

        for house in self.houses:
            relative_z = house.z - self.camera_z

            # Check if house is in throwing range
            if 0 < relative_z < 250:
                # Check if throwing in correct direction
                correct_side = (direction < 0 and house.side < 0) or (direction > 0 and house.side > 0)

                if correct_side:
                    # Random chance to hit different targets based on distance
                    hit_roll = random.random()

                    if relative_z < 100:  # Close range - better accuracy
                        if hit_roll < 0.4 and not house.mailbox_hit:
                            # Hit mailbox
                            house.mailbox_hit = True
                            self.score += 1
                            hit_something = True
                            break
                        elif hit_roll < 0.6 and house.window_open and not house.window_hit:
                            # Hit open window
                            house.window_hit = True
                            self.score += 1
                            hit_something = True
                            break
                        elif hit_roll < 0.7 and house.has_cat and not house.cat_hit:
                            # Hit cat (cat runs away)
                            house.cat_hit = True
                            self.score += 1
                            hit_something = True
                            break
                    else:  # Longer range - less accurate
                        if hit_roll < 0.2 and not house.mailbox_hit:
                            house.mailbox_hit = True
                            self.score += 1
                            hit_something = True
                            break
                        elif hit_roll < 0.3 and house.window_open and not house.window_hit:
                            house.window_hit = True
                            self.score += 1
                            hit_something = True
                            break

        return hit_something

    def update(self):
        if self.game_over:
            return

        # Auto move forward (biking)
        self.camera_z += self.move_speed

        # Update head bob for biking motion
        self.bob_angle += self.bob_speed

        # Handle continuous input for strafing
        keys = pygame.key.get_pressed()

        # Strafe left/right
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.camera_x = max(-200, self.camera_x - self.strafe_speed)
            self.tilt_angle = max(-10, self.tilt_angle - 1)  # Tilt left when turning
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.camera_x = min(200, self.camera_x + self.strafe_speed)
            self.tilt_angle = min(10, self.tilt_angle + 1)  # Tilt right when turning
        else:
            # Return tilt to center
            if self.tilt_angle > 0:
                self.tilt_angle -= 0.5
            elif self.tilt_angle < 0:
                self.tilt_angle += 0.5

        # Update mouse position for aiming
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        # Calculate aim offset based on mouse position
        self.aim_offset_x = (self.mouse_x - SCREEN_WIDTH // 2) * 0.3
        self.aim_offset_y = (self.mouse_y - SCREEN_HEIGHT // 2) * 0.2

        # Update newspapers
        for paper in self.newspapers[:]:
            paper.update()
            if paper.z - self.camera_z < -100:
                self.newspapers.remove(paper)

        # Check if level complete
        last_house_z = max([h.z for h in self.houses]) if self.houses else 0
        if self.camera_z > last_house_z + 200:
            self.game_over = True

    def draw_road_with_bob(self, bob_offset):
        # Draw road surface with perspective and bob effect
        road_color = GRAY

        # Draw road as a trapezoid that extends from horizon to bottom of screen
        road_points = [
            (SCREEN_WIDTH // 2 - 50, HORIZON_Y + bob_offset),  # Top left (narrow at horizon)
            (SCREEN_WIDTH // 2 + 50, HORIZON_Y + bob_offset),  # Top right
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT),  # Bottom right (wide at bottom)
            (100, SCREEN_HEIGHT)  # Bottom left
        ]
        pygame.draw.polygon(self.screen, road_color, road_points)

        # Draw road edges
        pygame.draw.line(self.screen, DARK_GRAY, road_points[0], road_points[3], 3)
        pygame.draw.line(self.screen, DARK_GRAY, road_points[1], road_points[2], 3)

    def draw_sky(self):
        # Gradient sky
        for y in range(HORIZON_Y):
            color_ratio = y / HORIZON_Y
            r = int(135 * color_ratio)
            g = int(206 * color_ratio)
            b = int(235 * color_ratio)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, SCREEN_WIDTH, 1))

    def draw(self):
        # Calculate bob and tilt offsets
        bob_offset = int(math.sin(self.bob_angle) * self.bob_amount)
        tilt_offset = int(self.tilt_angle * 2)

        # Clear screen
        self.screen.fill(LIGHT_GREEN)

        # Draw sky with tilt
        self.draw_sky()

        # Draw ground
        pygame.draw.rect(self.screen, DARK_GREEN,
                        (0, HORIZON_Y + bob_offset, SCREEN_WIDTH, SCREEN_HEIGHT - HORIZON_Y))

        # Draw road with bob effect
        self.draw_road_with_bob(bob_offset)

        # Sort objects by distance for proper rendering
        all_objects = []

        for house in self.houses:
            all_objects.append(('house', house, house.z))

        for tree in self.trees:
            all_objects.append(('tree', tree, tree.z))

        for paper in self.newspapers:
            all_objects.append(('paper', paper, paper.z))

        # Sort by z distance (far to near)
        all_objects.sort(key=lambda x: x[2], reverse=True)

        # Draw all objects with bob and tilt
        for obj_type, obj, _ in all_objects:
            if obj_type == 'house':
                obj.draw(self.screen, self.camera_z, bob_offset, tilt_offset)
            elif obj_type == 'tree':
                obj.draw(self.screen, self.camera_z, bob_offset, tilt_offset)
            elif obj_type == 'paper':
                obj.draw(self.screen, self.camera_z)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        papers_text = self.font.render(f"Papers: {self.papers}", True, WHITE)
        self.screen.blit(papers_text, (10, 50))

        # Draw crosshair at mouse position
        crosshair_color = WHITE
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y

        # Draw aiming crosshair
        pygame.draw.circle(self.screen, crosshair_color, (mouse_x, mouse_y), 15, 2)
        pygame.draw.line(self.screen, crosshair_color,
                        (mouse_x - 20, mouse_y),
                        (mouse_x - 8, mouse_y), 2)
        pygame.draw.line(self.screen, crosshair_color,
                        (mouse_x + 8, mouse_y),
                        (mouse_x + 20, mouse_y), 2)
        pygame.draw.line(self.screen, crosshair_color,
                        (mouse_x, mouse_y - 20),
                        (mouse_x, mouse_y - 8), 2)
        pygame.draw.line(self.screen, crosshair_color,
                        (mouse_x, mouse_y + 8),
                        (mouse_x, mouse_y + 20), 2)

        # Instructions
        inst1 = self.small_font.render("A/D: Steer | Left Click: Throw Paper | Auto-biking forward", True, WHITE)
        self.screen.blit(inst1, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT - 60))

        # Legend
        pygame.draw.rect(self.screen, GREEN, (10, 90, 15, 15))
        self.screen.blit(self.small_font.render("= Need delivery", True, WHITE), (30, 87))

        pygame.draw.rect(self.screen, BLUE, (10, 110, 15, 15))
        self.screen.blit(self.small_font.render("= Delivered", True, WHITE), (30, 107))

        # Game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("LEVEL COMPLETE!", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)

            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(final_score_text, score_rect)

            delivered_text = self.small_font.render(f"Delivered: {self.papers_delivered} | Missed: {self.papers_missed}", True, WHITE)
            delivered_rect = delivered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(delivered_text, delivered_rect)

            restart_text = self.small_font.render("Press SPACE to continue", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, restart_rect)

    def run(self):
        running = True
        game_ended = False

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

        if not game_ended:
            root = tk.Tk()
            root.withdraw()
            manager = GameEndManager()
            manager.handle_game_end(self.score, root)

        sys.exit(0)

def main():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = FirstPersonStreetGame()
    game.run()

if __name__ == "__main__":
    main()