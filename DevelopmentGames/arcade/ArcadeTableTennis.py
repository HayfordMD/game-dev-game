import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Table Tennis")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 80
        self.vel = 0
        self.speed = 6

    def update(self):
        self.y += self.vel
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def move(self, direction):
        self.vel = direction * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.reset()
        self.base_speed = 5
        self.speed_multiplier = 1.0

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = -5
        self.vel_y = random.uniform(-3, 3)
        self.radius = 8

    def update(self):
        # Apply speed multiplier
        actual_vel_x = self.vel_x * self.speed_multiplier
        actual_vel_y = self.vel_y * self.speed_multiplier

        self.x += actual_vel_x
        self.y += actual_vel_y

        # Bounce off top and bottom walls
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vel_y = abs(self.vel_y)
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vel_y = -abs(self.vel_y)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def check_paddle_collision(self, paddle):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)
        paddle_rect = paddle.get_rect()

        if ball_rect.colliderect(paddle_rect):
            # Calculate hit position (-1 to 1)
            paddle_center = paddle.y + paddle.height / 2
            hit_position = (self.y - paddle_center) / (paddle.height / 2)
            hit_position = max(-1, min(1, hit_position))

            # Reverse X direction and add angle based on hit position
            self.vel_x = abs(self.vel_x) if paddle.x < WIDTH // 2 else -abs(self.vel_x)
            self.vel_y = hit_position * 8  # Max Y velocity based on hit position

            # Move ball outside paddle to prevent multiple collisions
            if paddle.x < WIDTH // 2:
                self.x = paddle.x + paddle.width + self.radius + 1
            else:
                self.x = paddle.x - self.radius - 1

            return True
        return False

class AIPlayer:
    def __init__(self, paddle):
        self.paddle = paddle

    def update(self, ball):
        # Perfect AI - moves at whatever speed needed to never miss
        target_y = ball.y - self.paddle.height // 2

        # Move directly to target position at whatever speed required
        diff = target_y - self.paddle.y
        self.paddle.y = target_y

        # Keep paddle in bounds
        self.paddle.y = max(0, min(self.paddle.y, HEIGHT - self.paddle.height))

class Game:
    def __init__(self):
        self.player_paddle = Paddle(30, HEIGHT // 2 - 40)
        self.ai_paddle = Paddle(WIDTH - 45, HEIGHT // 2 - 40)
        self.ai = AIPlayer(self.ai_paddle)
        self.ball = Ball()
        self.score = 0
        self.lives = 2
        self.game_over = False
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.time_played = 0
        self.last_speed_increase = 0
        self.rallies = 0
        self.serve_delay = 0

    def update(self):
        if self.game_over:
            return

        self.time_played += 1/60

        # Handle serve delay
        if self.serve_delay > 0:
            self.serve_delay -= 1
            return

        # Update paddles
        self.player_paddle.update()
        self.ai.update(self.ball)  # AI updates position directly, no need for paddle.update()

        # Update ball
        self.ball.update()

        # Check paddle collisions
        if self.ball.check_paddle_collision(self.player_paddle):
            self.score += 1  # Point for returning volley
            self.rallies += 1
            # Speed up 15% every time player hits the ball
            self.ball.speed_multiplier *= 1.15

        if self.ball.check_paddle_collision(self.ai_paddle):
            self.rallies += 1

        # Check for scoring
        if self.ball.x < -self.ball.radius:
            # Player missed
            self.lives -= 1
            self.rallies = 0
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()
                self.serve_delay = 60  # 1 second delay

        elif self.ball.x > WIDTH + self.ball.radius:
            # AI missed (won't happen with perfect AI)
            self.score += 5  # Bonus points if AI somehow misses
            self.ball.reset()
            self.serve_delay = 60

    def draw(self, screen):
        screen.fill(BLACK)

        # Draw center line
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, y, 4, 10))

        # Draw paddles
        self.player_paddle.draw(screen)
        self.ai_paddle.draw(screen)

        # Draw ball if not in serve delay
        if self.serve_delay <= 0:
            self.ball.draw(screen)

        # Draw UI
        score_text = self.font.render(str(self.score), True, WHITE)
        screen.blit(score_text, (WIDTH // 4 - score_text.get_width() // 2, 50))

        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH // 4 - lives_text.get_width() // 2, 100))

        speed_text = self.small_font.render(f"Speed: {int(self.ball.speed_multiplier * 100)}%", True, WHITE)
        screen.blit(speed_text, (10, HEIGHT - 30))

        if self.rallies > 0:
            rally_text = self.small_font.render(f"Rally: {self.rallies}", True, WHITE)
            screen.blit(rally_text, (WIDTH // 2 - rally_text.get_width() // 2, 20))

        if self.serve_delay > 0:
            ready_text = self.small_font.render("Get Ready!", True, WHITE)
            screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2, HEIGHT // 2))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

            final_score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

            restart_text = self.small_font.render("Press SPACE to play again", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

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

        keys = pygame.key.get_pressed()
        if not game.game_over:
            if keys[pygame.K_UP]:
                game.player_paddle.move(-1)
            elif keys[pygame.K_DOWN]:
                game.player_paddle.move(1)
            else:
                game.player_paddle.vel = 0

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()