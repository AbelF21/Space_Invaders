# Space Invaders Game

import pygame
import random

# Intialize the pygame. Will be present in every pygame game
pygame.init()

# Creating the screen, numbers are width by height in pixels
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Game background
background = pygame.image.load('background.png')


# Player
playerImage = pygame.image.load('spaceship.png')
# Player X and Y is assigning starting point on the screen to the spaceship
playerX = 370
playerY = 480
playerX_change = 0



# Enemy
enemyImage = pygame.image.load('enemy.png')
# Enemy X and Y is assigning starting point on the screen to the spaceship
enemyX = random.randint(0,736)
enemyY = random.randint(50,150)
enemyX_change = 2
enemyY_change = 40

# Bullet
bulletImage = pygame.image.load('bullet.png')
# Enemy X and Y is assigning starting point on the screen to the spaceship
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = 'ready'

# .blit is drawing the image on the screen
def player(x,y): 
    screen.blit(playerImage,(x,y))

def enemy(x,y): 
    screen.blit(enemyImage,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit('bullet.png',(x+16,y+10)) # adding 16 and 10 so the bullet appears in the top middle of the spaceship


# Game loop
running = True
while running:

    # Assigning RBG values to the screen. Values go from 0 - 255. Combination makes all the colors needed
    # Screen.fill needs to be called first so it is the first thing rendered
    screen.fill((0, 0, 0))
    background = pygame.image.load('background.png')
    screen.blit(background,(0,0))

    # Checks to see if the game wants to be closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystoke is pressed, check if it is -> or <-
        if event.type == pygame.KEYDOWN: # KEYDOWN checks if any key has been pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX,bulletY)
        if event.type == pygame.KEYUP: # KEYUP checks for when key has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # Player restriction for boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy restriction for boundaries
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 2
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -2
        enemyY += enemyY_change

    # Bullet Movement
    if bullet_state is 'fire':
        fire_bullet(playerX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    enemy(enemyX,enemyY)


    pygame.display.update()
    # pygame.display.update is updating the screen as the game goes on







