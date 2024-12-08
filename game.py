import pygame
import random
from bird import Bird
from pipe import Pipe
from ground import Ground
from background import generate_clouds, draw_clouds, COLORS

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = WHITE
PIPE_SPEED = 3

class Game:
    def __init__(self, high_score=0):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("FlappyPy")
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = []
        self.ground = Ground()
        self.score = 0
        self.high_score = high_score
        self.pipe_speed = PIPE_SPEED
        self.running = False
        self.pipes_move_vertically = False
        self.clouds = generate_clouds(10)

        # Button properties
        self.button_width = 200
        self.button_height = 60
        self.start_button_x = (SCREEN_WIDTH - self.button_width) // 2
        self.start_button_y = (SCREEN_HEIGHT - self.button_height) // 2
        self.quit_button_x = self.start_button_x
        self.quit_button_y = self.start_button_y + 80

    def draw_background(self):
        """Draw the background color and clouds."""
        self.screen.fill(COLORS["background"])
        draw_clouds(self.screen, self.clouds)

    def create_pipe(self):
        """Generate a new pipe with a random gap height."""
        gap_height = random.randint(100, SCREEN_HEIGHT - 250)
        new_pipe = Pipe(SCREEN_WIDTH, gap_height, self.pipe_speed)
        self.pipes.append(new_pipe)

    def draw_button(self, x, y, text, hovered):
        """Draw a button with hover effect."""
        button_color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, (x, y, self.button_width, self.button_height))
        font = pygame.font.SysFont("Nunito", 36)
        button_text = font.render(text, True, BUTTON_TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=(x + self.button_width // 2, y + self.button_height // 2))
        self.screen.blit(button_text, button_text_rect)

    def show_start_screen(self):
        """Display the start screen."""
        font = pygame.font.SysFont("Nunito", 70)

        while True:
            self.draw_background()
            title_text = font.render("Flappy Bird", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)

            # Button interactions
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_hovered = self.start_button_x < mouse_x < self.start_button_x + self.button_width and \
                            self.start_button_y < mouse_y < self.start_button_y + self.button_height
            quit_hovered = self.quit_button_x < mouse_x < self.quit_button_x + self.button_width and \
                        self.quit_button_y < mouse_y < self.quit_button_y + self.button_height

            # Draw buttons
            self.draw_button(self.start_button_x, self.start_button_y, "Start Game", start_hovered)
            self.draw_button(self.quit_button_x, self.quit_button_y, "Quit", quit_hovered)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_hovered:
                        return  # Start the game
                    elif quit_hovered:
                        pygame.quit()
                        exit()

            pygame.display.flip()
            self.clock.tick(FPS)

    def show_game_over_screen(self):
        """Display the game over screen."""
        font = pygame.font.SysFont("Nunito", 48)

        while True:
            self.draw_background()
            game_over_text = font.render("Game Over!", True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(game_over_text, game_over_rect)

            # Score display
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
            high_score_text_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            self.screen.blit(score_text, score_text_rect)
            self.screen.blit(high_score_text, high_score_text_rect)

            # Button interactions
            mouse_x, mouse_y = pygame.mouse.get_pos()
            retry_hovered = self.start_button_x < mouse_x < self.start_button_x + self.button_width and \
                            self.start_button_y < mouse_y < self.start_button_y + self.button_height
            quit_hovered = self.quit_button_x < mouse_x < self.quit_button_x + self.button_width and \
                        self.quit_button_y < mouse_y < self.quit_button_y + self.button_height

            # Draw buttons
            self.draw_button(self.start_button_x, self.start_button_y, "Retry", retry_hovered)
            self.draw_button(self.quit_button_x, self.quit_button_y, "Quit", quit_hovered)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_hovered:
                        return  # Retry the game
                    elif quit_hovered:
                        pygame.quit()
                        exit()

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        """Main game loop."""
        while True:
            if not self.running:
                self.show_start_screen()
                self.bird = Bird()
                self.pipes = []
                self.score = 0
                self.running = True
                self.pipes_move_vertically = False

            passed_pipes = []
            while self.running:
                self.draw_background()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.bird.jump()

                self.bird.update()

                if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - 300:
                    self.create_pipe()

                if self.score >= 5:
                    self.pipes_move_vertically = True

                for pipe in self.pipes:
                    pipe.update(move_vertically=self.pipes_move_vertically)
                    if pipe.off_screen():
                        self.pipes.remove(pipe)
                    if pipe not in passed_pipes and self.bird.x > pipe.x + 60:
                        self.score += 1
                        passed_pipes.append(pipe)

                if self.score >= 1 and (self.score + 1) % 10 == 0:
                    self.pipe_speed += 0.01

                for pipe in self.pipes:
                    if pipe.collide(self.bird) or self.ground.collide(self.bird):
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.running = False
                        break

                self.bird.draw(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.ground.draw(self.screen)

                font = pygame.font.SysFont("Nunito", 36)
                score_text = font.render(f"Score: {self.score}", True, BLACK)
                self.screen.blit(score_text, (10, 10))

                pygame.display.flip()
                self.clock.tick(FPS)

            self.show_game_over_screen()
