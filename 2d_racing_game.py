import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2D Racing Game')

# Function to load and resize images
def load_and_resize_image(image_path, width, height):
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

# Load and resize images (adjust width and height as needed)
player_car_image = load_and_resize_image(os.path.join('images', 'player_car.png'), 80, 160)
opponent_car_image = load_and_resize_image(os.path.join('images', 'opponent_car.png'), 80, 160)

# Load background image (assuming it fills the entire screen)
background_image = load_and_resize_image(os.path.join('images', 'background.png'), screen_width, screen_height)

# Load road animation frames and resize if necessary
road_frames = [
    load_and_resize_image(os.path.join('images', f'road_{i}.png'), screen_width, screen_height)
    for i in range(1, 5)  # Assuming there are 4 frames of animation
]

car_width = player_car_image.get_width()
car_height = player_car_image.get_height()

# Setup player car and opponent cars
player_car = pygame.Rect(screen_width // 2 - car_width // 2, screen_height - car_height - 10, car_width, car_height)
opponent_cars = [
    pygame.Rect(random.randint(0, screen_width - car_width), -car_height - random.randint(0, 300), car_width, car_height),
    pygame.Rect(random.randint(0, screen_width - car_width), -car_height * 5 - random.randint(0, 300), car_width, car_height)
]

opponent_speeds = [5, 7]
player_speed = 5
road_speed = 5

# Function to display text
def display_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
clock = pygame.time.Clock()
running = True
score = 0
high_score = 0
game_over = False

# Road position settings
road_y = 0

# Road animation variables
current_road_frame = 0
road_animation_speed = 10  # Animation speed, higher values slow down the animation

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.left > 0:
        player_car.x -= player_speed
    if keys[pygame.K_RIGHT] and player_car.right < screen_width:
        player_car.x += player_speed

    if not game_over:
        for i in range(len(opponent_cars)):
            opponent_cars[i].y += opponent_speeds[i]
            if opponent_cars[i].top > screen_height:
                opponent_cars[i].y = -car_height
                opponent_cars[i].x = random.randint(0, screen_width - car_width)
                score += 1
                if score > high_score:
                    high_score = score

                # Increase the speed of opponents and road
                opponent_speeds[i] += 0.1
                road_speed += 0.01

            if player_car.colliderect(opponent_cars[i]):
                game_over = True

        road_y += road_speed
        if road_y >= screen_height:
            road_y = 0

        # Update road animation frame only when the game is not over
        current_road_frame = (current_road_frame + 1) % (len(road_frames) * road_animation_speed)
        road_image = road_frames[current_road_frame // road_animation_speed]
    else:
        # Draw the current road frame without updating when the game is over
        road_image = road_frames[current_road_frame // road_animation_speed]

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw road
    screen.blit(road_image, (0, road_y))
    screen.blit(road_image, (0, road_y - screen_height))

    screen.blit(player_car_image, player_car.topleft)
    for car in opponent_cars:
        screen.blit(opponent_car_image, car.topleft)

    display_text(f'Score: {score}', 30, (255, 255, 255), 10, 10)
    display_text(f'High Score: {high_score}', 30, (255, 255, 255), 10, 50)

    if game_over:
        display_text('Game Over', 50, (255, 255, 255), screen_width // 2 - 100, screen_height // 2 - 50)
        display_text('Press R to Restart', 30, (255, 255, 255), screen_width // 2 - 100, screen_height // 2)

    pygame.display.flip()
    clock.tick(60)

    if game_over and keys[pygame.K_r]:
        player_car.x = screen_width // 2 - car_width // 2
        opponent_cars = [
            pygame.Rect(random.randint(0, screen_width - car_width), -car_height, car_width, car_height),
            pygame.Rect(random.randint(0, screen_width - car_width), -car_height * 5, car_width, car_height)
        ]
        score = 0
        road_speed = 5
        opponent_speeds = [5, 7]
        game_over = False

pygame.quit()
