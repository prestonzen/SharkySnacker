import pygame
import sys
from random import randint

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sharky Snacker')
clock = pygame.time.Clock()

# Load images
pelmeni_image = pygame.image.load('assets/pelmeniSingle-70x70p.png')
sharky_image = pygame.image.load('assets/Sharky-485x280p.png')

# Scale images to fit the grid size
pelmeni_image = pygame.transform.scale(pelmeni_image, (CELL_SIZE, CELL_SIZE))
sharky_image = pygame.transform.scale(sharky_image, (CELL_SIZE, CELL_SIZE))

# Game grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Place pelmeni
for _ in range(100):  # Adjust number of pelmeni as needed
    x, y = randint(1, GRID_WIDTH - 2), randint(1, GRID_HEIGHT - 2)
    grid[y][x] = 1  # 1 represents a pelmeni

# Shark position
shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Shark movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and shark_x > 0:
        shark_x -= 1
    if keys[pygame.K_RIGHT] and shark_x < GRID_WIDTH - 1:
        shark_x += 1
    if keys[pygame.K_UP] and shark_y > 0:
        shark_y -= 1
    if keys[pygame.K_DOWN] and shark_y < GRID_HEIGHT - 1:
        shark_y += 1

    # Collision with pelmeni
    if grid[shark_y][shark_x] == 1:
        grid[shark_y][shark_x] = 0
        # Increase score, etc.

    # Drawing the grid
    screen.fill((0, 0, 0))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                screen.blit(pelmeni_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Draw the shark
    screen.blit(sharky_image, (shark_x * CELL_SIZE, shark_y * CELL_SIZE))

    # Update display
    pygame.display.update()
    clock.tick(15)

pygame.quit()
sys.exit()
