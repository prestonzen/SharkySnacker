import pygame
import sys
from random import randint, choice

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
FONT_SIZE = 24
LIVES = 3
SCORE = 0
ENEMY_SPEED = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sharky Snacker')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Load images
pelmeni_image = pygame.image.load('assets/pelmeniSingle-70x70p.png').convert_alpha()
sharky_image = pygame.image.load('assets/Sharky-485x280p.png').convert_alpha()
enemy_image = pygame.image.load('assets/MilaSnape.png').convert_alpha()
heart_image = pygame.image.load('assets/heart.png').convert_alpha()  # Load the heart image

# Scale images to fit the grid size
pelmeni_image = pygame.transform.scale(pelmeni_image, (CELL_SIZE, CELL_SIZE))
sharky_image = pygame.transform.scale(sharky_image, (CELL_SIZE, CELL_SIZE))
enemy_image = pygame.transform.scale(enemy_image, (CELL_SIZE, CELL_SIZE))
heart_image = pygame.transform.scale(heart_image, (CELL_SIZE, CELL_SIZE))  # Scale the heart image

# Load sound effects and music
pygame.mixer.music.load('assets/happy-happy-happy-song.mp3')
pygame.mixer.music.play(-1)
death_sound = pygame.mixer.Sound('assets/roblox_OOF.mp3')
eating_sound = pygame.mixer.Sound('assets/slurp.mp3')

# Game grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Place pelmeni
for _ in range(100):
    x, y = randint(1, GRID_WIDTH - 2), randint(1, GRID_HEIGHT - 2)
    grid[y][x] = 1

# Shark and enemy positions
shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
enemy_x, enemy_y = randint(1, GRID_WIDTH - 2), randint(1, GRID_HEIGHT - 2)

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

    # Enemy movement
    enemy_x += choice([-ENEMY_SPEED, 0, ENEMY_SPEED])
    enemy_y += choice([-ENEMY_SPEED, 0, ENEMY_SPEED])
    enemy_x = max(0, min(GRID_WIDTH - 1, enemy_x))
    enemy_y = max(0, min(GRID_HEIGHT - 1, enemy_y))

    # Collision with pelmeni
    if grid[shark_y][shark_x] == 1:
        grid[shark_y][shark_x] = 0
        eating_sound.play()
        SCORE += 10  # Update score

    # Collision with enemy
    if shark_x == enemy_x and shark_y == enemy_y:
        death_sound.play()
        LIVES -= 1
        shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2  # Reset shark position
        if LIVES == 0:
            running = False  # Game over

    # Drawing the grid
    screen.fill((0, 0, 0))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                screen.blit(pelmeni_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Draw the shark
    screen.blit(sharky_image, (shark_x * CELL_SIZE, shark_y * CELL_SIZE))

    # Draw the enemy
    screen.blit(enemy_image, (enemy_x * CELL_SIZE, enemy_y * CELL_SIZE))

    # Draw the score
    score_text = font.render(f'Score: {SCORE}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw the lives
    for i in range(LIVES):
        heart_x = SCREEN_WIDTH - (i + 1) * (heart_image.get_width() + 10)
        screen.blit(heart_image, (heart_x, 10))

    # Update display
    pygame.display.update()
    clock.tick(15)  # Frame rate

pygame.quit()
sys.exit()

