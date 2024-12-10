import pygame
import random

# Constants
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
PIPE_WIDTH = 60
PIPE_GAP = 200
PIPE_SPEED = 3

class Pipe:
    def __init__(self, x, gap_height, pipe_speed):
        self.x = x
        self.gap_height = gap_height
        self.top = self.gap_height
        self.bottom = self.gap_height + PIPE_GAP
        self.width = PIPE_WIDTH
        self.pipe_speed = pipe_speed
        self.vertical_speed = 2
        self.vertical_direction = 1  # 1 means down, -1 means up
        self.vertical_movement_enabled = False
        self.pipe_top_image = pygame.image.load("pipe_top.png").convert_alpha()
        self.pipe_bottom_image = pygame.image.load("pipe_bottom.png").convert_alpha()
        self.pipe_top_image = pygame.transform.flip(self.pipe_top_image, False, True)
        self.pipe_top_image = pygame.transform.scale(self.pipe_top_image, (PIPE_WIDTH, SCREEN_HEIGHT))
        self.pipe_bottom_image = pygame.transform.scale(self.pipe_bottom_image, (PIPE_WIDTH, SCREEN_HEIGHT))

    def update(self, move_vertically=False):
        """Move the pipe to the left and optionally move vertically."""
        self.x -= self.pipe_speed

        if move_vertically:
            # Move the pipes up and down
            self.top += self.vertical_speed * self.vertical_direction
            self.bottom = self.top + PIPE_GAP

            # Reverse direction if the pipe hits the screen boundaries
            if self.top <= 50 or self.bottom >= SCREEN_HEIGHT - 50:  # Keep some space from edges
                self.vertical_direction *= -1

    def draw(self, screen):
        """Draw the top and bottom pipes."""
        # Top pipe
        top_pipe_flipped = pygame.transform.flip(self.pipe_top_image, False, True)  # Flip vertically
        top_pipe_rect = top_pipe_flipped.get_rect(midbottom=(self.x + PIPE_WIDTH // 2, self.top))
        screen.blit(top_pipe_flipped, top_pipe_rect)

        # Bottom pipe
        bottom_pipe_rect = self.pipe_bottom_image.get_rect(midtop=(self.x + PIPE_WIDTH // 2, self.bottom))
        screen.blit(self.pipe_bottom_image, bottom_pipe_rect)

    def off_screen(self):
        """Check if the pipe has moved off-screen."""
        return self.x < -self.width

    def collide(self, bird):
        """Check if the bird collides with the pipes."""
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
    
    def reset_vertical_movement(self):
        """Reset vertical movement to its initial state."""
        self.vertical_movement_enabled = False
        self.gap_height = random.randint(100, SCREEN_HEIGHT - 250)
        self.top = self.gap_height
        self.bottom = self.gap_height + PIPE_GAP