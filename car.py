import pygame
import os

class Car:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'car.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5  # Increase the speed of the car
        print(f'Car initialized at {self.rect.topleft}')  # Debug print

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Keep the car within screen bounds
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
        print(f'Car moved to {self.rect.topleft}')  # Debug print

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        print(f'Drawing car at {self.rect.topleft}')  # Debug print