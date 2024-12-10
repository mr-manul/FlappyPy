import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Scattered Clouds")

COLORS = {
    "background": (112, 197, 206),  # Light blue
}

# Load cloud image
cloud_image = pygame.image.load("cloud.png").convert_alpha()
cloud_image.set_alpha(200)  # Set transparency (0 to 255)
# Scale cloud image function
def scale_cloud(image, size):
    return pygame.transform.scale(image, (size, size))

# Generate random clouds
def generate_clouds(num_clouds):
    clouds = []
    for _ in range(num_clouds):
        x = random.randint(0, WIDTH)         # Random x position
        y = random.randint(0, HEIGHT // 2)   # Random y position (top half of screen)
        size = random.randint(40, 100)       # Random size (width and height)
        cloud = {
            "image": scale_cloud(cloud_image, size),
            "x": x,
            "y": y,
            "size": size
        }
        clouds.append(cloud)
    return clouds

#scattered clouds
def draw_clouds(screen, clouds):
    for cloud in clouds:
        screen.blit(cloud["image"], (cloud["x"], cloud["y"]))

# Main function
def main():
    # Generate 10 scattered clouds
    clouds = generate_clouds(10)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw background
        screen.fill(COLORS["background"])

        # Draw clouds
        draw_clouds(screen, clouds)

        # Update display
        pygame.display.flip()
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    main()