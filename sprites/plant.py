import pygame
from settings import *

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE-10, GRID_SIZE-10))
        self.image.fill((50, 120, 50))  # Dark green base
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.health = 100
        self.max_health = 100
        self.cost = 0
        
        # Draw basic plant shape (pot)
        pot_color = (139, 69, 19)  # Brown
        pot_rect = pygame.Rect(
            5,
            self.image.get_height() * 2 // 3,
            self.image.get_width() - 10,
            self.image.get_height() // 3
        )
        pygame.draw.rect(self.image, pot_color, pot_rect)
        
        # Add pixel-style highlights to pot
        highlight_color = (160, 82, 45)
        pygame.draw.rect(self.image, highlight_color, (
            pot_rect.left + 2,
            pot_rect.top + 2,
            4,
            4
        ))
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            
    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            bar_width = 40
            bar_height = 5
            pos_x = self.rect.x + (self.rect.width - bar_width) // 2
            pos_y = self.rect.y - 10
            
            # Background (red)
            pygame.draw.rect(surface, RED, (pos_x, pos_y, bar_width, bar_height))
            # Health (green)
            health_width = int(bar_width * (self.health / self.max_health))
            if health_width > 0:
                pygame.draw.rect(surface, GREEN, (pos_x, pos_y, health_width, bar_height))
            
    def update(self):
        pass  # To be implemented by child classes
