import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (64, 128, 255)
DARK_BLUE = (32, 64, 128)

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

    def draw(self, screen):
        color = LIGHT_GRAY if self.is_hovered else WHITE
        border_color = DARK_BLUE if self.is_hovered else GRAY

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)

        button_width = 200
        button_height = 60
        button_spacing = 20
        start_y = WINDOW_HEIGHT // 2 + 50

        self.new_game_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "New Game",
            self.font_button
        )

        self.load_game_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            "Load Game",
            self.font_button
        )

        self.options_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
            "Options",
            self.font_button
        )

        self.quit_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + 3 * (button_height + button_spacing),
            button_width,
            button_height,
            "Quit",
            self.font_button
        )

    def handle_event(self, event):
        if self.new_game_button.handle_event(event):
            return "new_game"
        elif self.load_game_button.handle_event(event):
            return "load_game"
        elif self.options_button.handle_event(event):
            return "options"
        elif self.quit_button.handle_event(event):
            return "quit"
        return None

    def draw(self):
        self.screen.fill(DARK_GRAY)

        title_text = self.font_title.render("Game Dev Studio", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.font_button.render("Build Your Gaming Empire", True, LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(subtitle_text, subtitle_rect)

        self.new_game_button.draw(self.screen)
        self.load_game_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)

class OptionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)

        self.back_button = Button(
            50,
            WINDOW_HEIGHT - 100,
            100,
            50,
            "Back",
            self.font_button
        )

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return "back"
        return None

    def draw(self):
        self.screen.fill(DARK_GRAY)

        title_text = self.font_title.render("Options", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        options_text = [
            "Volume: 100%",
            "Resolution: 1024x768",
            "Fullscreen: Off",
            "Auto-save: On"
        ]

        for i, text in enumerate(options_text):
            text_surface = self.font_text.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            self.screen.blit(text_surface, text_rect)

        note_text = self.font_text.render("(Options functionality coming soon)", True, GRAY)
        note_rect = note_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
        self.screen.blit(note_text, note_rect)

        self.back_button.draw(self.screen)

class LoadGameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 36)

        self.back_button = Button(
            50,
            WINDOW_HEIGHT - 100,
            100,
            50,
            "Back",
            pygame.font.Font(None, 48)
        )

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return "back"
        return None

    def draw(self):
        self.screen.fill(DARK_GRAY)

        title_text = self.font_title.render("Load Game", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        no_saves_text = self.font_text.render("No saved games found", True, GRAY)
        no_saves_rect = no_saves_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(no_saves_text, no_saves_rect)

        info_text = self.font_text.render("(Save functionality coming soon)", True, GRAY)
        info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(info_text, info_rect)

        self.back_button.draw(self.screen)

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 36)

        self.back_button = Button(
            50,
            WINDOW_HEIGHT - 100,
            100,
            50,
            "Menu",
            pygame.font.Font(None, 48)
        )

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return "menu"
        return None

    def draw(self):
        self.screen.fill(BLACK)

        title_text = self.font_title.render("Game Development Studio", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        welcome_text = [
            "Welcome to your new game development studio!",
            "",
            "Here you will:",
            "• Create amazing games",
            "• Manage your team",
            "• Build your reputation",
            "• Grow from indie dev to AAA studio",
            "",
            "(Game features coming soon)"
        ]

        for i, text in enumerate(welcome_text):
            if text:
                text_surface = self.font_text.render(text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 40))
                self.screen.blit(text_surface, text_rect)

        self.back_button.draw(self.screen)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game Dev Studio")
        self.clock = pygame.time.Clock()
        self.running = True

        self.start_menu = StartMenu(self.screen)
        self.options_menu = OptionsMenu(self.screen)
        self.load_game_screen = LoadGameScreen(self.screen)
        self.game_screen = GameScreen(self.screen)

        self.current_screen = "start"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.current_screen == "start":
                result = self.start_menu.handle_event(event)
                if result == "new_game":
                    self.current_screen = "game"
                elif result == "load_game":
                    self.current_screen = "load_game"
                elif result == "options":
                    self.current_screen = "options"
                elif result == "quit":
                    self.running = False

            elif self.current_screen == "load_game":
                result = self.load_game_screen.handle_event(event)
                if result == "back":
                    self.current_screen = "start"

            elif self.current_screen == "options":
                result = self.options_menu.handle_event(event)
                if result == "back":
                    self.current_screen = "start"

            elif self.current_screen == "game":
                result = self.game_screen.handle_event(event)
                if result == "menu":
                    self.current_screen = "start"

    def draw(self):
        if self.current_screen == "start":
            self.start_menu.draw()
        elif self.current_screen == "options":
            self.options_menu.draw()
        elif self.current_screen == "game":
            self.game_screen.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()