import pygame
import os

# Initialize pygame
pygame.init()

def create_icon():
    # Create a 32x32 surface for the icon
    icon = pygame.Surface((32, 32))
    icon.fill((0, 0, 0))  # Fill with black for transparency
    icon.set_colorkey((0, 0, 0))  # Make black transparent
    
    # Draw a stylized peashooter
    # Stem
    pygame.draw.rect(icon, (0, 150, 0), (8, 12, 6, 12))
    
    # Head
    pygame.draw.rect(icon, (0, 200, 0), (14, 8, 12, 10))
    
    # Barrel
    pygame.draw.rect(icon, (0, 100, 0), (24, 10, 4, 6))
    
    # Pot
    pygame.draw.rect(icon, (139, 69, 19), (6, 24, 20, 8))
    pygame.draw.rect(icon, (160, 82, 45), (8, 22, 16, 3))
    
    # Highlight
    pygame.draw.rect(icon, (0, 230, 0), (16, 10, 2, 2))
    
    return icon

if __name__ == '__main__':
    # Create the icon
    icon = create_icon()
    
    # Save as .ico file
    if os.path.exists('icon.png'):
        os.remove('icon.png')
    pygame.image.save(icon, 'icon.png')

    # Convert PNG to ICO using PIL
    try:
        from PIL import Image
        img = Image.open("icon.png")
        img.save("icon.ico", format="ICO", sizes=[(32, 32)])
        os.remove("icon.png")
    except ImportError:
        print("PIL not installed, icon will not be created")
