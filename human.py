import pygame
import random
import math
import os

class Human:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'human.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.angle = random.uniform(0, 2 * math.pi)
        self.move_counter = 0
        self.original_image = self.image
        self.fleeing = False
        self.flee_timer = 0

    def move(self, snakes=None):
        if snakes:
            # Find the nearest snake
            nearest_snake = min(snakes, key=lambda s: math.sqrt(
                (s.rect.centerx - self.rect.centerx) ** 2 + 
                (s.rect.centery - self.rect.centery) ** 2
            ), default=None)
            
            if nearest_snake:
                # Calculate distance to nearest snake
                distance = math.sqrt(
                    (nearest_snake.rect.centerx - self.rect.centerx) ** 2 + 
                    (nearest_snake.rect.centery - self.rect.centery) ** 2
                )
                
                # If snake is close, flee from it
                if distance < 200:  # Flee if snake is within 200 pixels
                    self.fleeing = True
                    self.flee_timer = 60  # Flee for 60 frames
                    # Calculate angle away from snake
                    self.angle = math.atan2(
                        self.rect.centery - nearest_snake.rect.centery,
                        self.rect.centerx - nearest_snake.rect.centerx
                    )
        
        if self.flee_timer > 0:
            self.flee_timer -= 1
            speed = self.speed * 1.5  # Move faster while fleeing
        else:
            self.fleeing = False
            speed = self.speed
            # Change direction randomly when not fleeing
            self.move_counter += 1
            if self.move_counter >= 60:
                self.move_counter = 0
                self.angle = random.uniform(0, 2 * math.pi)

        # Move in the current direction
        dx = math.cos(self.angle) * speed
        dy = math.sin(self.angle) * speed
        
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        # Bounce off screen edges
        screen = pygame.display.get_surface()
        if new_x < 0 or new_x > screen.get_width() - self.rect.width:
            self.angle = math.pi - self.angle
            dx = -dx
        if new_y < 0 or new_y > screen.get_height() - self.rect.height:
            self.angle = -self.angle
            dy = -dy
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Rotate image to face movement direction
        angle_degrees = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.original_image, -angle_degrees)
        
        # Keep the same center after rotation
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.fleeing:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)