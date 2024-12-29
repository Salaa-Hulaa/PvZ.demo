import pygame
import random
import math
from settings import *
from sprites.sunflower import Sunflower
from sprites.peashooter import Peashooter
from sprites.wallnut import WallNut
from sprites.zombie import Zombie
from sprites.sun import Sun
from sound_manager import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plants vs. Zombies")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.suns = pygame.sprite.Group()
        
        # Game state
        self.sun_amount = INITIAL_SUN
        self.selected_plant = None
        self.wave_number = 0
        self.zombies_spawned = 0
        self.last_zombie_spawn = 0
        self.wave_start_time = 0
        self.game_start_time = 0
        self.last_sun_drop = 0
        
        # Plant types
        self.plant_types = {
            'sunflower': {'class': Sunflower, 'cost': SUNFLOWER_COST},
            'peashooter': {'class': Peashooter, 'cost': PEASHOOTER_COST},
            'wallnut': {'class': WallNut, 'cost': WALLNUT_COST}
        }
        
        # 初始化音效管理器
        self.sound_manager = SoundManager()
        self.sound_manager.play_music('background.wav')
        
    def start_game(self):
        # Reset game state
        self.state = PLAYING
        self.sun_amount = INITIAL_SUN
        self.selected_plant = None
        self.wave_number = 0
        self.zombies_spawned = 0
        self.last_zombie_spawn = 0
        self.wave_start_time = 0
        self.game_start_time = pygame.time.get_ticks()
        self.last_sun_drop = 0
        
        # Clear all sprite groups
        self.all_sprites.empty()
        self.plants.empty()
        self.zombies.empty()
        self.bullets.empty()
        self.suns.empty()
        
        # Play background music
        self.sound_manager.play_music('background.wav')
        
    def spawn_zombie(self):
        if len(self.zombies) < MAX_ZOMBIES:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_zombie_spawn >= ZOMBIE_SPAWN_INTERVAL:
                # Randomly choose a row
                row = random.randint(0, GRID_ROWS - 1)
                grid_height = GRID_SIZE * GRID_ROWS
                grid_y_offset = GAME_AREA_TOP + (GAME_AREA_BOTTOM - GAME_AREA_TOP - grid_height) // 2
                y = grid_y_offset + row * GRID_SIZE + GRID_SIZE // 2
                
                # Create zombie at the right edge of the screen
                zombie_type = random.choice(ZOMBIE_TYPES)
                zombie = Zombie(SCREEN_WIDTH + 50, y, zombie_type)
                self.zombies.add(zombie)
                self.all_sprites.add(zombie)
                self.zombies_spawned += 1
                self.last_zombie_spawn = current_time
                
    def check_wave_completion(self):
        if self.state != PLAYING:
            return
            
        current_time = pygame.time.get_ticks()
        # Start first wave after initial delay
        if self.wave_number == 0 and current_time >= self.game_start_time + WAVE_INITIAL_DELAY:
            self.start_wave()
            
        # Check if current wave is complete
        elif self.wave_number > 0:
            if self.zombies_spawned >= WAVE_ZOMBIE_COUNT[self.wave_number - 1] and len(self.zombies) == 0:
                if self.wave_number >= len(WAVE_ZOMBIE_COUNT):
                    self.state = VICTORY
                else:
                    self.start_wave()
                    
    def start_wave(self):
        self.wave_number += 1
        self.zombies_spawned = 0
        self.wave_start_time = pygame.time.get_ticks()
        
    def update(self):
        if self.state == PLAYING:
            current_time = pygame.time.get_ticks()
            
            # Update all sprites
            for sprite in self.all_sprites:
                sprite.update(self)
            
            # Random sun drops
            if current_time - self.last_sun_drop >= NATURAL_SUN_INTERVAL:
                self.last_sun_drop = current_time
                self.spawn_random_sun()
            
            # Spawn zombies if in wave
            if self.wave_number > 0 and self.zombies_spawned < WAVE_ZOMBIE_COUNT[self.wave_number - 1]:
                self.spawn_zombie()
            
            # Check for game over
            if self.check_game_over():
                self.state = GAME_OVER
                self.sound_manager.play_sound('game_over')
                return
            
            # Check for victory
            if self.check_victory():
                self.state = VICTORY
                self.sound_manager.play_sound('victory')
                return
            
            # Check wave completion
            self.check_wave_completion()
            
            self.check_collisions()
            
    def check_collisions(self):
        # Bullets hitting zombies
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.zombies, False)
            if hits:
                bullet.kill()
                for zombie in hits:
                    zombie.take_damage(bullet.damage)
                    self.sound_manager.play_sound('zombie_hit')
                    
        # Zombies attacking plants
        for zombie in self.zombies:
            hits = pygame.sprite.spritecollide(zombie, self.plants, False)
            if hits:
                zombie.attacking = True
                zombie.attack(hits[0])
                self.sound_manager.play_sound('zombie_eat')
            else:
                zombie.attacking = False
                
    def draw_grid(self, mouse_pos):
        # Calculate grid area
        grid_height = GRID_SIZE * GRID_ROWS
        grid_y_offset = GAME_AREA_TOP + (GAME_AREA_BOTTOM - GAME_AREA_TOP - grid_height) // 2
        
        for x in range(GRID_COLS):
            for y in range(GRID_ROWS):
                rect = pygame.Rect(x * GRID_SIZE, 
                                 grid_y_offset + y * GRID_SIZE,
                                 GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)
                
                # Highlight grid cell under mouse if a plant is selected
                if self.selected_plant and rect.collidepoint(mouse_pos):
                    # Check if placement is valid
                    grid_x, grid_y = x, y
                    can_place = True
                    
                    # Check if space is empty
                    for plant in self.plants:
                        plant_grid_x = (plant.rect.centerx) // GRID_SIZE
                        plant_grid_y = (plant.rect.centery - grid_y_offset) // GRID_SIZE
                        if plant_grid_x == grid_x and plant_grid_y == grid_y:
                            can_place = False
                            break
                    
                    # Check if we can afford it
                    if self.plant_types[self.selected_plant]['cost'] > self.sun_amount:
                        can_place = False
                    
                    # Draw highlight
                    highlight_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    color = GRID_VALID if can_place else GRID_INVALID
                    pygame.draw.rect(highlight_surface, color, highlight_surface.get_rect())
                    self.screen.blit(highlight_surface, rect)
                    
    def draw_selection_info(self, mouse_pos):
        if not self.selected_plant:
            return
            
        # Create a small info panel that follows the cursor
        font = pygame.font.Font(None, 24)
        plant_info = self.plant_types[self.selected_plant]
        
        # Create text surfaces
        name_text = font.render(self.selected_plant.capitalize(), True, TEXT_COLOR)
        cost_text = font.render(f"Cost: {plant_info['cost']}", True, 
                              COST_COLOR if self.sun_amount >= plant_info['cost'] else WARNING_COLOR)
        
        # Calculate panel dimensions
        padding = 5
        panel_width = max(name_text.get_width(), cost_text.get_width()) + padding * 2
        panel_height = name_text.get_height() + cost_text.get_height() + padding * 3
        
        # Create panel surface with alpha
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL_BG_COLOR, panel.get_rect(),
                        border_radius=5)
        
        # Position text on panel
        name_rect = name_text.get_rect(centerx=panel_width//2, top=padding)
        cost_rect = cost_text.get_rect(centerx=panel_width//2, top=name_rect.bottom + padding)
        
        panel.blit(name_text, name_rect)
        panel.blit(cost_text, cost_rect)
        
        # Position panel near cursor but ensure it stays on screen
        panel_x = min(mouse_pos[0] + 20, SCREEN_WIDTH - panel_width)
        panel_y = min(mouse_pos[1] + 20, SCREEN_HEIGHT - panel_height)
        
        # Draw panel
        self.screen.blit(panel, (panel_x, panel_y))
        
    def draw_plant_selection(self):
        # Draw plant selection buttons
        y = GRID_ROWS * GRID_SIZE + 10
        for i, (plant_name, plant_info) in enumerate(self.plant_types.items()):
            button_rect = pygame.Rect(10 + i * (BUTTON_SIZE + BUTTON_MARGIN), y,
                                    BUTTON_SIZE, BUTTON_SIZE)
            
            # Button background
            if self.selected_plant == plant_name:
                color = BUTTON_SELECTED
            elif plant_info['cost'] > self.sun_amount:
                color = BUTTON_DISABLED
            else:
                color = BUTTON_HOVER if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_BACKGROUND
            
            # Draw button with border
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, TEXT_COLOR, button_rect, 2)  # Border
            
            # Plant preview
            if plant_name == 'peashooter':
                plant = plant_info['class'](0, 0, self.bullets, self.all_sprites)
            elif plant_name == 'sunflower':
                plant = plant_info['class'](0, 0, self.suns, self.all_sprites)
            else:
                plant = plant_info['class'](0, 0)
            preview_image = plant.image
            preview_rect = preview_image.get_rect(center=button_rect.center)
            self.screen.blit(preview_image, preview_rect)
            plant.kill()
            
            # Cost text with shadow
            font = pygame.font.Font(None, 24)
            cost_color = COST_COLOR if self.sun_amount >= plant_info['cost'] else WARNING_COLOR
            cost_text = font.render(str(plant_info['cost']), True, cost_color)
            cost_rect = cost_text.get_rect(bottom=button_rect.bottom - 2, centerx=button_rect.centerx)
            
            # Draw shadow then text
            shadow_text = font.render(str(plant_info['cost']), True, TEXT_SHADOW)
            shadow_rect = shadow_text.get_rect(bottom=cost_rect.bottom + 1, centerx=cost_rect.centerx + 1)
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(cost_text, cost_rect)
            
    def draw_game(self):
        # Draw background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw grid
        mouse_pos = pygame.mouse.get_pos()
        self.draw_grid(mouse_pos)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw health bars
        for plant in self.plants:
            plant.draw_health_bar(self.screen)
        for zombie in self.zombies:
            zombie.draw_health_bar(self.screen)
        
        # Draw selection info
        if self.selected_plant:
            self.draw_selection_info(mouse_pos)
        
        # Draw panels
        self.draw_top_panel()
        self.draw_bottom_panel()
        
    def draw_top_panel(self):
        # Create semi-transparent panel
        panel = pygame.Surface((SCREEN_WIDTH, TOP_BAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL_BG_COLOR, panel.get_rect(),
                        border_radius=PANEL_CORNER_RADIUS)
        
        # Draw sun counter with icon
        font = pygame.font.Font(None, 36)
        sun_text = font.render(f"{self.sun_amount}", True, COST_COLOR)
        sun_rect = sun_text.get_rect(left=PANEL_PADDING + 40, centery=TOP_BAR_HEIGHT//2)
        
        # Draw sun icon (simple yellow circle)
        sun_icon = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(sun_icon, YELLOW, (15, 15), 12)
        sun_icon_rect = sun_icon.get_rect(right=sun_rect.left - 5, centery=sun_rect.centery)
        
        # Draw wave info
        if self.wave_number > 0:
            wave_text = font.render(f"Wave {self.wave_number}", True, TEXT_COLOR)
            wave_rect = wave_text.get_rect(centerx=SCREEN_WIDTH//2, centery=TOP_BAR_HEIGHT//2)
            
            if self.wave_number <= len(WAVE_ZOMBIE_COUNT):
                zombies_left = WAVE_ZOMBIE_COUNT[self.wave_number - 1] - self.zombies_spawned
                zombies_text = font.render(f"Zombies: {zombies_left}", True, TEXT_COLOR)
                zombies_rect = zombies_text.get_rect(right=SCREEN_WIDTH-PANEL_PADDING,
                                                   centery=TOP_BAR_HEIGHT//2)
                panel.blit(zombies_text, zombies_rect)
            
            panel.blit(wave_text, wave_rect)
        else:
            ready_text = font.render("Get Ready!", True, TEXT_COLOR)
            ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH//2, TOP_BAR_HEIGHT//2))
            panel.blit(ready_text, ready_rect)
            
            time_left = (FIRST_WAVE_DELAY - (pygame.time.get_ticks() - self.game_start_time)) // 1000
            if time_left > 0:
                timer_text = font.render(str(time_left), True, WARNING_COLOR)
                timer_rect = timer_text.get_rect(left=ready_rect.right + 10,
                                               centery=TOP_BAR_HEIGHT//2)
                panel.blit(timer_text, timer_rect)
        
        panel.blit(sun_icon, sun_icon_rect)
        panel.blit(sun_text, sun_rect)
        self.screen.blit(panel, (0, 0))
        
    def draw_bottom_panel(self):
        # Create panel surface
        panel = pygame.Surface((SCREEN_WIDTH, BOTTOM_PANEL_HEIGHT))
        panel.fill(PANEL_BG_COLOR)
        
        # Calculate button positions
        y = (BOTTOM_PANEL_HEIGHT - BUTTON_SIZE) // 2
        
        # Draw plant buttons
        for i, (plant_name, plant_info) in enumerate(self.plant_types.items()):
            button_rect = pygame.Rect(PANEL_PADDING + i * (BUTTON_SIZE + BUTTON_MARGIN), y,
                                    BUTTON_SIZE, BUTTON_SIZE)
            
            # Button background with border radius
            if self.selected_plant == plant_name:
                color = BUTTON_SELECTED
            elif plant_info['cost'] > self.sun_amount:
                color = BUTTON_DISABLED
            else:
                color = BUTTON_HOVER if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_BACKGROUND
            
            pygame.draw.rect(panel, color, button_rect, border_radius=10)
            pygame.draw.rect(panel, TEXT_COLOR, button_rect, 2, border_radius=10)
            
            # Plant preview
            plant = plant_info['class'](0, 0)
            preview_image = plant.image
            preview_rect = preview_image.get_rect(center=button_rect.center)
            panel.blit(preview_image, preview_rect)
            plant.kill()
            
            # Cost text with shadow
            font = pygame.font.Font(None, 24)
            cost_color = COST_COLOR if self.sun_amount >= plant_info['cost'] else WARNING_COLOR
            cost_text = font.render(str(plant_info['cost']), True, cost_color)
            cost_rect = cost_text.get_rect(bottom=button_rect.bottom - 2,
                                         centerx=button_rect.centerx)
            
            shadow_text = font.render(str(plant_info['cost']), True, TEXT_SHADOW)
            shadow_rect = shadow_text.get_rect(bottom=cost_rect.bottom + 1,
                                             centerx=cost_rect.centerx + 1)
            panel.blit(shadow_text, shadow_rect)
            panel.blit(cost_text, cost_rect)
        
        self.screen.blit(panel, (0, SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT))
        
    def draw_game_info(self):
        # Draw sun counter
        font = pygame.font.Font(None, 36)
        sun_text = font.render(f"Sun: {self.sun_amount}", True, WHITE)
        self.screen.blit(sun_text, (10, 10))
        
        # Draw wave info
        if self.wave_number > 0:
            wave_text = font.render(f"Wave {self.wave_number}", True, WHITE)
            wave_rect = wave_text.get_rect(centerx=SCREEN_WIDTH//2, top=10)
            self.screen.blit(wave_text, wave_rect)
            
            # Draw zombies remaining
            if self.wave_number <= len(WAVE_ZOMBIE_COUNT):
                zombies_left = WAVE_ZOMBIE_COUNT[self.wave_number - 1] - self.zombies_spawned
                zombies_text = font.render(f"Zombies: {zombies_left}", True, WHITE)
                zombies_rect = zombies_text.get_rect(right=SCREEN_WIDTH-10, top=10)
                self.screen.blit(zombies_text, zombies_rect)
        else:
            # Draw "Get Ready" message
            ready_text = font.render("Get Ready!", True, WHITE)
            ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(ready_text, ready_rect)
            
            # Draw countdown
            time_left = (FIRST_WAVE_DELAY - (pygame.time.get_ticks() - self.game_start_time)) // 1000
            if time_left > 0:
                timer_text = font.render(str(time_left), True, WHITE)
                timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH//2, 90))
                self.screen.blit(timer_text, timer_rect)
        
    def draw_menu(self):
        # Fill background with a nice gradient
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw bouncing title
        title_font = pygame.font.Font(None, TITLE_SIZE)
        title_text = "Plants vs. Zombies"
        bounce_offset = math.sin(pygame.time.get_ticks() * 0.003) * TITLE_BOUNCE_HEIGHT
        title_surface = title_font.render(title_text, True, TITLE_COLOR)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH//2, centery=150 + bounce_offset)
        
        # Add shadow to title
        shadow_surface = title_font.render(title_text, True, (0, 50, 0))
        shadow_rect = shadow_surface.get_rect(centerx=title_rect.centerx + 4, 
                                            centery=title_rect.centery + 4)
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Draw menu items
        menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        mouse_pos = pygame.mouse.get_pos()
        
        for i, item in enumerate(MENU_ITEMS):
            item_y = MENU_START_Y + i * (MENU_FONT_SIZE + MENU_ITEM_SPACING)
            item_surface = menu_font.render(item, True, MENU_ITEM_COLOR)
            item_rect = item_surface.get_rect(centerx=SCREEN_WIDTH//2, centery=item_y)
            
            # Check if mouse is hovering over item
            if item_rect.collidepoint(mouse_pos):
                # Create larger version of text
                hover_surface = pygame.transform.scale(item_surface, 
                    (int(item_surface.get_width() * MENU_ITEM_GROW), 
                     int(item_surface.get_height() * MENU_ITEM_GROW)))
                hover_rect = hover_surface.get_rect(center=item_rect.center)
                
                # Draw shadow
                shadow_surface = pygame.transform.scale(
                    menu_font.render(item, True, (0, 50, 0)), 
                    (hover_surface.get_width(), hover_surface.get_height()))
                shadow_rect = shadow_surface.get_rect(centerx=hover_rect.centerx + 2,
                                                    centery=hover_rect.centery + 2)
                self.screen.blit(shadow_surface, shadow_rect)
                self.screen.blit(hover_surface, hover_rect)
            else:
                # Draw normal item with shadow
                shadow_surface = menu_font.render(item, True, (0, 50, 0))
                shadow_rect = shadow_surface.get_rect(centerx=item_rect.centerx + 2,
                                                    centery=item_rect.centery + 2)
                self.screen.blit(shadow_surface, shadow_rect)
                self.screen.blit(item_surface, item_rect)
                
    def handle_menu_click(self, pos):
        # Check if any menu item was clicked
        for i, item in enumerate(MENU_ITEMS):
            item_y = MENU_START_Y + i * (MENU_FONT_SIZE + MENU_ITEM_SPACING)
            item_rect = pygame.Rect(
                SCREEN_WIDTH//2 - 100,  # Approximate width
                item_y - MENU_FONT_SIZE//2,
                200,  # Approximate width
                MENU_FONT_SIZE
            )
            
            if item_rect.collidepoint(pos):
                self.sound_manager.play_sound('menu_click')
                if item == "Start Game":
                    self.start_game()
                elif item == "How to Play":
                    self.state = HELP
                elif item == "Quit":
                    self.running = False
                    
    def draw_help(self):
        # Fill background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_font = pygame.font.Font(None, TITLE_SIZE)
        title_text = "How to Play"
        title_surface = title_font.render(title_text, True, TITLE_COLOR)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH//2, centery=100)
        
        # Add shadow to title
        shadow_surface = title_font.render(title_text, True, (0, 50, 0))
        shadow_rect = shadow_surface.get_rect(centerx=title_rect.centerx + 4,
                                            centery=title_rect.centery + 4)
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Draw instructions
        instructions = [
            "Click on a plant in the bottom panel to select it",
            "Click on the grid to place the selected plant",
            "Sunflowers generate sun for purchasing plants",
            "Peashooters attack zombies",
            "Collect sun by clicking on it",
            "Defend your house from the zombies!",
            "",
            "Press any key to return to menu"
        ]
        
        font = pygame.font.Font(None, 32)
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, MENU_ITEM_COLOR)
            text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH//2,
                                            centery=200 + i * 40)
            # Draw shadow
            shadow_surface = font.render(line, True, (0, 50, 0))
            shadow_rect = shadow_surface.get_rect(centerx=text_rect.centerx + 2,
                                                centery=text_rect.centery + 2)
            self.screen.blit(shadow_surface, shadow_rect)
            self.screen.blit(text_surface, text_rect)
            
    def draw(self):
        self.screen.fill(LAWN_COLOR)
        
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == VICTORY:
            self.draw_game()
            self.draw_victory()
        elif self.state == HELP:
            self.draw_help()
            
        pygame.display.flip()
        
    def handle_click(self, pos):
        if self.state != PLAYING:
            return
            
        x, y = pos
        
        # Check for sun collection first
        for sun in self.suns:
            if sun.rect.collidepoint(pos):
                self.sun_amount += sun.collect()
                self.sound_manager.play_sound('collect_sun')
                return
        
        # Check if click is in plant selection area (bottom panel)
        if y > SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT:
            # Adjust y coordinate relative to panel
            panel_y = y - (SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT)
            button_y = (BOTTOM_PANEL_HEIGHT - BUTTON_SIZE) // 2
            
            # Check if y is in button row
            if button_y <= panel_y <= button_y + BUTTON_SIZE:
                # Check each button
                for i, (plant_name, plant_info) in enumerate(self.plant_types.items()):
                    button_x = PANEL_PADDING + i * (BUTTON_SIZE + BUTTON_MARGIN)
                    button_rect = pygame.Rect(button_x, button_y, BUTTON_SIZE, BUTTON_SIZE)
                    
                    # Adjust x coordinate relative to panel
                    if button_rect.collidepoint(x, panel_y):
                        if self.selected_plant == plant_name:
                            self.selected_plant = None
                        elif plant_info['cost'] <= self.sun_amount:
                            self.selected_plant = plant_name
                        return
            return
            
        # Calculate grid area
        grid_height = GRID_SIZE * GRID_ROWS
        grid_y_offset = GAME_AREA_TOP + (GAME_AREA_BOTTOM - GAME_AREA_TOP - grid_height) // 2
        
        # Adjust y coordinate for grid calculation
        grid_y = (y - grid_y_offset) // GRID_SIZE
        grid_x = x // GRID_SIZE
        
        # Check if click is in grid
        if (0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS and
            grid_y_offset <= y < grid_y_offset + grid_height):
            self.place_plant(grid_x, grid_y)
            
    def handle_plant_selection(self, x, y):
        button_y = GRID_ROWS * GRID_SIZE + 10
        if y < button_y or y > button_y + BUTTON_SIZE:
            return
            
        # Calculate which plant was clicked
        button_x = x - 10  # Subtract left margin
        if button_x < 0:
            return
            
        button_index = button_x // (BUTTON_SIZE + BUTTON_MARGIN)
        if button_index >= len(self.plant_types):
            return
            
        plant_name = list(self.plant_types.keys())[button_index]
        if self.plant_types[plant_name]['cost'] <= self.sun_amount:
            self.selected_plant = plant_name if self.selected_plant != plant_name else None
            
    def place_plant(self, grid_x, grid_y):
        if not self.selected_plant:
            return
            
        # Calculate grid area
        grid_height = GRID_SIZE * GRID_ROWS
        grid_y_offset = GAME_AREA_TOP + (GAME_AREA_BOTTOM - GAME_AREA_TOP - grid_height) // 2
        
        # Calculate plant position
        x = grid_x * GRID_SIZE + GRID_SIZE // 2
        y = grid_y_offset + grid_y * GRID_SIZE + GRID_SIZE // 2
        
        # Check if position is valid
        if not (0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS):
            return
            
        # Check if there's already a plant there
        for plant in self.plants:
            if plant.rect.collidepoint(x, y):
                return
                
        # Get plant info
        plant_info = self.plant_types[self.selected_plant]
        
        # Check if we can afford it
        if self.sun_amount < plant_info['cost']:
            return
            
        # Create the plant
        plant = plant_info['class'](x, y)
        
        # Add to sprite groups
        self.plants.add(plant)
        self.all_sprites.add(plant)
        
        # Deduct cost
        self.sun_amount -= plant_info['cost']
        
        # Play planting sound
        self.sound_manager.play_sound('plant')
        
        # Deselect plant
        self.selected_plant = None
        
    def spawn_random_sun(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        sun = Sun(x, -30)  # Start above the screen
        self.suns.add(sun)
        self.all_sprites.add(sun)
        
    def check_game_over(self):
        # Check if any zombie has reached the house (left side of screen)
        for zombie in self.zombies:
            if zombie.rect.right < GRID_SIZE:
                return True
        return False
        
    def check_victory(self):
        # Victory conditions:
        # 1. All waves completed
        # 2. No zombies left
        if self.wave_number >= len(WAVE_ZOMBIE_COUNT) and len(self.zombies) == 0:
            return True
        return False
        
    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        
        # Draw shadow
        shadow = font.render("Game Over!", True, (100, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 4, text_rect.centery + 4))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        
        # Draw restart instruction
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_victory(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw victory text
        font = pygame.font.Font(None, 72)
        text = font.render("Victory!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        
        # Draw shadow
        shadow = font.render("Victory!", True, (0, 100, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 4, text_rect.centery + 4))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        
        # Draw restart instruction
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.state == MENU:
                            self.handle_menu_click(event.pos)
                        elif self.state == PLAYING:
                            self.handle_click(event.pos)
                            
                elif event.type == pygame.KEYDOWN:
                    if self.state == HELP:
                        self.state = MENU
                    elif event.key == pygame.K_r and self.state in [GAME_OVER, VICTORY]:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        if self.state == PLAYING:
                            self.state = MENU
                        elif self.state == HELP:
                            self.state = MENU
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
        pygame.quit()
