import pygame
import random

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
PIPE_WIDTH = 60
PIPE_GAP = 200
PIPE_SPEED = 3
GREEN = (0, 255, 0)


class Pipe:
    def __init__(self, x, gap_height):
        self.x = x
        self.gap_height = gap_height
        self.top = self.gap_height
        self.bottom = self.gap_height + PIPE_GAP
        self.width = PIPE_WIDTH

    def update(self):
        """Move the pipe to the left."""
        self.x -= PIPE_SPEED

    def draw(self, screen):
        """Draw the top and bottom pipes."""
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom))

    def off_screen(self):
        """Check if the pipe has moved off-screen."""
        return self.x < -self.width

    def collide(self, bird):
        """Check if the bird collides with the pipes."""
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)