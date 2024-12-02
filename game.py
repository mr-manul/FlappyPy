import pygame
import random
from bird import Bird
from pipe import Pipe

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = WHITE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.running = True

    def create_pipe(self):
        """Generate a new pipe with a random gap height."""
        gap_height = random.randint(100, SCREEN_HEIGHT - 250)
        new_pipe = Pipe(SCREEN_WIDTH, gap_height)
        self.pipes.append(new_pipe)

    def show_start_screen(self):
        """Display the start screen with a button."""
        font = pygame.font.SysFont("Arial", 48)
        button_font = pygame.font.SysFont("Arial", 36)

        # Button properties
        button_width = 200
        button_height = 60
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = (SCREEN_HEIGHT - button_height) // 2

        start_screen = True
        while start_screen:
            self.screen.fill(WHITE)  # Clear screen with white background

            # Title text
            title_text = font.render("Flappy Bird", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)

            # Button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height
            button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))

            # Button text
            button_text = button_font.render("Start Game", True, BUTTON_TEXT_COLOR)
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(button_text, button_text_rect)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                    start_screen = False

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        """Main game loop."""
        self.show_start_screen()  # Show the starting screen before the game starts

        while self.running:
            self.screen.fill(WHITE)  # Clear the screen with a white background

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            # Update the bird
            self.bird.update()

            # Add a new pipe if needed
            if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - 300:
                self.create_pipe()

            # Update pipes
            for pipe in self.pipes:
                pipe.update()
                if pipe.off_screen():
                    self.pipes.remove(pipe)
                    self.score += 1  # Increment score when a pipe goes off-screen

            # Check collisions
            for pipe in self.pipes:
                if pipe.collide(self.bird):
                    print(f"Game Over! Your Score: {self.score}")
                    self.running = False

            # Draw the bird and pipes
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)

            # Draw the score
            font = pygame.font.SysFont("Arial", 36)
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
