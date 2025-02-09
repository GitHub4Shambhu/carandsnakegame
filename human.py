import pygame
import random
import math
import os

class Human:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'human.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        print(f'Human initialized at {self.rect.topleft}')  # Debug print
        
        # Add random movement
        self.speed = 2
        self.angle = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.move_counter = 0

    def move(self):
        # Change direction randomly every 60 frames
        self.move_counter += 1
        if self.move_counter >= 60:
            self.move_counter = 0
            self.angle = random.uniform(0, 2 * math.pi)

        # Move in the current direction using trigonometry
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        
        self.rect.x += dx
        self.rect.y += dy

        # Keep human within screen bounds and bounce off edges
        if self.rect.left < 0:
            self.rect.left = 0
            self.angle = math.pi - self.angle
        elif self.rect.right > 800:
            self.rect.right = 800
            self.angle = math.pi - self.angle
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.angle = -self.angle
        elif self.rect.bottom > 600:
            self.rect.bottom = 600
            self.angle = -self.angle

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        print(f'Drawing human at {self.rect.topleft}')  # Debug print