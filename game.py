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
        self.running = True

    def create_pipe(self):
        """Generate a new pipe with a random gap height."""
        gap_height = random.randint(100, SCREEN_HEIGHT - 250)
        new_pipe = Pipe(SCREEN_WIDTH, gap_height)
        self.pipes.append(new_pipe)

    def run(self):
        """Main game loop."""
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
                    # Update high score if the current score is greater
                    if self.score > self.high_score:
                        self.high_score = self.score
                    print(f"Game Over! Your Score: {self.score}, High Score: {self.high_score}")
                    self.running = False

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

        pygame.quit()