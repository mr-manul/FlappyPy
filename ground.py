import pygame

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 40

class Ground:
    def __init__(self):
        self.top = SCREEN_HEIGHT - GROUND_HEIGHT
        self.width = SCREEN_WIDTH
        self.height = GROUND_HEIGHT
        self.rect = pygame.Rect(0, self.top, self.width, self.height)

        # Load the grass image
        self.grass_image = pygame.image.load("images/ground.png").convert_alpha()

        # Scale the image while keeping the height at 40
        self.grass_image = pygame.transform.scale(self.grass_image, (SCREEN_WIDTH, self.height))

    def draw(self, screen):
        """Draw the ground with the ground image."""
        # Draw the grass image, stretched to cover the entire width
        screen.blit(self.grass_image, (0, self.top))

    def collide(self, bird):
        """Check if the bird collides with the ground."""
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        return self.rect.colliderect(bird_rect)
