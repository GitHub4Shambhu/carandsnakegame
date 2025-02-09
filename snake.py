import pygame
import random
import os

class Snake:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'snake.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image to 50x50 pixels
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2  # Adjust the speed of the snake
        print(f'Snake rect: {self.rect}')  # Debug print

    def move_towards(self, target_x, target_y):
        if self.rect.x < target_x:
            self.rect.x += self.speed
        elif self.rect.x > target_x:
            self.rect.x -= self.speed
        if self.rect.y < target_y:
            self.rect.y += self.speed
        elif self.rect.y > target_y:
            self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)