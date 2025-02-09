import pygame
import random
import math
import os
from car import Car
from snake import Snake
from human import Human

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car and Snake Game")

# Set game icon
current_dir = os.path.dirname(os.path.abspath(__file__))
game_icon = pygame.image.load(os.path.join(current_dir, 'gamelogo.png'))
pygame.display.set_icon(game_icon)

# Game clock
clock = pygame.time.Clock()

# Create game objects
cars = [Car(random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100)) for _ in range(50)]
snakes = [Snake(random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100)) for _ in range(50)]
humans = [Human(random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100)) for _ in range(10)]

# Add movement angles for cars
car_angles = [random.uniform(0, 2 * math.pi) for _ in range(len(cars))]
car_move_counters = [0 for _ in range(len(cars))]

# Debug prints to verify initial positions
for i, car in enumerate(cars):
    print(f'Car {i} initial position: {car.rect.topleft}')
for i, human in enumerate(humans):
    print(f'Human {i} initial position: {human.rect.topleft}')

# Scores
car_score = 0
snake_score = 0

# Font for displaying scores
font = pygame.font.Font(None, 36)

# Selected car index (for controlling one car at a time)
selected_car_index = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Stop the game when 'S' key is pressed
                running = False
            elif event.key == pygame.K_TAB:  # Switch between cars
                selected_car_index = (selected_car_index + 1) % len(cars)
                print(f'Selected car {selected_car_index}')

    # Handle user input for the selected car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cars[selected_car_index].move(-1, 0)
    if keys[pygame.K_RIGHT]:
        cars[selected_car_index].move(1, 0)
    if keys[pygame.K_UP]:
        cars[selected_car_index].move(0, -1)
    if keys[pygame.K_DOWN]:
        cars[selected_car_index].move(0, 1)

    # Move all cars automatically except the selected one
    for i, car in enumerate(cars):
        if i != selected_car_index:
            # Change direction randomly every 120 frames
            car_move_counters[i] += 1
            if car_move_counters[i] >= 120:
                car_move_counters[i] = 0
                car_angles[i] = random.uniform(0, 2 * math.pi)

            # Move in the current direction
            dx = math.cos(car_angles[i])
            dy = math.sin(car_angles[i])
            car.move(dx, dy)

    # Move humans
    for human in humans:
        human.move()

    # Move the snakes towards the nearest human
    for snake in snakes:
        nearest_human = min(humans, key=lambda h: ((h.rect.x - snake.rect.x) ** 2 + (h.rect.y - snake.rect.y) ** 2))
        snake.move_towards(nearest_human.rect.x, nearest_human.rect.y)

    # Check for collisions
    for car in cars:
        for snake in snakes:
            if car.rect.colliderect(snake.rect):
                car_score += 1
                snake.rect.topleft = (random.randint(0, SCREEN_WIDTH - snake.rect.width), 
                                    random.randint(0, SCREEN_HEIGHT - snake.rect.height))
    
    for snake in snakes:
        for human in humans:
            if snake.rect.colliderect(human.rect):
                snake_score += 1
                snake.rect.topleft = (random.randint(0, SCREEN_WIDTH - snake.rect.width), 
                                    random.randint(0, SCREEN_HEIGHT - snake.rect.height))

    # Fill the screen with white color
    screen.fill(WHITE)

    # Draw the game objects
    for car in cars:
        car.draw(screen)
    for snake in snakes:
        snake.draw(screen)
    for human in humans:
        human.draw(screen)

    # Highlight the selected car
    pygame.draw.rect(screen, RED, cars[selected_car_index].rect, 2)

    # Display the scores
    car_score_text = font.render(f'Car Score: {car_score}', True, BLACK)
    snake_score_text = font.render(f'Snake Score: {snake_score}', True, BLACK)
    selected_car_text = font.render(f'Selected Car: {selected_car_index}', True, BLACK)
    screen.blit(car_score_text, (10, 10))
    screen.blit(snake_score_text, (10, 50))
    screen.blit(selected_car_text, (10, 90))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)  # Increased frame rate for smoother movement

# Quit Pygame
pygame.quit()