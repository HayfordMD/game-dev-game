"""
2D Zombie Sprites for Pygame
Simple pixel-art style zombie sprites with animations
"""

import pygame
import random
import math

class Zombie(pygame.sprite.Sprite):
    """Basic zombie sprite with simple animations"""

    def __init__(self, x, y, zombie_type="normal"):
        super().__init__()
        self.zombie_type = zombie_type
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_speed = 0.2
        self.direction = "right"
        self.speed = random.uniform(0.5, 1.5)

        # Create zombie sprite
        self.size = 32
        self.create_zombie_frames()
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Movement and animation
        self.state = "idle"  # idle, walking, attacking
        self.health = 100
        self.attack_cooldown = 0

    def create_zombie_frames(self):
        """Create simple zombie sprites programmatically"""
        self.idle_frames = []
        self.walk_frames = []
        self.attack_frames = []

        # Color schemes for different zombie types
        colors = {
            "normal": {"skin": (100, 150, 100), "clothes": (50, 50, 80)},
            "fast": {"skin": (150, 100, 100), "clothes": (80, 50, 50)},
            "strong": {"skin": (80, 120, 80), "clothes": (40, 40, 60)}
        }

        zombie_colors = colors.get(self.zombie_type, colors["normal"])

        # Create idle frames (2 frames)
        for i in range(2):
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.draw_zombie(surface, zombie_colors, "idle", i)
            self.idle_frames.append(surface)

        # Create walking frames (4 frames)
        for i in range(4):
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.draw_zombie(surface, zombie_colors, "walk", i)
            self.walk_frames.append(surface)

        # Create attack frames (2 frames)
        for i in range(2):
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.draw_zombie(surface, zombie_colors, "attack", i)
            self.attack_frames.append(surface)

    def draw_zombie(self, surface, colors, animation_type, frame):
        """Draw a simple pixel-art zombie"""
        skin_color = colors["skin"]
        clothes_color = colors["clothes"]

        # Basic zombie shape
        # Head
        head_y = 8
        if animation_type == "walk" and frame % 2 == 1:
            head_y = 7  # Bobbing motion

        pygame.draw.rect(surface, skin_color, (12, head_y, 8, 8))

        # Eyes (red)
        pygame.draw.rect(surface, (200, 0, 0), (14, head_y + 2, 2, 2))
        pygame.draw.rect(surface, (200, 0, 0), (17, head_y + 2, 2, 2))

        # Body
        pygame.draw.rect(surface, clothes_color, (11, 16, 10, 10))

        # Arms
        if animation_type == "attack":
            # Arms forward for attack
            pygame.draw.rect(surface, skin_color, (8 + frame * 2, 18, 3, 8))
            pygame.draw.rect(surface, skin_color, (21 - frame * 2, 18, 3, 8))
        elif animation_type == "walk":
            # Swinging arms
            arm_offset = math.sin(frame * math.pi / 2) * 2
            pygame.draw.rect(surface, skin_color, (8, 18 + arm_offset, 3, 6))
            pygame.draw.rect(surface, skin_color, (21, 18 - arm_offset, 3, 6))
        else:
            # Default arms down
            pygame.draw.rect(surface, skin_color, (8, 18, 3, 6))
            pygame.draw.rect(surface, skin_color, (21, 18, 3, 6))

        # Legs
        if animation_type == "walk":
            # Animated legs
            leg_offset = frame % 2
            pygame.draw.rect(surface, clothes_color, (13 - leg_offset, 26, 3, 5))
            pygame.draw.rect(surface, clothes_color, (17 + leg_offset, 26, 3, 5))
        else:
            # Static legs
            pygame.draw.rect(surface, clothes_color, (13, 26, 3, 5))
            pygame.draw.rect(surface, clothes_color, (17, 26, 3, 5))

        # Add some decay/damage details
        if random.random() > 0.7:
            pygame.draw.rect(surface, (60, 40, 40),
                           (random.randint(11, 20), random.randint(16, 25), 2, 2))

    def update(self, target_pos=None):
        """Update zombie position and animation"""
        # Animation
        self.frame += self.animation_speed

        # Choose animation based on state
        if self.state == "walking":
            frame_list = self.walk_frames
            if self.frame >= len(frame_list):
                self.frame = 0
        elif self.state == "attacking":
            frame_list = self.attack_frames
            if self.frame >= len(frame_list):
                self.frame = 0
                self.state = "walking"  # Return to walking after attack
        else:  # idle
            frame_list = self.idle_frames
            if self.frame >= len(frame_list):
                self.frame = 0

        # Set current frame
        current_frame = int(self.frame) % len(frame_list)
        self.image = frame_list[current_frame]

        # Flip sprite based on direction
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        # Movement towards target
        if target_pos and self.state == "walking":
            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 5:
                # Move towards target
                dx_norm = dx / distance
                dy_norm = dy / distance
                self.rect.centerx += dx_norm * self.speed
                self.rect.centery += dy_norm * self.speed

                # Update direction
                if dx_norm < 0:
                    self.direction = "left"
                else:
                    self.direction = "right"
            elif distance < 50 and self.attack_cooldown <= 0:
                # Close enough to attack
                self.state = "attacking"
                self.attack_cooldown = 60
                self.frame = 0

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Random state changes for idle zombies
        if self.state == "idle" and random.random() < 0.01:
            self.state = "walking"
        elif self.state == "walking" and random.random() < 0.005:
            self.state = "idle"


class ZombieHorde:
    """Manages multiple zombies"""

    def __init__(self):
        self.zombies = pygame.sprite.Group()

    def spawn_zombie(self, x, y, zombie_type="normal"):
        """Spawn a new zombie"""
        zombie = Zombie(x, y, zombie_type)
        self.zombies.add(zombie)
        return zombie

    def spawn_wave(self, count, screen_width, screen_height):
        """Spawn a wave of zombies around the edges"""
        for i in range(count):
            side = random.choice(["top", "bottom", "left", "right"])

            if side == "top":
                x = random.randint(0, screen_width)
                y = -20
            elif side == "bottom":
                x = random.randint(0, screen_width)
                y = screen_height + 20
            elif side == "left":
                x = -20
                y = random.randint(0, screen_height)
            else:  # right
                x = screen_width + 20
                y = random.randint(0, screen_height)

            zombie_type = random.choice(["normal", "normal", "fast", "strong"])
            self.spawn_zombie(x, y, zombie_type)

    def update(self, target_pos=None):
        """Update all zombies"""
        for zombie in self.zombies:
            zombie.update(target_pos)

    def draw(self, screen):
        """Draw all zombies"""
        self.zombies.draw(screen)


# Demo/Test code
def main():
    """Test the zombie sprites"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Zombie Sprites Test")
    clock = pygame.time.Clock()

    # Create zombie horde
    horde = ZombieHorde()

    # Spawn initial zombies
    for i in range(5):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        zombie_type = random.choice(["normal", "fast", "strong"])
        horde.spawn_zombie(x, y, zombie_type)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Spawn a wave
                    horde.spawn_wave(5, 800, 600)
                elif event.key == pygame.K_c:
                    # Clear zombies
                    horde.zombies.empty()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Spawn zombie at mouse position
                mouse_pos = pygame.mouse.get_pos()
                horde.spawn_zombie(mouse_pos[0], mouse_pos[1])

        # Get mouse position for zombie targeting
        mouse_pos = pygame.mouse.get_pos()

        # Update
        horde.update(mouse_pos)

        # Draw
        screen.fill((40, 40, 60))  # Dark background

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Click: Spawn zombie at cursor",
            "Space: Spawn wave",
            "C: Clear all zombies",
            "Zombies follow mouse cursor"
        ]
        y_offset = 10
        for instruction in instructions:
            text = font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (10, y_offset))
            y_offset += 25

        # Draw zombie count
        count_text = font.render(f"Zombies: {len(horde.zombies)}", True, (255, 255, 255))
        screen.blit(count_text, (700, 10))

        # Draw zombies
        horde.draw(screen)

        # Draw cursor
        pygame.draw.circle(screen, (255, 100, 100), mouse_pos, 5)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()