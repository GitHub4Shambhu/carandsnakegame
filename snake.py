import pygame
import random
import os
import math

class Snake:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'snake.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.angle = 0
        self.original_image = self.image

    def move_towards(self, target_x, target_y):
        # Calculate direction vector
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Normalize the direction vector and apply speed
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            # Update position
            self.rect.x += dx
            self.rect.y += dy
            
            # Calculate angle for rotation
            self.angle = math.degrees(math.atan2(-dy, dx))
            
            # Rotate the image
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Keep the same center after rotation
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        # Keep snake within screen bounds
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def set_speed(self, difficulty):
        if difficulty == 'easy':
            self.speed = 2
        elif difficulty == 'medium':
            self.speed = 3
        elif difficulty == 'hard':
            self.speed = 4

    def draw(self, screen):
        screen.blit(self.image, self.rect)