import pygame
from settings import *
from .plant import Plant
from .bullet import Bullet

class Peashooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = PEASHOOTER_COST
        self.health = 100
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 2000  # Shoot every 2 seconds
        
        # Draw pixel art peashooter
        # Stem
        stem_color = (0, 150, 0)
        stem_rect = pygame.Rect(
            self.image.get_width() // 4,
            self.image.get_height() // 3,
            self.image.get_width() // 4,
            self.image.get_height() // 3
        )
        pygame.draw.rect(self.image, stem_color, stem_rect)
        
        # Head (shooting part)
        head_color = (0, 200, 0)
        head_rect = pygame.Rect(
            self.image.get_width() // 2,
            self.image.get_height() // 3,
            self.image.get_width() // 3,
            self.image.get_height() // 3
        )
        pygame.draw.rect(self.image, head_color, head_rect)
        
        # Pixel details
        # Stem highlight
        highlight_color = (0, 180, 0)
        pygame.draw.rect(self.image, highlight_color, (
            stem_rect.left + 2,
            stem_rect.top + 2,
            4, 4
        ))
        
        # Head highlight
        pygame.draw.rect(self.image, (0, 230, 0), (
            head_rect.left + 2,
            head_rect.top + 2,
            4, 4
        ))
        
        # Barrel opening
        pygame.draw.rect(self.image, (0, 100, 0), (
            head_rect.right - 8,
            head_rect.centery - 4,
            8, 8
        ))
        
    def update(self, game):
        # Check if there are any zombies in this row
        for zombie in game.zombies:
            if abs(zombie.rect.centery - self.rect.centery) < GRID_SIZE // 2:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shoot_delay:
                    self.shoot(game)
                    self.last_shot_time = current_time
                break
            
    def shoot(self, game):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        game.bullets.add(bullet)
        game.all_sprites.add(bullet)
        game.sound_manager.play_sound('shoot')
        self.last_shot_time = pygame.time.get_ticks()
