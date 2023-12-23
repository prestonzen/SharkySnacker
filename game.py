import os
import sys
import pygame
from random import randint, choice

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
PELMENI_SEQUENCE = [1, 2, 3, 5, 8, 13, 21, 34]
ENEMY_SPEED = CELL_SIZE // 2

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sharky Snacker')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

# Load images using resource_path
pelmeni_image = pygame.image.load(resource_path('assets/pelmeniSingle-70x70p.png')).convert_alpha()
sharky_image_original = pygame.image.load(resource_path('assets/Sharky-485x280p.png')).convert_alpha()
enemy_image_original = pygame.image.load(resource_path('assets/MilaSnape.png')).convert_alpha()
heart_image = pygame.image.load(resource_path('assets/heart.png')).convert_alpha()
kaizen_logo = pygame.image.load(resource_path('assets/KaizenGaming2-750x750p.png')).convert_alpha()


# Scale images to fit the grid size
sharky_image = pygame.transform.scale(sharky_image_original, (CELL_SIZE, CELL_SIZE))
enemy_image = pygame.transform.scale(enemy_image_original, (CELL_SIZE * 4, CELL_SIZE * 3))  # Enemy is 3x larger
pelmeni_image = pygame.transform.scale(pelmeni_image, (CELL_SIZE, CELL_SIZE))
heart_image = pygame.transform.scale(heart_image, (CELL_SIZE, CELL_SIZE))
kaizen_logo = pygame.transform.scale(kaizen_logo, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Sharky images for each direction
sharky_image_left = sharky_image  # Original image is facing left
sharky_image_right = pygame.transform.flip(sharky_image_left, True, False)
sharky_image_up = pygame.transform.rotate(sharky_image_left, -90)
sharky_image_down = pygame.transform.rotate(sharky_image_left, 90)
sharky_current_image = sharky_image_left

# Sound effects
eating_sound = pygame.mixer.Sound(resource_path('assets/slurp.mp3'))
death_sound = pygame.mixer.Sound(resource_path('assets/roblox_OOF.mp3'))

# Start background music
pygame.mixer.music.load(resource_path('assets/happy-happy-happy-song.mp3'))
pygame.mixer.music.play(-1)

# Game variables
lives = 3
score = 0
level = 0
pelmeni_count = PELMENI_SEQUENCE[level]
enemy_direction = [choice([-1, 1]), choice([-1, 1])]
game_over = False

# Show splash screen
screen.fill((0, 0, 0))
screen.blit(kaizen_logo, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))
pygame.display.update()
pygame.time.wait(3000)  # Show splash screen for 3 seconds

# Function to place pelmeni and hearts
def place_items():
    grid = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    items = {'pelmeni': pelmeni_count, 'heart': 1}  # One heart per level
    positions = []

    while items['pelmeni'] > 0 or items['heart'] > 0:
        x, y = randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)
        if (x, y) not in positions:
            positions.append((x, y))
            if items['pelmeni'] > 0:
                grid[y][x] = 'pelmeni'
                items['pelmeni'] -= 1
            elif items['heart'] > 0:
                grid[y][x] = 'heart'
                items['heart'] -= 1
    return grid

# Initialize grid and place items
grid = place_items()

# Shark and enemy positions
shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
enemy_x, enemy_y = randint(0, SCREEN_WIDTH - CELL_SIZE * 4), randint(0, SCREEN_HEIGHT - CELL_SIZE * 4)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Reset game state for a new game
            game_over = False
            score = 0
            level = 0
            lives = 3
            pelmeni_count = PELMENI_SEQUENCE[level]
            grid = place_items()
            shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
            enemy_x, enemy_y = randint(0, SCREEN_WIDTH - CELL_SIZE * 4), randint(0, SCREEN_HEIGHT - CELL_SIZE * 4)
            pygame.mixer.music.play(-1)  # Restart music

    if not game_over:
        # Shark movement and direction logic
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = 1

        # Update Sharky's position and current image based on movement
        shark_x = max(0, min(GRID_WIDTH - 1, shark_x + move_x))
        shark_y = max(0, min(GRID_HEIGHT - 1, shark_y + move_y))
        if move_x == -1:
            sharky_current_image = sharky_image_left
        elif move_x == 1:
            sharky_current_image = sharky_image_right
        if move_y == -1:
            sharky_current_image = sharky_image_up
        elif move_y == 1:
            sharky_current_image = sharky_image_down

        # Enemy movement logic with wall bouncing
        enemy_x += enemy_direction[0] * ENEMY_SPEED
        enemy_y += enemy_direction[1] * ENEMY_SPEED
        if enemy_x <= 0 or enemy_x + CELL_SIZE * 4 >= SCREEN_WIDTH:
            enemy_direction[0] *= -1
        if enemy_y <= 0 or enemy_y + CELL_SIZE * 4 >= SCREEN_HEIGHT:
            enemy_direction[1] *= -1

        # Drawing the grid and items
        screen.fill((0, 0, 0))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 'pelmeni':
                    screen.blit(pelmeni_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif grid[y][x] == 'heart':
                    screen.blit(heart_image, (x * CELL_SIZE, y * CELL_SIZE))

        # Collision detection and scoring logic
        current_cell = grid[shark_y][shark_x]
        if current_cell == 'pelmeni':
            grid[shark_y][shark_x] = ''  # Clear the pelmeni from the grid
            eating_sound.play()
            score += 10  # Increment score
            pelmeni_count -= 1
        elif current_cell == 'heart':
            grid[shark_y][shark_x] = ''  # Clear the heart from the grid
            lives += 1  # Increment lives

        # Check if level is complete
        if pelmeni_count <= 0:
            level += 1
            if level < len(PELMENI_SEQUENCE):
                pelmeni_count = PELMENI_SEQUENCE[level]
                grid = place_items()  # Place new items for the next level
            else:
                game_over = True  # No more levels, end the game

        # Drawing Sharky, enemy, score, and lives
        screen.blit(sharky_current_image, (shark_x * CELL_SIZE, shark_y * CELL_SIZE))
        screen.blit(enemy_image, (enemy_x, enemy_y))

        # Draw the score
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draw the lives
        for i in range(lives):
            screen.blit(heart_image, (SCREEN_WIDTH - (i + 1) * (CELL_SIZE + 5), 10))

        # Check for collision with enemy
        if (enemy_x <= shark_x * CELL_SIZE <= enemy_x + CELL_SIZE * 4 and
            enemy_y <= shark_y * CELL_SIZE <= enemy_y + CELL_SIZE * 4):
            death_sound.play()
            lives -= 1
            shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2  # Reset Sharky position
            if lives <= 0:
                game_over = True

        # Update display and tick
        pygame.display.update()
        clock.tick(15)  # Frame rate

    else:
        # Game over screen
        screen.fill((0, 0, 0))
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        play_again_text = font.render('Press Space to Play Again', True, (255, 255, 255))
        screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))
        pygame.display.update()

        # Wait for space key to reset the game after game over
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_over = False
                    score = 0
                    level = 0
                    lives = 3
                    pelmeni_count = PELMENI_SEQUENCE[0]
                    grid = place_items()
                    shark_x, shark_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
                    enemy_x, enemy_y = randint(0, SCREEN_WIDTH - CELL_SIZE * 4), randint(0, SCREEN_HEIGHT - CELL_SIZE * 4)
                    pygame.mixer.music.play(-1)  # Restart music
                    break  # Break out of the inner loop to restart the game loop

# Clean up
pygame.quit()
sys.exit()
