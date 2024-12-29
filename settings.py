import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Background Colors
BACKGROUND_COLOR = (87, 181, 58)  # Bright grass green
GRID_COLOR = (76, 158, 51)  # Slightly darker green for grid
MENU_BG_COLOR = (50, 120, 40)  # Dark green for menu

# UI Colors
PANEL_BG_COLOR = (60, 40, 20, 200)  # Semi-transparent brown
BUTTON_BACKGROUND = (101, 67, 33)  # Dark brown
BUTTON_HOVER = (139, 69, 19)  # Saddle brown
BUTTON_DISABLED = (80, 80, 80)  # Gray
BUTTON_SELECTED = (218, 165, 32)  # Golden rod

# Grid settings
GRID_HIGHLIGHT = (255, 255, 255, 30)  # Semi-transparent white
GRID_VALID = (100, 255, 100, 80)  # Semi-transparent green
GRID_INVALID = (255, 100, 100, 80)  # Semi-transparent red

# Text Colors
TEXT_COLOR = WHITE
TEXT_SHADOW = (0, 0, 0)
COST_COLOR = (255, 255, 150)  # Light yellow
WARNING_COLOR = (255, 100, 100)  # Light red
INFO_COLOR = (100, 255, 100)  # Light green

# UI Layout
SIDEBAR_WIDTH = 200
TOP_BAR_HEIGHT = 60
BOTTOM_PANEL_HEIGHT = 100
PANEL_PADDING = 10
PANEL_CORNER_RADIUS = 15
PANEL_MARGIN = 5  # Margin between panels and game area

# Game settings
GRID_SIZE = 80
GRID_COLS = 9
GRID_ROWS = 5
LAWN_COLOR = (20, 100, 20)  # Dark green for the lawn
GRID_LINE_COLOR = (30, 110, 30)  # Slightly lighter green for grid lines

# Game Area
GAME_AREA_TOP = TOP_BAR_HEIGHT + PANEL_MARGIN
GAME_AREA_BOTTOM = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT - PANEL_MARGIN

# Plant settings
INITIAL_SUN = 500
SUNFLOWER_COST = 50
PEASHOOTER_COST = 100
WALLNUT_COST = 50

SUNFLOWER_HEALTH = 80
PEASHOOTER_HEALTH = 100
WALLNUT_HEALTH = 300

# Sun settings
SUN_GENERATION_TIME = 5000  # 5 seconds
NATURAL_SUN_INTERVAL = 10000  # 10 seconds
SUN_LIFETIME = 5000  # 5 seconds

# Zombie settings
ZOMBIE_HEALTH = 100
CONE_ZOMBIE_HEALTH = 200
BUCKET_ZOMBIE_HEALTH = 300
ZOMBIE_SPEED = 0.5  # Reduced speed
ZOMBIE_DAMAGE = 25
ZOMBIE_TYPES = ['normal', 'cone']  # Different types of zombies
ZOMBIE_ATTACK_DELAY = 1000  # Attack every second
MAX_ZOMBIES = 10  # Maximum number of zombies on screen

# Wave settings
FIRST_WAVE_DELAY = 10000  # 10 seconds before first wave
WAVE_INITIAL_DELAY = 30000  # 30 seconds before first wave
WAVE_ZOMBIE_COUNT = [3, 5, 7, 10]  # Number of zombies per wave
ZOMBIE_SPAWN_INTERVAL = 3000  # 3 seconds between zombies
WAVE_SPAWN_DELAY = 2000  # Delay between zombies in a wave
MAX_WAVES = len(WAVE_ZOMBIE_COUNT)  # Maximum number of waves

# Bullet settings
BULLET_SPEED = 7
BULLET_DAMAGE = 25

# Button settings
BUTTON_SIZE = 70
BUTTON_MARGIN = 10

# Menu settings
TITLE_SIZE = 64
MENU_FONT_SIZE = 36
MENU_ITEM_SPACING = 20
MENU_START_Y = 250

# Menu colors
TITLE_COLOR = (0, 100, 0)  # Dark green
MENU_ITEM_COLOR = WHITE
MENU_ITEM_SELECTED = YELLOW
MENU_ITEM_HEIGHT = 50
MENU_ITEM_PADDING = 20
MENU_HOVER_COLOR = (0, 120, 0)  # Medium green

# Menu items
MENU_ITEMS = ['Start Game', 'Help', 'Quit']

# Menu animations
TITLE_BOUNCE_HEIGHT = 20
TITLE_BOUNCE_SPEED = 2
MENU_ITEM_GROW = 1.2  # Scale factor when hovering

# Game states
MENU = 'menu'
PLAYING = 'playing'
GAME_OVER = 'game_over'
VICTORY = 'victory'
HELP = 'help'

# Game states
PAUSED = "PAUSED"
