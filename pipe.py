import pygame

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
PIPE_WIDTH = 60
PIPE_GAP = 200
PIPE_SPEED = 3

# Placeholders for images
pipe_top_image = None
pipe_bottom_image = None

def load_pipe_images():
    """Load images after Pygame display is initialized."""
    global pipe_top_image, pipe_bottom_image
    if pipe_top_image is None or pipe_bottom_image is None:
        pipe_top_image = pygame.image.load("pipe_top.png").convert_alpha()
        pipe_bottom_image = pygame.image.load("pipe_bottom.png").convert_alpha()

class Pipe:
    def __init__(self, x, gap_height):
        load_pipe_images()  # Ensure images are loaded
        self.x = x
        self.gap_height = gap_height
        self.top = self.gap_height
        self.bottom = self.gap_height + PIPE_GAP
        self.top_image = pygame.transform.scale(pipe_top_image, (PIPE_WIDTH, self.top))
        self.bottom_image = pygame.transform.scale(pipe_bottom_image, (PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))
        self.width = PIPE_WIDTH

    def update(self):
        """Move the pipe to the left."""
        self.x -= PIPE_SPEED

    def draw(self, screen):
        """Draw the top and bottom pipes."""
        # Draw the top pipe
        screen.blit(pygame.transform.flip(self.top_image, False, True), (self.x, self.top - self.top_image.get_height()))
        # Draw the bottom pipe
        screen.blit(self.bottom_image, (self.x, self.bottom))

    def off_screen(self):
        """Check if the pipe has moved off-screen."""
        return self.x < -self.width

    def collide(self, bird):
        """Check if the bird collides with the pipes."""
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
