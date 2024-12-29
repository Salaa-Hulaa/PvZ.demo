import pygame
from settings import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, zombie_type='normal'):
        super().__init__()
        self.type = zombie_type
        self.image = pygame.Surface((GRID_SIZE-20, GRID_SIZE-20))
        self.image.fill((128, 128, 128))  # Gray base color
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = float(x)  # For precise position tracking
        
        # Stats based on zombie type
        if self.type == 'cone':
            self.health = CONE_ZOMBIE_HEALTH
            self.speed = ZOMBIE_SPEED * 0.8  # Slightly slower
        else:  # normal zombie
            self.health = ZOMBIE_HEALTH
            self.speed = ZOMBIE_SPEED
            
        self.max_health = self.health
        self.damage = ZOMBIE_DAMAGE
        self.attacking = False
        self.last_attack_time = 0
        self.attack_delay = ZOMBIE_ATTACK_DELAY
        self.target = None
        
        # Draw pixel art zombie
        self.draw_zombie()
        
    def draw_zombie(self):
        # Body
        body_color = (100, 100, 100)  # Gray for zombie skin
        pygame.draw.rect(self.image, body_color, (
            10, 10,
            self.image.get_width() - 20,
            self.image.get_height() - 20
        ))
        
        # Head
        head_color = (120, 120, 120)
        head_rect = pygame.Rect(
            15, 5,
            30, 30
        )
        pygame.draw.rect(self.image, head_color, head_rect)
        
        # Eyes
        eye_color = (255, 0, 0)  # Red eyes
        pygame.draw.rect(self.image, eye_color, (20, 15, 5, 5))
        pygame.draw.rect(self.image, eye_color, (35, 15, 5, 5))
        
        # Cone hat for cone zombie
        if self.type == 'cone':
            cone_color = (200, 140, 0)  # Orange-brown
            points = [
                (30, 0),  # Top
                (15, 15),  # Bottom left
                (45, 15)   # Bottom right
            ]
            pygame.draw.polygon(self.image, cone_color, points)
        
    def update(self, game):
        if not self.attacking:
            self.x -= self.speed
            self.rect.x = int(self.x)
            
            # Check for collisions with plants
            for plant in game.plants:
                if self.rect.colliderect(plant.rect):
                    self.attacking = True
                    self.target = plant
                    game.sound_manager.play_sound('chomp')
                    break
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_delay:
                if self.target and self.target.alive():
                    self.target.health -= self.damage
                    if self.target.health <= 0:
                        self.target.kill()
                        self.attacking = False
                        self.target = None
                        game.sound_manager.play_sound('plant_death')
                    else:
                        game.sound_manager.play_sound('chomp')
                    self.last_attack_time = current_time
                else:
                    self.attacking = False
                    self.target = None
                    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            
    def attack(self, target):
        self.target = target
        
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
