import pygame

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 40
GREEN = (0, 255, 0)


class Ground:
    def __init__(self):
        self.top = SCREEN_HEIGHT - GROUND_HEIGHT
        self.width = SCREEN_WIDTH
        self.height = GROUND_HEIGHT
        self.rect = pygame.Rect(0, self.top, self.width, self.height)

    def draw(self, screen):
        """Draw the ground."""
        pygame.draw.rect(screen, GREEN, self.rect)

    def collide(self, bird):
        """Check if the bird collides with the ground."""
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        return self.rect.colliderect(bird_rect)