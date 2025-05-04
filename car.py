import pygame
import os

class Car:
    def __init__(self, x, y):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, 'car.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.base_speed = 5
        self.speed = self.base_speed
        self.health = 100
        self.shield = False
        self.speed_boost_timer = 0
        self.shield_timer = 0

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
        
        # Update power-up timers
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = self.base_speed
                
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False

    def apply_powerup(self, power_type):
        if power_type == 'speed':
            self.speed = self.base_speed * 1.5
            self.speed_boost_timer = 180  # 6 seconds at 30 FPS
        elif power_type == 'shield':
            self.shield = True
            self.shield_timer = 300  # 10 seconds at 30 FPS
        elif power_type == 'health':
            self.health = min(100, self.health + 30)

    def take_damage(self, amount):
        if not self.shield:
            self.health -= amount
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Draw health bar
        health_bar_width = 50
        health_width = (self.health / 100) * health_bar_width
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))
        
        # Draw shield effect
        if self.shield:
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)