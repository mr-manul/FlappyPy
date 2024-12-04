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
        pygame.display.set_caption("FlappyPy")
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = 0  # Initialize high score to 0
        self.running = False

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

    def show_game_over_screen(self):
        """Display the game over screen with retry and quit options."""
        font = pygame.font.SysFont("Arial", 48)
        button_font = pygame.font.SysFont("Arial", 36)

        # Button properties
        button_width = 200
        button_height = 60
        retry_button_x = (SCREEN_WIDTH - button_width) // 2
        retry_button_y = (SCREEN_HEIGHT - button_height) // 2 - 40
        quit_button_x = retry_button_x
        quit_button_y = retry_button_y + 80

        while True:
            self.screen.fill(WHITE)  # Clear screen with white background

            # Game over text
            game_over_text = font.render("Game Over!", True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(game_over_text, game_over_rect)

            # Retry button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            retry_hovered = retry_button_x < mouse_x < retry_button_x + button_width and \
                            retry_button_y < mouse_y < retry_button_y + button_height
            retry_button_color = BUTTON_HOVER_COLOR if retry_hovered else BUTTON_COLOR
            pygame.draw.rect(self.screen, retry_button_color, (retry_button_x, retry_button_y, button_width, button_height))
            retry_text = button_font.render("Retry", True, BUTTON_TEXT_COLOR)
            retry_text_rect = retry_text.get_rect(center=(retry_button_x + button_width // 2, retry_button_y + button_height // 2))
            self.screen.blit(retry_text, retry_text_rect)

            # Quit button
            quit_hovered = quit_button_x < mouse_x < quit_button_x + button_width and \
                        quit_button_y < mouse_y < quit_button_y + button_height
            quit_button_color = BUTTON_HOVER_COLOR if quit_hovered else BUTTON_COLOR
            pygame.draw.rect(self.screen, quit_button_color, (quit_button_x, quit_button_y, button_width, button_height))
            quit_text = button_font.render("Quit", True, BUTTON_TEXT_COLOR)
            quit_text_rect = quit_text.get_rect(center=(quit_button_x + button_width // 2, quit_button_y + button_height // 2))
            self.screen.blit(quit_text, quit_text_rect)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_hovered:
                        # Restart the game directly
                        self.__init__()  # Reinitialize the game
                        return  # Exit this screen and go back to the main game loop
                    elif quit_hovered:
                        # Immediately stop the game and return to the start screen
                        self.running = False  # Ensure the game loop exits
                        return

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        """Main game loop."""
        while True:  # Keep the game loop running indefinitely until explicitly quit
            if not self.running:
                self.show_start_screen()  # Show the starting screen
                self.__init__()  # Reset the game state after the start screen
                self.running = True  # Ensure the game loop runs

            # Main game loop
            while self.running:
                self.screen.fill(WHITE)  # Clear the screen with a white background

                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
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
                        self.show_game_over_screen()  # Show the game-over screen
                        self.score > self.high_score
                        self.high_score = self.score
                        break

                # Draw the bird and pipes
                self.bird.draw(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)

            # Draw the score and high score
            font = pygame.font.SysFont("Arial", 36)
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))  # Score in top-left corner
            self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))  # High score in top-right corner

                # Update the display
                pygame.display.flip()
                self.clock.tick(FPS)




