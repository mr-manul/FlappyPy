import pygame

# Constants
BLUE = (0, 0, 255)
BIRD_WIDTH = 30
BIRD_HEIGHT = 20
GRAVITY = 0.35
JUMP_STRENGTH = -8


class Bird:
    def __init__(self):
        self.x = 200  # Initial x-coordinate
        self.y = 300  # Initial y-coordinate
        self.velocity = 0
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load('images/bird.png')

    def update(self):
        """Apply gravity and update the bird's position."""
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent the bird from going off-screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > 600 - self.height:  # Assuming screen height is 600
            self.y = 600 - self.height
            self.velocity = 0

    def jump(self):
        """Make the bird jump."""
        self.velocity = JUMP_STRENGTH

    def draw(self, screen):
        """Draw the bird on the screen."""
        screen.blit(self.image, (self.x, self.y))