import pygame
import math
import random
import sys
from enum import Enum

# Initialize Pygame and its modules
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors (demonstrating color constants)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

class Scene(Enum):
    """Enum for different showcase scenes"""
    MENU = 0
    SPRITES = 1
    PARTICLES = 2
    PHYSICS = 3
    DRAWING = 4
    TEXT = 5
    SOUND = 6
    INPUT = 7
    COLLISION = 8

class Particle:
    """Particle system demonstration"""
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-10, -2)
        self.lifetime = random.randint(30, 60)
        self.size = random.randint(2, 6)
        self.color = color or (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.gravity = 0.5

    def update(self):
        self.vx *= 0.98  # Air resistance
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self, screen):
        if self.lifetime > 0:
            alpha = min(255, self.lifetime * 8)
            pygame.draw.circle(screen, (*self.color[:3], alpha) if len(self.color) == 4 else self.color,
                             (int(self.x), int(self.y)), int(self.size))

class BouncingBall:
    """Physics demonstration with bouncing balls"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 30)
        self.vx = random.uniform(-5, 5)
        self.vy = 0
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.gravity = 0.8
        self.bounce_damping = 0.9

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vx *= -self.bounce_damping
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))

        # Bounce off floor
        if self.y + self.radius >= SCREEN_HEIGHT - 100:
            self.vy *= -self.bounce_damping
            self.y = SCREEN_HEIGHT - 100 - self.radius
            # Add some randomness to prevent perfect bounces
            self.vx += random.uniform(-0.5, 0.5)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)

class AnimatedSprite:
    """Sprite animation demonstration"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_speed = 0.2
        self.size = 50
        self.rotation = 0
        self.scale = 1.0
        self.scale_direction = 1
        self.color_shift = 0

    def update(self):
        self.frame += self.animation_speed
        self.rotation += 2
        self.scale += 0.02 * self.scale_direction
        if self.scale > 1.5 or self.scale < 0.5:
            self.scale_direction *= -1
        self.color_shift = (self.color_shift + 2) % 360

    def draw(self, screen):
        # Create a surface for the sprite
        sprite_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        # Draw animated shape
        points = []
        sides = 6
        for i in range(sides):
            angle = (i * 360 / sides) + self.rotation
            x = self.size + math.cos(math.radians(angle)) * self.size * self.scale
            y = self.size + math.sin(math.radians(angle)) * self.size * self.scale
            points.append((x, y))

        # Create rainbow color based on shift
        color = pygame.Color(0)
        color.hsva = (self.color_shift, 100, 100, 100)

        pygame.draw.polygon(sprite_surf, color, points)
        pygame.draw.polygon(sprite_surf, BLACK, points, 3)

        # Rotate the surface
        rotated = pygame.transform.rotate(sprite_surf, self.rotation)

        # Blit to screen
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)

class Button:
    """UI Button demonstration"""
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c + 50) for c in color)
        self.pressed = False
        self.hovered = False
        self.font = pygame.font.Font(None, 32)

    def update(self, mouse_pos, mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked:
            self.pressed = True
        else:
            self.pressed = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        if self.pressed:
            pygame.draw.rect(screen, tuple(max(0, c - 50) for c in color), self.rect)
        else:
            pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw text
        text_surf = self.font.render(self.text, True, WHITE if self.pressed else BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class PygameShowcase:
    def __init__(self):
        # Display setup (demonstrating display modes)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Feature Showcase")

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Font setup (demonstrating font rendering)
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)

        # Scene management
        self.current_scene = Scene.MENU
        self.running = True

        # Feature demonstrations
        self.particles = []
        self.balls = []
        self.sprites = []
        self.buttons = []

        # Input tracking
        self.keys_pressed = set()
        self.mouse_trail = []
        self.mouse_drawing = []

        # Surface demonstrations
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Initialize demo objects
        self.init_demos()

    def init_demos(self):
        """Initialize demonstration objects"""
        # Create animated sprites
        for i in range(3):
            self.sprites.append(AnimatedSprite(200 + i * 200, 300))

        # Create physics balls
        for i in range(5):
            self.balls.append(BouncingBall(random.randint(50, SCREEN_WIDTH - 50),
                                          random.randint(50, 200)))

        # Create menu buttons
        scenes = [("Sprites", Scene.SPRITES), ("Particles", Scene.PARTICLES),
                 ("Physics", Scene.PHYSICS), ("Drawing", Scene.DRAWING),
                 ("Text", Scene.TEXT), ("Input", Scene.INPUT),
                 ("Collision", Scene.COLLISION)]

        for i, (name, scene) in enumerate(scenes):
            x = 400 + (i % 2) * 200
            y = 200 + (i // 2) * 80
            button = Button(x, y, 180, 60, name, BLUE)
            button.scene = scene
            self.buttons.append(button)

    def handle_events(self):
        """Event handling demonstration"""
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)

                # Scene navigation
                if event.key == pygame.K_ESCAPE:
                    self.current_scene = Scene.MENU
                elif event.key == pygame.K_1:
                    self.current_scene = Scene.SPRITES
                elif event.key == pygame.K_2:
                    self.current_scene = Scene.PARTICLES
                elif event.key == pygame.K_3:
                    self.current_scene = Scene.PHYSICS
                elif event.key == pygame.K_4:
                    self.current_scene = Scene.DRAWING
                elif event.key == pygame.K_5:
                    self.current_scene = Scene.TEXT
                elif event.key == pygame.K_6:
                    self.current_scene = Scene.INPUT
                elif event.key == pygame.K_7:
                    self.current_scene = Scene.COLLISION

            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                if event.button == 1:  # Left click
                    # Create particles at mouse position
                    if self.current_scene == Scene.PARTICLES:
                        for _ in range(20):
                            self.particles.append(Particle(*event.pos))

                    # Start drawing
                    elif self.current_scene == Scene.DRAWING:
                        self.mouse_drawing = [event.pos]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.current_scene == Scene.DRAWING:
                    if len(self.mouse_drawing) > 1:
                        # Keep the drawing
                        self.mouse_drawing = []

            elif event.type == pygame.MOUSEMOTION:
                # Track mouse trail
                self.mouse_trail.append(event.pos)
                if len(self.mouse_trail) > 50:
                    self.mouse_trail.pop(0)

                # Continue drawing
                if event.buttons[0] and self.current_scene == Scene.DRAWING:
                    self.mouse_drawing.append(event.pos)

        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)
            if button.pressed and self.current_scene == Scene.MENU:
                self.current_scene = button.scene

    def update(self):
        """Update all animated elements"""
        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

        # Update physics balls
        for ball in self.balls:
            ball.update()

        # Update animated sprites
        for sprite in self.sprites:
            sprite.update()

        # Create ambient particles
        if self.current_scene == Scene.PARTICLES and random.random() < 0.3:
            self.particles.append(Particle(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT))

    def draw_menu(self):
        """Draw main menu"""
        # Title with shadow effect
        shadow_surf = self.title_font.render("Pygame Feature Showcase", True, GRAY)
        title_surf = self.title_font.render("Pygame Feature Showcase", True, WHITE)

        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 3, 100 + 3))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))

        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)

        # Instructions
        inst_surf = self.subtitle_font.render("Click a button or press 1-7 to explore features", True, WHITE)
        inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(inst_surf, inst_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # ESC instruction
        esc_surf = self.info_font.render("Press ESC to return to menu", True, GRAY)
        self.screen.blit(esc_surf, (10, SCREEN_HEIGHT - 30))

    def draw_sprites(self):
        """Sprite and animation demonstration"""
        title_surf = self.subtitle_font.render("Animated Sprites & Transformations", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        # Draw animated sprites
        for sprite in self.sprites:
            sprite.draw(self.screen)

        # Draw rotating rect
        rect_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(rect_surf, ORANGE, (0, 0, 100, 100))
        angle = (pygame.time.get_ticks() / 10) % 360
        rotated = pygame.transform.rotate(rect_surf, angle)

        # Scale demonstration
        scale_factor = 1 + math.sin(pygame.time.get_ticks() / 500) * 0.5
        scaled = pygame.transform.scale(rotated,
                                       (int(100 * scale_factor), int(100 * scale_factor)))

        rect = scaled.get_rect(center=(SCREEN_WIDTH - 200, 400))
        self.screen.blit(scaled, rect)

        # Flip demonstration
        flip_surf = pygame.Surface((80, 80))
        flip_surf.fill(PURPLE)
        pygame.draw.circle(flip_surf, WHITE, (20, 40), 10)

        if (pygame.time.get_ticks() // 1000) % 2:
            flipped = pygame.transform.flip(flip_surf, True, False)
        else:
            flipped = flip_surf

        self.screen.blit(flipped, (100, 400))

        info_surf = self.info_font.render("Rotation, Scaling, Color Shifting, Flipping", True, GRAY)
        self.screen.blit(info_surf, (50, 70))

    def draw_particles(self):
        """Particle system demonstration"""
        title_surf = self.subtitle_font.render("Particle System", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        info_surf = self.info_font.render("Click to create particle bursts", True, GRAY)
        self.screen.blit(info_surf, (50, 70))

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw particle count
        count_surf = self.info_font.render(f"Particles: {len(self.particles)}", True, WHITE)
        self.screen.blit(count_surf, (10, SCREEN_HEIGHT - 30))

    def draw_physics(self):
        """Physics simulation demonstration"""
        title_surf = self.subtitle_font.render("Physics Simulation", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        info_surf = self.info_font.render("Gravity, Bouncing, Damping", True, GRAY)
        self.screen.blit(info_surf, (50, 70))

        # Draw floor
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

        # Draw balls
        for ball in self.balls:
            ball.draw(self.screen)

        # Add new ball on spacebar
        if pygame.K_SPACE in self.keys_pressed:
            if len(self.balls) < 20:
                self.balls.append(BouncingBall(random.randint(50, SCREEN_WIDTH - 50), 50))

        count_surf = self.info_font.render(f"Balls: {len(self.balls)} (Press SPACE to add)", True, WHITE)
        self.screen.blit(count_surf, (10, SCREEN_HEIGHT - 130))

    def draw_drawing(self):
        """Drawing primitives demonstration"""
        title_surf = self.subtitle_font.render("Drawing Primitives", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        info_surf = self.info_font.render("Lines, Circles, Rectangles, Polygons, Arcs", True, GRAY)
        self.screen.blit(info_surf, (50, 70))

        # Draw various shapes
        y_offset = 150

        # Lines
        pygame.draw.line(self.screen, RED, (50, y_offset), (150, y_offset + 50), 3)
        pygame.draw.lines(self.screen, GREEN, False,
                         [(200, y_offset), (250, y_offset + 50), (300, y_offset), (350, y_offset + 50)], 2)

        # Circles
        pygame.draw.circle(self.screen, BLUE, (450, y_offset + 25), 30)
        pygame.draw.circle(self.screen, YELLOW, (550, y_offset + 25), 30, 5)

        # Rectangles
        pygame.draw.rect(self.screen, PURPLE, (50, y_offset + 100, 100, 60))
        pygame.draw.rect(self.screen, ORANGE, (200, y_offset + 100, 100, 60), 3)

        # Polygon
        points = [(400, y_offset + 100), (450, y_offset + 80),
                 (500, y_offset + 100), (480, y_offset + 150), (420, y_offset + 150)]
        pygame.draw.polygon(self.screen, CYAN, points)

        # Arc
        pygame.draw.arc(self.screen, WHITE, (550, y_offset + 100, 100, 80), 0, math.pi, 3)

        # Ellipse
        pygame.draw.ellipse(self.screen, RED, (700, y_offset + 100, 120, 60))

        # Anti-aliased line
        pygame.draw.aaline(self.screen, WHITE, (50, y_offset + 200), (750, y_offset + 250))

        # User drawing
        if len(self.mouse_drawing) > 1:
            pygame.draw.lines(self.screen, WHITE, False, self.mouse_drawing, 3)

        draw_inst = self.info_font.render("Click and drag to draw", True, GRAY)
        self.screen.blit(draw_inst, (50, SCREEN_HEIGHT - 30))

    def draw_text(self):
        """Text rendering demonstration"""
        title_surf = self.subtitle_font.render("Text Rendering", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        y = 100

        # Different fonts
        fonts = [
            (pygame.font.Font(None, 24), "Default Font Size 24"),
            (pygame.font.Font(None, 36), "Default Font Size 36"),
            (pygame.font.Font(None, 48), "Default Font Size 48"),
        ]

        try:
            # Try to use system fonts
            fonts.extend([
                (pygame.font.SysFont("arial", 32), "Arial Font"),
                (pygame.font.SysFont("times", 32), "Times Font"),
                (pygame.font.SysFont("courier", 32), "Courier Font"),
            ])
        except:
            pass

        for font, text in fonts:
            text_surf = font.render(text, True, WHITE)
            self.screen.blit(text_surf, (50, y))
            y += text_surf.get_height() + 10

        # Colored text
        y += 20
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
        color_text = "Colored Text"
        for i, char in enumerate(color_text):
            char_surf = self.subtitle_font.render(char, True, colors[i % len(colors)])
            self.screen.blit(char_surf, (50 + i * 25, y))

        # Anti-aliased vs non-anti-aliased
        y += 60
        aa_surf = self.subtitle_font.render("Anti-aliased Text", True, WHITE)
        no_aa_surf = self.subtitle_font.render("Non Anti-aliased Text", False, WHITE)
        self.screen.blit(aa_surf, (50, y))
        self.screen.blit(no_aa_surf, (350, y))

        # Multiline text
        y += 60
        lines = ["This is line 1", "This is line 2", "This is line 3"]
        for i, line in enumerate(lines):
            line_surf = self.info_font.render(line, True, GRAY)
            self.screen.blit(line_surf, (50, y + i * 25))

    def draw_input(self):
        """Input handling demonstration"""
        title_surf = self.subtitle_font.render("Input Handling", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        y = 100

        # Mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_text = f"Mouse Position: ({mouse_x}, {mouse_y})"
        mouse_surf = self.info_font.render(mouse_text, True, WHITE)
        self.screen.blit(mouse_surf, (50, y))

        # Mouse buttons
        y += 30
        buttons = pygame.mouse.get_pressed()
        button_text = f"Mouse Buttons: Left={buttons[0]} Middle={buttons[1]} Right={buttons[2]}"
        button_surf = self.info_font.render(button_text, True, WHITE)
        self.screen.blit(button_surf, (50, y))

        # Draw mouse trail
        if len(self.mouse_trail) > 1:
            for i in range(len(self.mouse_trail) - 1):
                alpha = int(255 * (i / len(self.mouse_trail)))
                color = (*WHITE[:3], alpha)
                pygame.draw.line(self.screen, WHITE, self.mouse_trail[i], self.mouse_trail[i + 1], 2)

        # Keyboard input
        y += 60
        key_text = "Keys Pressed: " + ", ".join([pygame.key.name(k) for k in self.keys_pressed][:5])
        if len(self.keys_pressed) > 5:
            key_text += "..."
        key_surf = self.info_font.render(key_text, True, WHITE)
        self.screen.blit(key_surf, (50, y))

        # Modifier keys
        y += 30
        mods = pygame.key.get_mods()
        mod_text = f"Modifiers: Shift={bool(mods & pygame.KMOD_SHIFT)} "
        mod_text += f"Ctrl={bool(mods & pygame.KMOD_CTRL)} "
        mod_text += f"Alt={bool(mods & pygame.KMOD_ALT)}"
        mod_surf = self.info_font.render(mod_text, True, WHITE)
        self.screen.blit(mod_surf, (50, y))

        # Interactive element
        y += 60
        inst_surf = self.info_font.render("Use WASD or Arrow Keys to move the square", True, GRAY)
        self.screen.blit(inst_surf, (50, y))

        # Moveable square
        square_x = getattr(self, 'square_x', SCREEN_WIDTH // 2)
        square_y = getattr(self, 'square_y', 400)

        speed = 5
        if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            square_x -= speed
        if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            square_x += speed
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            square_y -= speed
        if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            square_y += speed

        # Keep square on screen
        square_x = max(25, min(SCREEN_WIDTH - 25, square_x))
        square_y = max(25, min(SCREEN_HEIGHT - 25, square_y))

        self.square_x = square_x
        self.square_y = square_y

        pygame.draw.rect(self.screen, YELLOW, (square_x - 25, square_y - 25, 50, 50))

    def draw_collision(self):
        """Collision detection demonstration"""
        title_surf = self.subtitle_font.render("Collision Detection", True, WHITE)
        self.screen.blit(title_surf, (50, 30))

        info_surf = self.info_font.render("Rectangle and Circle Collision", True, GRAY)
        self.screen.blit(info_surf, (50, 70))

        # Get mouse position for interactive collision
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Static rectangles
        rect1 = pygame.Rect(200, 200, 100, 80)
        rect2 = pygame.Rect(mouse_x - 50, mouse_y - 40, 100, 80)

        # Check rectangle collision
        rect_colliding = rect1.colliderect(rect2)

        # Draw rectangles
        color1 = RED if rect_colliding else GREEN
        pygame.draw.rect(self.screen, color1, rect1)
        pygame.draw.rect(self.screen, BLUE, rect2)
        pygame.draw.rect(self.screen, BLACK, rect1, 2)
        pygame.draw.rect(self.screen, BLACK, rect2, 2)

        # Circle collision
        circle1_pos = (500, 250)
        circle1_radius = 50
        circle2_pos = (mouse_x, mouse_y)
        circle2_radius = 40

        # Check circle collision
        dx = circle1_pos[0] - circle2_pos[0]
        dy = circle1_pos[1] - circle2_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        circle_colliding = distance < (circle1_radius + circle2_radius)

        # Draw circles
        color2 = RED if circle_colliding else GREEN
        pygame.draw.circle(self.screen, color2, circle1_pos, circle1_radius)
        pygame.draw.circle(self.screen, YELLOW, circle2_pos, circle2_radius)
        pygame.draw.circle(self.screen, BLACK, circle1_pos, circle1_radius, 2)
        pygame.draw.circle(self.screen, BLACK, circle2_pos, circle2_radius, 2)

        # Point in rectangle
        point = (mouse_x, mouse_y)
        test_rect = pygame.Rect(200, 400, 150, 100)
        point_in_rect = test_rect.collidepoint(point)

        rect_color = RED if point_in_rect else CYAN
        pygame.draw.rect(self.screen, rect_color, test_rect)
        pygame.draw.rect(self.screen, BLACK, test_rect, 2)

        # Draw collision status
        y = 550
        status_text = f"Rectangle Collision: {rect_colliding}"
        status_surf = self.info_font.render(status_text, True, WHITE)
        self.screen.blit(status_surf, (50, y))

        y += 30
        status_text = f"Circle Collision: {circle_colliding}"
        status_surf = self.info_font.render(status_text, True, WHITE)
        self.screen.blit(status_surf, (50, y))

        y += 30
        status_text = f"Point in Rectangle: {point_in_rect}"
        status_surf = self.info_font.render(status_text, True, WHITE)
        self.screen.blit(status_surf, (50, y))

        inst = self.info_font.render("Move mouse to test collisions", True, GRAY)
        self.screen.blit(inst, (50, SCREEN_HEIGHT - 30))

    def draw(self):
        """Main drawing function"""
        # Clear screen with gradient background
        for y in range(SCREEN_HEIGHT):
            color_value = int(20 + (y / SCREEN_HEIGHT) * 30)
            pygame.draw.line(self.screen, (color_value, 0, color_value),
                           (0, y), (SCREEN_WIDTH, y))

        # Draw based on current scene
        if self.current_scene == Scene.MENU:
            self.draw_menu()
        elif self.current_scene == Scene.SPRITES:
            self.draw_sprites()
        elif self.current_scene == Scene.PARTICLES:
            self.draw_particles()
        elif self.current_scene == Scene.PHYSICS:
            self.draw_physics()
        elif self.current_scene == Scene.DRAWING:
            self.draw_drawing()
        elif self.current_scene == Scene.TEXT:
            self.draw_text()
        elif self.current_scene == Scene.INPUT:
            self.draw_input()
        elif self.current_scene == Scene.COLLISION:
            self.draw_collision()

        # Draw FPS counter
        fps = int(self.clock.get_fps())
        fps_surf = self.info_font.render(f"FPS: {fps}", True, GREEN if fps > 55 else YELLOW if fps > 30 else RED)
        self.screen.blit(fps_surf, (SCREEN_WIDTH - 100, 10))

        # Draw current scene indicator
        if self.current_scene != Scene.MENU:
            scene_text = f"Scene: {self.current_scene.name} (ESC for menu)"
            scene_surf = self.info_font.render(scene_text, True, WHITE)
            self.screen.blit(scene_surf, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 30))

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(FPS)

        # Cleanup
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    showcase = PygameShowcase()
    showcase.run()

if __name__ == "__main__":
    main()