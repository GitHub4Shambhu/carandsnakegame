import pygame
import random
import os
import math

class PowerUp:
    def __init__(self, x, y, power_type):
        self.power_type = power_type  # 'speed', 'shield', 'health'
        self.rect = pygame.Rect(x, y, 30, 30)
        self.active = True
        self.colors = {
            'speed': (255, 255, 0),   # Yellow
            'shield': (0, 0, 255),    # Blue
            'health': (0, 255, 0)     # Green
        }
        self.icons = {
            'speed': '⚡',
            'shield': '🛡️',
            'health': '❤️'
        }
        # Animation variables
        self.angle = 0
        self.pulse_size = 0
        self.pulse_direction = 1
        self.creation_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        if not self.active:
            return
            
        # Rotate and pulse animation
        self.angle = (self.angle + 2) % 360
        self.pulse_size += 0.1 * self.pulse_direction
        if self.pulse_size > 5:
            self.pulse_direction = -1
        elif self.pulse_size < 0:
            self.pulse_direction = 1
            
        # Draw the base powerup
        color = self.colors[self.power_type]
        rotated_rect = self.rect.copy()
        
        # Adjust size based on pulse
        pulse_offset = int(self.pulse_size)
        expanded_rect = pygame.Rect(
            rotated_rect.x - pulse_offset,
            rotated_rect.y - pulse_offset,
            rotated_rect.width + pulse_offset * 2,
            rotated_rect.height + pulse_offset * 2
        )
        
        # Draw the powerup with glow effect
        for i in range(3):
            alpha = 150 - i * 40
            size_offset = i * 4
            glow_rect = pygame.Rect(
                rotated_rect.x - size_offset,
                rotated_rect.y - size_offset,
                rotated_rect.width + size_offset * 2,
                rotated_rect.height + size_offset * 2
            )
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            
            # Create a color with alpha
            r, g, b = color
            glow_color = (r, g, b, alpha)
            pygame.draw.rect(glow_surf, glow_color, 
                           pygame.Rect(0, 0, glow_rect.width, glow_rect.height), 
                           border_radius=10)
            
            # Rotate the glow
            if i == 0:  # Only rotate the inner shape
                glow_surf = pygame.transform.rotate(glow_surf, self.angle)
                glow_rect = glow_surf.get_rect(center=rotated_rect.center)
                
            screen.blit(glow_surf, glow_rect)
        
        # Draw the inner shape (diamond for speed, circle for shield, etc.)
        inner_surf = pygame.Surface((rotated_rect.width - 10, rotated_rect.height - 10), pygame.SRCALPHA)
        
        if self.power_type == 'speed':
            # Draw a diamond/lightning shape
            points = [
                (inner_surf.get_width() // 2, 0),                      # Top
                (inner_surf.get_width(), inner_surf.get_height() // 2), # Right
                (inner_surf.get_width() // 2, inner_surf.get_height()),  # Bottom
                (0, inner_surf.get_height() // 2)                      # Left
            ]
            pygame.draw.polygon(inner_surf, (255, 255, 255), points)
        elif self.power_type == 'shield':
            # Draw a shield/circle shape
            pygame.draw.circle(inner_surf, (255, 255, 255), 
                             (inner_surf.get_width() // 2, inner_surf.get_height() // 2), 
                             inner_surf.get_width() // 2)
        elif self.power_type == 'health':
            # Draw a heart/plus shape
            cross_width = 6
            # Horizontal bar
            pygame.draw.rect(inner_surf, (255, 255, 255), 
                           pygame.Rect(0, (inner_surf.get_height() - cross_width) // 2, 
                                     inner_surf.get_width(), cross_width))
            # Vertical bar
            pygame.draw.rect(inner_surf, (255, 255, 255), 
                           pygame.Rect((inner_surf.get_width() - cross_width) // 2, 0, 
                                     cross_width, inner_surf.get_height()))
        
        # Center the inner shape in the powerup
        inner_rect = inner_surf.get_rect(center=rotated_rect.center)
        screen.blit(inner_surf, inner_rect)
        
    @staticmethod
    def spawn_random(screen_width, screen_height):
        # Avoid spawning too close to the edges
        margin = 50
        x = random.randint(margin, screen_width - margin)
        y = random.randint(margin, screen_height - margin)
        power_type = random.choice(['speed', 'shield', 'health'])
        return PowerUp(x, y, power_type)