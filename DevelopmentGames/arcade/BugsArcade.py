import pygame
import random
import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from systems.game_end_manager import GameEndManager

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede Clone")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 40
        self.speed = 5
        self.width = 20
        self.height = 20
        self.shoot_cooldown = 0

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        self.x = min(WIDTH - self.width, self.x + self.speed)

    def move_up(self):
        if self.y > HEIGHT - 100:
            self.y = max(HEIGHT - 100, self.y - self.speed)

    def move_down(self):
        self.y = min(HEIGHT - self.height, self.y + self.speed)

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x + 8, self.y - 5, 4, 10))

    def can_shoot(self):
        return self.shoot_cooldown == 0

    def shoot(self):
        if self.can_shoot():
            self.shoot_cooldown = 10
            return Bullet(self.x + self.width // 2, self.y)
        return None

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.width = 3
        self.height = 10
        self.active = True

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x - self.width // 2, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

class Mushroom:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.health = 4
        self.colors = [BROWN, (100, 50, 10), (80, 40, 8), (60, 30, 6)]

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def draw(self, screen):
        if self.health > 0:
            color = self.colors[4 - self.health]
            pygame.draw.circle(screen, color, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2 - 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

class CentipedeSegment:
    def __init__(self, x, y, is_head=False):
        self.grid_x = x
        self.grid_y = y
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.direction = 1
        self.is_head = is_head
        self.dropping = False
        self.speed = 2
        self.move_timer = 0

    def update(self, mushrooms):
        self.move_timer += 1
        if self.move_timer < 5:
            return

        self.move_timer = 0

        if self.dropping:
            self.grid_y += 1
            self.y = self.grid_y * GRID_SIZE
            self.dropping = False
            self.direction *= -1
        else:
            next_x = self.grid_x + self.direction
            hit_wall = next_x < 0 or next_x >= COLS
            hit_mushroom = False

            for mushroom in mushrooms:
                if mushroom.grid_x == next_x and mushroom.grid_y == self.grid_y:
                    hit_mushroom = True
                    break

            if hit_wall or hit_mushroom:
                if self.grid_y < ROWS - 1:
                    self.dropping = True
                else:
                    self.direction *= -1
            else:
                self.grid_x = next_x
                self.x = self.grid_x * GRID_SIZE

    def draw(self, screen):
        color = RED if self.is_head else YELLOW
        pygame.draw.circle(screen, color, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2 - 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

class Spider:
    def __init__(self):
        self.x = random.choice([0, WIDTH])
        self.y = random.randint(HEIGHT - 150, HEIGHT - 50)
        self.vel_x = 3 if self.x == 0 else -3
        self.vel_y = random.uniform(-2, 2)
        self.width = 25
        self.height = 25
        self.active = True
        self.zigzag_timer = 0

    def update(self):
        self.x += self.vel_x
        self.zigzag_timer += 1

        if self.zigzag_timer % 30 == 0:
            self.vel_y = random.uniform(-3, 3)

        self.y += self.vel_y

        if self.y < HEIGHT - 150:
            self.y = HEIGHT - 150
            self.vel_y = abs(self.vel_y)
        elif self.y > HEIGHT - 20:
            self.y = HEIGHT - 20
            self.vel_y = -abs(self.vel_y)

        if self.x < -self.width or self.x > WIDTH:
            self.active = False

    def draw(self, screen):
        pygame.draw.ellipse(screen, PURPLE, (self.x, self.y, self.width, self.height))
        for i in range(4):
            x_offset = -10 if self.vel_x > 0 else 10
            pygame.draw.line(screen, PURPLE,
                           (self.x + self.width // 2, self.y + self.height // 2),
                           (self.x + self.width // 2 + x_offset, self.y + i * 7 - 5), 2)
            pygame.draw.line(screen, PURPLE,
                           (self.x + self.width // 2, self.y + self.height // 2),
                           (self.x + self.width // 2 - x_offset, self.y + i * 7 - 5), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Flea:
    def __init__(self):
        self.grid_x = random.randint(0, COLS - 1)
        self.x = self.grid_x * GRID_SIZE
        self.y = 0
        self.speed = 8
        self.active = True
        self.mushroom_timer = 0

    def update(self, mushrooms):
        self.y += self.speed
        self.mushroom_timer += 1

        if self.mushroom_timer > 15:
            self.mushroom_timer = 0
            grid_y = self.y // GRID_SIZE
            if grid_y < ROWS - 5 and random.random() < 0.3:
                mushroom_exists = False
                for mushroom in mushrooms:
                    if mushroom.grid_x == self.grid_x and mushroom.grid_y == grid_y:
                        mushroom_exists = True
                        break
                if not mushroom_exists:
                    mushrooms.append(Mushroom(self.grid_x, grid_y))

        if self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        pygame.draw.ellipse(screen, ORANGE, (self.x, self.y, GRID_SIZE, GRID_SIZE + 5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.mushrooms = []
        self.centipede = []
        self.spiders = []
        self.fleas = []
        self.score = 0
        self.lives = 1
        self.level = 1
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.spider_timer = 0
        self.flea_timer = 0

        self.generate_mushrooms()
        self.spawn_centipede()

    def generate_mushrooms(self):
        for _ in range(30):
            x = random.randint(0, COLS - 1)
            y = random.randint(1, ROWS - 6)
            self.mushrooms.append(Mushroom(x, y))

    def spawn_centipede(self):
        length = min(10 + self.level * 2, 20)
        start_x = COLS // 2
        for i in range(length):
            segment = CentipedeSegment(start_x - i, 0, is_head=(i == 0))
            self.centipede.append(segment)

    def update(self):
        if self.game_over:
            return

        self.player.update()

        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
                continue

            bullet_rect = bullet.get_rect()

            for mushroom in self.mushrooms[:]:
                if bullet_rect.colliderect(mushroom.get_rect()):
                    if mushroom.hit():
                        self.mushrooms.remove(mushroom)
                        self.score += 1
                    self.bullets.remove(bullet)
                    break

            for i, segment in enumerate(self.centipede[:]):
                if bullet_rect.colliderect(segment.get_rect()):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if segment.is_head:
                        self.score += 1
                    else:
                        self.score += 1

                    self.mushrooms.append(Mushroom(segment.grid_x, segment.grid_y))

                    self.centipede.remove(segment)

                    if not segment.is_head and i < len(self.centipede):
                        for j in range(i, len(self.centipede)):
                            if self.centipede[j] == segment:
                                continue
                            self.centipede[j].is_head = True
                            break

                    break

            for spider in self.spiders[:]:
                if bullet_rect.colliderect(spider.get_rect()):
                    self.bullets.remove(bullet)
                    self.spiders.remove(spider)
                    self.score += 3
                    break

            for flea in self.fleas[:]:
                if bullet_rect.colliderect(flea.get_rect()):
                    self.bullets.remove(bullet)
                    self.fleas.remove(flea)
                    self.score += 2
                    break

        for segment in self.centipede:
            segment.update(self.mushrooms)

        for spider in self.spiders[:]:
            spider.update()
            if not spider.active:
                self.spiders.remove(spider)

            for mushroom in self.mushrooms[:]:
                if spider.get_rect().colliderect(mushroom.get_rect()):
                    self.mushrooms.remove(mushroom)

        for flea in self.fleas[:]:
            flea.update(self.mushrooms)
            if not flea.active:
                self.fleas.remove(flea)

        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        for segment in self.centipede:
            if player_rect.colliderect(segment.get_rect()):
                self.lives -= 1
                self.player = Player()
                if self.lives <= 0:
                    self.game_over = True
                break

        for spider in self.spiders:
            if player_rect.colliderect(spider.get_rect()):
                self.lives -= 1
                self.player = Player()
                self.spiders.remove(spider)
                if self.lives <= 0:
                    self.game_over = True
                break

        if len(self.centipede) == 0:
            self.level += 1
            self.spawn_centipede()

        self.spider_timer += 1
        if self.spider_timer > 180 and len(self.spiders) < 2:
            if random.random() < 0.02:
                self.spiders.append(Spider())
                self.spider_timer = 0

        self.flea_timer += 1
        mushroom_count = sum(1 for m in self.mushrooms if m.grid_y > ROWS - 10)
        if self.flea_timer > 120 and mushroom_count < 5:
            if random.random() < 0.01:
                self.fleas.append(Flea())
                self.flea_timer = 0

    def shoot(self):
        if not self.game_over:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.append(bullet)

    def draw(self, screen):
        screen.fill(BLACK)

        for mushroom in self.mushrooms:
            mushroom.draw(screen)

        for segment in self.centipede:
            segment.draw(screen)

        for spider in self.spiders:
            spider.draw(screen)

        for flea in self.fleas:
            flea.draw(screen)

        if not self.game_over:
            self.player.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH - 150, 10))

        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - 40, 10))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            screen.blit(score_text, text_rect)

            restart_text = self.small_font.render("Press SPACE to continue", True, WHITE)
            text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
            screen.blit(restart_text, text_rect)

def main():
    game = Game()
    running = True
    game_ended = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.game_over and not game_ended:
                        game_ended = True
                        pygame.quit()

                        root = tk.Tk()
                        root.withdraw()
                        manager = GameEndManager()
                        manager.handle_game_end(game.score, root)

                        sys.exit(0)
                    elif not game.game_over:
                        game.shoot()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if not game.game_over:
            if keys[pygame.K_LEFT]:
                game.player.move_left()
            if keys[pygame.K_RIGHT]:
                game.player.move_right()
            if keys[pygame.K_UP]:
                game.player.move_up()
            if keys[pygame.K_DOWN]:
                game.player.move_down()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Always show results, even with 0 score
    if not game_ended:
        root = tk.Tk()
        root.withdraw()
        manager = GameEndManager()
        manager.handle_game_end(game.score, root)

if __name__ == "__main__":
    main()