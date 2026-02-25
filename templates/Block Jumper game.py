import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_SIZE = 50
PLAYER_SPEED = 5
GRAVITY = 0.5
SPIKE_WIDTH = 30
SPIKE_HEIGHT = 50
SPIKE_SPEED = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game with Pygame")

# Player variables
player_x = 100
player_y = HEIGHT - PLAYER_SIZE
player_velocity = 0
jumping = False

# Spikes variables
spike_x = WIDTH
spike_y = HEIGHT - SPIKE_HEIGHT

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping and not game_over:
                player_velocity = -10  # Jump
                jumping = True

    # Apply gravity
    player_velocity += GRAVITY

    # Update player position
    player_y += player_velocity

    # Ground collision
    if player_y >= HEIGHT - PLAYER_SIZE:
        player_y = HEIGHT - PLAYER_SIZE
        jumping = False

    # Update spike position
    spike_x -= SPIKE_SPEED

    # Check for collision with the spike
    if spike_x < player_x + PLAYER_SIZE and spike_x + SPIKE_WIDTH > player_x and player_y + PLAYER_SIZE > spike_y:
        game_over = True

    # If the spike goes off the screen, reset it
    if spike_x + SPIKE_WIDTH < 0:
        spike_x = WIDTH
        spike_y = HEIGHT - SPIKE_HEIGHT

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Draw the spike
    pygame.draw.rect(screen, RED, (spike_x, spike_y, SPIKE_WIDTH, SPIKE_HEIGHT))

    pygame.display.update()

    # Game over condition
    if game_over:
        pygame.time.delay(1000)  # Pause for a moment before exiting
        running = False

    clock.tick(30)  # Limit the frame rate to 30 FPS

pygame.quit()
sys.exit()