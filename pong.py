# Import the pygame library
from pygame import mixer
import pygame, random

from sys import exit

# Necessary Step! Initiates all of the parts of the Pygame library.
pygame.init()

# Create Screen - a display surface
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

# Add a label to the pygame window
pygame.display.set_caption("Pong clone")

# Create Clock object - responsible for controlling the games frame rate
clock = pygame.time.Clock() # create a clock object


all_sprites = pygame.sprite.Group() #contains all surfaces



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((5, 30), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect_center = (self.x, self.y)
        pygame.draw.rect(self.image, (255, 255, 255, 0), pygame.Rect(self.x, self.y, 5, 30))
        self.rect = self.image.get_rect(center = (self.x, self.y))


while True:
    #Event loop - Looks for for user input which could include: key presses, mouse movement, mouse clicks, etc.
    for event in pygame.event.get():
        # Close game if the red square in the top left of the window is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
   


    # Blits all surfaces to screen
    all_sprites.draw(screen)

    # Updates all of the images and objects on the screen (display surface)
    pygame.display.update()

    #Setting the game's frame rate to 60 frames per second
    clock.tick(30)
