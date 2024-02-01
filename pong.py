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
    def __init__(self, x, y, index):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((10, 50), pygame.SRCALPHA, 32)
        self.image.fill((255, 255, 255))
        self.image = self.image.convert_alpha()
        self.rect_center = (self.x, self.y)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.deltay = 0
        self.index = index


    def move_down(self):
        if self.y < 575:
            self.deltay =5 
        else:
            self.y = 575
            self.deltay = 5
        self.y += self.deltay
        self.rect_center = (self.x, self.y)
        # pygame.draw.rect(self.image, (255, 255, 255, 0), pygame.Rect(self.x, self.y, 5, 30))
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def move_up(self):
        if self.y > 25:
            self.deltay =-5 
        else:
            self.y = 20
            self.deltay = 5
        self.y += self.deltay
        self.rect_center = (self.x, self.y)
        # pygame.draw.rect(self.image, (255, 255, 255, 0), pygame.Rect(self.x, self.y, 5, 30))
        self.rect = self.image.get_rect(center = (self.x, self.y))
    

class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, score):
        super().__init__()
        self.x = x
        self.y = y
        self.score_p1 = score[0]
        self.score_p2 = score[1]
        self.font = pygame.font.Font(None,100)
        self.pics = [self.font.render("Player 1 Won", False,"Green"), self.font.render("Player 2 won", False,"Red"), self.font.render(str(self.score_p1)+" - "+str(self.score_p2), False, "Blue")]
        self.image = self.pics[2]

    def change(self, score):
        
        if score[0] >= 5:
            self.image = self.pics[0]
            
        elif score[1] >= 5:
            self.image = self.pics[1]
            
        
    def update(self, score):
        self.score_p1 = score[0]
        self.score_p2 = score[1]
        print(score)
        self.pics[2] = self.font.render(str(self.score_p1)+" - "+str(self.score_p2), False, 'Blue')
        self.image = self.pics[2]
                


class Ball(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32) 
        self.image = self.image.convert_alpha()
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 128)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.rect_center = (self.x, self.y)
        self.deltax = 0
        self.deltay = 0
        self.moved = False

    def move(self, collide):
        if self.moved == False:
            self.deltax = random.randint(-5, 5)
            self.deltay = random.randint(-5, 5)
            while self.deltax == 0: 
                self.deltax = random.randint(-5, 5)
            while self.deltay == 0:
                self.deltay = random.randint(-5, 5)
            
        if  not (self.y > 0 and self.y < 600):
            self.deltay = -self.deltay
        if collide == True:
            self.deltax = -self.deltax

        self.x = self.x + self.deltax
        self.y = self.y +self.deltay

        self.rect = self.image.get_rect(center = (self.x, self.y))
        if self.x < 0:
            self.x = 400
            self.y = 300
            self.moved = False
            return 'p2'
            
        elif self.x > 800:
            self.x = 400
            self.y = 300
            self.moved = False
            return 'p1'
        self.moved = True
        return 'p0'

    


players = pygame.sprite.Group()

p1 = Player(100, 300, 0)
p2 = Player(700, 300, 1)
players.add(p1)
players.add(p2)

balls = pygame.sprite.Group()
balls.add(Ball(400, 300))

score = [0, 0]

shown = Score(350, 100, score)

objects = pygame.sprite.Group()

objects.add(players)
objects.add(balls)

while True:
    
    #Event loop - Looks for for user input which could include: key presses, mouse movement, mouse clicks, etc.
    for event in pygame.event.get():
        # Close game if the red square in the top left of the window is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        p2.move_up()
    if keys[pygame.K_DOWN]:
        p2.move_down()
    if keys[pygame.K_w]:
        p1.move_up()
    if keys[pygame.K_s]:
        p1.move_down()

    collide = False
    for ball in balls:
        collide = pygame.sprite.spritecollide(ball, players, False)
        if len(collide) == 1:
            collide = True
        var = ball.move(collide)
        
    if var == 'p2':
        score[1] +=1
        var = 'p0'
    elif var == 'p1':
        score[0] +=1
        var = 'p0'

    shown.change(score)

    if score[0] <= 5 and score[1] <= 5:
        print("AA")
        shown.update(score)

    # print(score)

    screen.fill((0, 0, 0))
    # Blits all surfaces to screen
    objects.draw(screen)
    screen.blit(shown.image, (shown.x, shown.y))

    # Updates all of the images and objects on the screen (display surface)
    pygame.display.flip()

    #Setting the game's frame rate to 60 frames per second
    clock.tick(60)
