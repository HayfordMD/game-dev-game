import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crystal Caverns")
clock = pygame.time.Clock()

# 4 color palette - Gameboy style
BLACK = (15, 56, 15)
DARK_GREEN = (48, 98, 48)
LIGHT_GREEN = (139, 172, 15)
PALE_GREEN = (155, 188, 15)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.vel_x = 0
        self.vel_y = 0
        self.base_speed = 4
        self.speed_multiplier = 1.0
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2
        self.facing_right = True
        self.alive = True

    def update(self, level):
        # Apply gravity
        if not self.on_ground:
            self.vel_y += 0.8
            if self.vel_y > 15:
                self.vel_y = 15

        # Horizontal movement
        self.x += self.vel_x * self.speed_multiplier
        self.check_tile_collisions(level, True)

        # Vertical movement
        self.y += self.vel_y
        self.on_ground = False
        self.check_tile_collisions(level, False)

        # Keep player in bounds
        self.x = max(0, min(self.x, WIDTH - self.width))

        # Death if fall off screen
        if self.y > HEIGHT:
            self.alive = False

    def check_tile_collisions(self, level, horizontal):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for row_idx, row in enumerate(level.tiles):
            for col_idx, tile in enumerate(row):
                if tile == 1:  # Solid tile
                    tile_rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        if horizontal:
                            if self.vel_x > 0:
                                self.x = tile_rect.left - self.width
                            elif self.vel_x < 0:
                                self.x = tile_rect.right
                        else:
                            if self.vel_y > 0:
                                self.y = tile_rect.top - self.height
                                self.vel_y = 0
                                self.on_ground = True
                                self.jump_count = 0
                            elif self.vel_y < 0:
                                self.y = tile_rect.bottom
                                self.vel_y = 0
                elif tile == 2:  # Spike
                    tile_rect = pygame.Rect(col_idx * TILE_SIZE + 8, row_idx * TILE_SIZE + 16, 16, 16)
                    if player_rect.colliderect(tile_rect):
                        self.alive = False

    def jump(self):
        if self.jump_count < self.max_jumps:
            self.vel_y = -13
            self.jump_count += 1

    def move(self, direction):
        self.vel_x = direction * self.base_speed
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False

    def draw(self, screen):
        # Simple character representation
        pygame.draw.rect(screen, PALE_GREEN, (self.x + 4, self.y + 4, 16, 16))
        # Eyes to show direction
        if self.facing_right:
            pygame.draw.rect(screen, BLACK, (self.x + 14, self.y + 8, 4, 4))
        else:
            pygame.draw.rect(screen, BLACK, (self.x + 6, self.y + 8, 4, 4))

class Crystal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.bob_offset = 0

    def update(self):
        self.bob_offset += 0.1

    def draw(self, screen):
        if not self.collected:
            y_offset = math.sin(self.bob_offset) * 4
            points = [
                (self.x + 16, self.y + 4 + y_offset),
                (self.x + 8, self.y + 12 + y_offset),
                (self.x + 16, self.y + 20 + y_offset),
                (self.x + 24, self.y + 12 + y_offset)
            ]
            pygame.draw.polygon(screen, PALE_GREEN, points)
            pygame.draw.polygon(screen, LIGHT_GREEN, points, 2)

class Enemy:
    def __init__(self, x, y, enemy_type="walker"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.type = enemy_type
        self.vel_x = 2 if enemy_type == "walker" else 3
        self.vel_y = 0

    def update(self, level):
        if self.type == "walker":
            self.x += self.vel_x

            # Check for walls or edges
            future_x = self.x + (self.vel_x * 5)
            check_x = future_x // TILE_SIZE
            check_y = (self.y + self.height + 1) // TILE_SIZE

            # Turn around at walls
            if check_x < 0 or check_x >= len(level.tiles[0]):
                self.vel_x *= -1
            elif check_y < len(level.tiles):
                if level.tiles[check_y][check_x] != 1:  # No ground ahead
                    self.vel_x *= -1
                wall_check_y = self.y // TILE_SIZE
                if wall_check_y >= 0 and level.tiles[wall_check_y][check_x] == 1:  # Wall ahead
                    self.vel_x *= -1

        elif self.type == "flyer":
            self.x += self.vel_x
            if self.x < 0 or self.x > WIDTH - self.width:
                self.vel_x *= -1

    def draw(self, screen):
        if self.type == "walker":
            # Spider-like enemy
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 4, self.y + 8, 16, 12))
            # Legs
            for i in range(4):
                pygame.draw.rect(screen, DARK_GREEN, (self.x + i * 6, self.y + 16, 2, 8))
        else:
            # Bat-like enemy
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 8, self.y + 8, 8, 8))
            # Wings
            pygame.draw.polygon(screen, DARK_GREEN, [
                (self.x, self.y + 10),
                (self.x + 8, self.y + 12),
                (self.x + 4, self.y + 18)
            ])
            pygame.draw.polygon(screen, DARK_GREEN, [
                (self.x + 24, self.y + 10),
                (self.x + 16, self.y + 12),
                (self.x + 20, self.y + 18)
            ])

class Level:
    def __init__(self):
        self.tiles = []
        self.generate_level()

    def generate_level(self):
        # Initialize empty level
        cols = 25
        rows = 19
        self.tiles = [[0 for _ in range(cols)] for _ in range(rows)]

        # Create floor
        for col in range(cols):
            self.tiles[rows-1][col] = 1
            self.tiles[rows-2][col] = 1

        # Add guaranteed safe starting area
        for row in range(13, 17):
            for col in range(0, 4):
                if row < 16:
                    self.tiles[row][col] = 0
                self.tiles[row][0] = 1
                self.tiles[row][1] = 1
                self.tiles[row][2] = 1

        # Create a guaranteed path with platforms
        platform_positions = [
            (3, 13, 3),   # (col, row, width)
            (8, 11, 4),
            (14, 12, 3),
            (19, 10, 4),
            (6, 7, 3),
            (12, 5, 4),
            (18, 8, 3)
        ]

        # Add main platforms
        for col, row, width in platform_positions:
            for w in range(width):
                if col + w < cols:
                    self.tiles[row][col + w] = 1

        # Add random additional platforms
        for _ in range(random.randint(3, 6)):
            col = random.randint(2, cols - 5)
            row = random.randint(3, rows - 5)
            width = random.randint(2, 4)

            # Check if platform doesn't block existing paths too much
            valid = True
            for w in range(width):
                if col + w < cols:
                    # Don't place directly above or below existing platforms
                    if row > 0 and self.tiles[row-1][col+w] == 1:
                        valid = False
                    if row < rows-1 and self.tiles[row+1][col+w] == 1:
                        valid = False

            if valid:
                for w in range(width):
                    if col + w < cols:
                        self.tiles[row][col + w] = 1

        # Add spikes but not in starting area or critical path
        spike_count = random.randint(2, 5)
        for _ in range(spike_count):
            col = random.randint(5, cols - 2)
            # Only place spikes on the ground or on platforms
            for row in range(rows - 3, 0, -1):
                if self.tiles[row][col] == 1 and self.tiles[row-1][col] == 0:
                    # Don't place spikes too close together
                    has_nearby_spike = False
                    for check_col in range(max(0, col-2), min(cols, col+3)):
                        if self.tiles[row-1][check_col] == 2:
                            has_nearby_spike = True
                            break

                    if not has_nearby_spike and random.random() < 0.3:
                        self.tiles[row-1][col] = 2
                        if col+1 < cols and random.random() < 0.5:
                            self.tiles[row-1][col+1] = 2
                        break

        # Create gap in floor for added challenge but ensure it's jumpable
        gap_start = random.randint(10, 15)
        gap_width = 2  # Keep gap small enough to jump
        for col in range(gap_start, min(gap_start + gap_width, cols)):
            self.tiles[rows-1][col] = 0
            self.tiles[rows-2][col] = 0

    def draw(self, screen):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if tile == 1:
                    # Draw solid tile
                    pygame.draw.rect(screen, DARK_GREEN, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, LIGHT_GREEN, (x, y, TILE_SIZE, TILE_SIZE), 2)
                elif tile == 2:
                    # Draw spike
                    points = [
                        (x + 16, y + 8),
                        (x + 8, y + 24),
                        (x + 24, y + 24)
                    ]
                    pygame.draw.polygon(screen, DARK_GREEN, points)

class Game:
    def __init__(self):
        self.player = Player(50, 400)
        self.level = Level()
        self.crystals = []
        self.enemies = []
        self.generate_entities()
        self.score = 0
        self.time_played = 0
        self.last_speed_reduction = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.game_over = False
        self.level_complete = False

    def generate_entities(self):
        # Place crystals on platforms
        cols = len(self.level.tiles[0])
        rows = len(self.level.tiles)

        # Find valid platform positions for crystals
        platform_tops = []
        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                # Check if this is top of a platform
                if (self.level.tiles[row][col] == 1 and
                    self.level.tiles[row-1][col] == 0 and
                    col > 2):  # Not in starting area
                    platform_tops.append((col, row))

        # Place 5 crystals on random platforms
        if len(platform_tops) >= 5:
            selected_positions = random.sample(platform_tops, 5)
        else:
            selected_positions = platform_tops
            # Add some floating crystals if not enough platforms
            for _ in range(5 - len(platform_tops)):
                col = random.randint(4, cols - 2)
                row = random.randint(3, rows - 6)
                selected_positions.append((col, row))

        for col, row in selected_positions:
            self.crystals.append(Crystal(col * TILE_SIZE, (row - 1) * TILE_SIZE))

        # Place enemies
        enemy_count = random.randint(3, 5)

        # Add walking enemies on platforms
        for _ in range(enemy_count // 2):
            if platform_tops:
                col, row = random.choice(platform_tops)
                # Don't place enemies in starting area
                if col > 4:
                    self.enemies.append(Enemy(col * TILE_SIZE, (row - 1) * TILE_SIZE, "walker"))

        # Add flying enemies
        for _ in range(enemy_count - len(self.enemies)):
            col = random.randint(6, cols - 2)
            row = random.randint(2, 8)
            self.enemies.append(Enemy(col * TILE_SIZE, row * TILE_SIZE, "flyer"))

    def update(self):
        if self.game_over or self.level_complete:
            return

        self.time_played += 1/60

        # Reduce speed every 30 seconds
        if self.time_played - self.last_speed_reduction >= 30:
            self.player.speed_multiplier *= 0.85
            self.last_speed_reduction = self.time_played

        self.player.update(self.level)

        # Update crystals
        for crystal in self.crystals:
            crystal.update()
            if not crystal.collected:
                crystal_rect = pygame.Rect(crystal.x, crystal.y, 32, 24)
                player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                if player_rect.colliderect(crystal_rect):
                    crystal.collected = True
                    self.score += 1

        # Check if all crystals collected
        if all(c.collected for c in self.crystals):
            self.level_complete = True
            self.score += 1  # Room completion bonus

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.level)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            if player_rect.colliderect(enemy_rect):
                self.player.alive = False

        if not self.player.alive:
            self.game_over = True

    def draw(self, screen):
        screen.fill(BLACK)

        self.level.draw(screen)

        for crystal in self.crystals:
            crystal.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        if self.player.alive:
            self.player.draw(screen)

        # UI
        score_text = self.small_font.render(f"Score: {self.score}", True, PALE_GREEN)
        screen.blit(score_text, (10, 10))

        time_text = self.small_font.render(f"Time: {int(self.time_played)}s", True, PALE_GREEN)
        screen.blit(time_text, (10, 35))

        speed_text = self.small_font.render(f"Speed: {int(self.player.speed_multiplier * 100)}%", True, PALE_GREEN)
        screen.blit(speed_text, (10, 60))

        crystals_left = sum(1 for c in self.crystals if not c.collected)
        crystal_text = self.small_font.render(f"Crystals: {crystals_left}", True, PALE_GREEN)
        screen.blit(crystal_text, (WIDTH - 150, 10))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, PALE_GREEN)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(game_over_text, text_rect)

            restart_text = self.small_font.render("Press SPACE to restart", True, PALE_GREEN)
            text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            screen.blit(restart_text, text_rect)

        elif self.level_complete:
            complete_text = self.font.render("LEVEL COMPLETE!", True, PALE_GREEN)
            text_rect = complete_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(complete_text, text_rect)

            score_text = self.small_font.render(f"Final Score: {self.score}", True, PALE_GREEN)
            text_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            screen.blit(score_text, text_rect)

    def restart(self):
        self.__init__()

def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.game_over or game.level_complete:
                        game.restart()
                    else:
                        game.player.jump()

        keys = pygame.key.get_pressed()
        if not game.game_over and not game.level_complete:
            if keys[pygame.K_LEFT]:
                game.player.move(-1)
            elif keys[pygame.K_RIGHT]:
                game.player.move(1)
            else:
                game.player.vel_x = 0

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()