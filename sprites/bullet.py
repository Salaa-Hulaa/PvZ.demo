import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 12))
        self.image.set_colorkey(BLACK)  # Make black background transparent
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE
        
        # Draw pixel art pea
        pea_color = (0, 255, 0)  # Bright green
        pygame.draw.rect(self.image, pea_color, (2, 2, 8, 8))
        
        # Add highlights
        highlight_color = (150, 255, 150)
        pygame.draw.rect(self.image, highlight_color, (2, 2, 3, 3))
        
        # Add shadow
        shadow_color = (0, 200, 0)
        pygame.draw.rect(self.image, shadow_color, (7, 7, 3, 3))
        
    def update(self, game):
        self.rect.x += self.speed
        
        # Check for collisions with zombies
        for zombie in game.zombies:
            if self.rect.colliderect(zombie.rect):
                zombie.take_damage(self.damage)
                game.sound_manager.play_sound('zombie_hit')
                self.kill()
                break
        
        # Remove if off screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
