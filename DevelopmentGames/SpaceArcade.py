import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteorium")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.radius = 10
        self.immunity_timer = 120  # 2 seconds at 60 FPS

    def rotate(self, direction):
        self.angle += direction * 5

    def thrust(self):
        thrust_power = 0.5
        self.vel_x += math.cos(math.radians(self.angle)) * thrust_power
        self.vel_y += math.sin(math.radians(self.angle)) * thrust_power

        max_speed = 7
        speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
        if speed > max_speed:
            self.vel_x = (self.vel_x / speed) * max_speed
            self.vel_y = (self.vel_y / speed) * max_speed

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_x *= 0.99
        self.vel_y *= 0.99

        if self.immunity_timer > 0:
            self.immunity_timer -= 1

        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def draw(self, screen):
        cos_a = math.cos(math.radians(self.angle))
        sin_a = math.sin(math.radians(self.angle))

        points = [
            (self.x + cos_a * 15, self.y + sin_a * 15),
            (self.x - cos_a * 10 - sin_a * 7, self.y - sin_a * 10 + cos_a * 7),
            (self.x - cos_a * 10 + sin_a * 7, self.y - sin_a * 10 - cos_a * 7)
        ]

        # Flashing effect during immunity
        if self.immunity_timer > 0 and self.immunity_timer % 10 < 5:
            return

        pygame.draw.polygon(screen, WHITE, points, 2)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vel_x = math.cos(math.radians(angle)) * 10
        self.vel_y = math.sin(math.radians(angle)) * 10
        self.lifetime = 40
        self.radius = 2

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1

        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

        return self.lifetime > 0

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Asteroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)

        if size == "large":
            self.radius = 40
        elif size == "medium":
            self.radius = 25
        else:
            self.radius = 15

        self.vertices = []
        num_vertices = random.randint(8, 12)
        for i in range(num_vertices):
            angle = (360 / num_vertices) * i
            variance = random.uniform(0.8, 1.2)
            self.vertices.append((angle, self.radius * variance))

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.angle += self.rotation_speed

        if self.x < -self.radius:
            self.x = WIDTH + self.radius
        elif self.x > WIDTH + self.radius:
            self.x = -self.radius
        if self.y < -self.radius:
            self.y = HEIGHT + self.radius
        elif self.y > HEIGHT + self.radius:
            self.y = -self.radius

    def draw(self, screen):
        points = []
        for vertex_angle, distance in self.vertices:
            angle = math.radians(vertex_angle + self.angle)
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            points.append((x, y))
        pygame.draw.polygon(screen, WHITE, points, 2)

    def split(self):
        if self.size == "large":
            return [
                Asteroid(self.x, self.y, "medium"),
                Asteroid(self.x, self.y, "medium")
            ]
        elif self.size == "medium":
            return [
                Asteroid(self.x, self.y, "small"),
                Asteroid(self.x, self.y, "small")
            ]
        return []

class Game:
    def __init__(self):
        self.ship = Ship(WIDTH // 2, HEIGHT // 2)
        self.bullets = []
        self.asteroids = []
        self.score = 0
        self.lives = 1
        self.level = 1
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.spawn_asteroids(4)

    def spawn_asteroids(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                dist = math.sqrt((x - self.ship.x)**2 + (y - self.ship.y)**2)
                if dist > 100:
                    self.asteroids.append(Asteroid(x, y, "large"))
                    break

    def check_collision(self, obj1, obj2):
        dist = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
        return dist < obj1.radius + obj2.radius

    def update(self):
        if self.game_over:
            return

        self.ship.update()

        for bullet in self.bullets[:]:
            if not bullet.update():
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            asteroid.update()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if self.check_collision(bullet, asteroid):
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

                    self.score += 1

                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                    break

        for asteroid in self.asteroids:
            if self.check_collision(self.ship, asteroid) and self.ship.immunity_timer == 0:
                self.lives -= 1
                self.ship = Ship(WIDTH // 2, HEIGHT // 2)
                if self.lives <= 0:
                    self.game_over = True
                break

        if len(self.asteroids) == 0:
            self.level += 1
            self.spawn_asteroids(3 + self.level)

    def shoot(self):
        if not self.game_over and len(self.bullets) < 4:
            self.bullets.append(Bullet(self.ship.x, self.ship.y, self.ship.angle))

    def draw(self, screen):
        screen.fill(BLACK)

        if not self.game_over:
            self.ship.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        for asteroid in self.asteroids:
            asteroid.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))

        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (10, 90))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(game_over_text, text_rect)

            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            screen.blit(restart_text, text_rect)

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
                    if game.game_over:
                        game.restart()
                    else:
                        game.shoot()

        keys = pygame.key.get_pressed()
        if not game.game_over:
            if keys[pygame.K_LEFT]:
                game.ship.rotate(-1)
            if keys[pygame.K_RIGHT]:
                game.ship.rotate(1)
            if keys[pygame.K_UP]:
                game.ship.thrust()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()