# Space Invaders Game

import pygame
from pygame import mixer
import random
import math
import time


# Intialize the pygame. Will be present in every pygame game
pygame.init()
game = 'play'


# Creating the screen, numbers are width by height in pixels
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Game background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Player
playerImage = pygame.image.load('spaceship.png')
# Player X and Y is assigning starting point on the screen to the spaceship
playerX = 370
playerY = 480
playerX_change = 0



# Creating Multiple Enemies
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = [] 
num_of_enemies = 6


for i in range(num_of_enemies):
    # Enemy image
    enemyImage.append(pygame.image.load('enemy.png'))
    # Enemy X and Y is assigning starting point on the screen to the spaceship
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

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

# Explosion
blow_up = pygame.image.load('explosion.png')

# Ship Explosion
ship_blow = pygame.image.load('explode.png')

# Score Creation
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf',32) # str is the font name and the number is the font size

textX = 10
textY = 10

# Bullets Remaining
shots = 10
shots_font = pygame.font.Font('freesansbold.ttf',32)
shotsX = 450
shotsY = 10

def shots_remaining(x,y):
    shots_print = shots_font.render('Shots Remaining: ' + str(shots) ,True, (255,255,255))
    screen.blit(shots_print,(x,y))

# Game Over Text
game_over = pygame.font.Font('freesansbold.ttf',96)

def show_score(x,y):
    score = score_font.render('Score: ' + str(score_value), True, (255,255,255)) # Render the font, add the str version of the value, add True, then color values in RGB numbers
    screen.blit(score,(x,y))

# .blit is drawing the image on the screen
def player(x,y): 
    screen.blit(playerImage,(x,y))

def enemy(x,y): 
    screen.blit(enemyImage[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImage,(x+16,y+10)) # adding 16 and 10 so the bullet appears in the top middle of the spaceship

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
    if distance < 27:
        return True

def game_over_text():
    gameover_text = game_over.render('GAME OVER', True, (255,255,255))
    screen.blit(gameover_text,(100,250))

def explosion(x,y):
    screen.blit(blow_up,(x,y))

def ship_explosion(x,y):
    screen.blit(ship_blow,(x,y))

def game_loss():
    if enemyY[i] > 440:
        for j in range(num_of_enemies):
            enemyY[j] = 2000
            enemyX_change[j] = 0
        global game
        game_over_text()
        return True


# Game loop
running = True
while running:

    # Assigning RBG values to the screen. Values go from 0 - 255. Combination makes all the colors needed
    # Screen.fill needs to be called first so it is the first thing rendered
    # screen.fill((0, 0, 0))
    background = pygame.image.load('background.png')
    screen.blit(background,(0,0))

    # Checks to see if the game wants to be closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystoke is pressed, check if it is -> or <-
        if event.type == pygame.KEYDOWN: # KEYDOWN checks if any key has been pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready' and shots > 0:
                    # Bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Getting the current X-cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                    shots -= 1
                else:
                    pass
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
    for i in range(num_of_enemies):
        # ##################################
        # #Speed changes
        moving_speed = 0.1 * score_value
        # enemy_speed = float(2) + moving_speed
        # ##################################
        # Game over
        # if enemyY[i] > 40:
        #     for j in range(num_of_enemies):
        #         game = 'loss'
        #         enemyY[j] = 2000
        #         enemyX_change[j] = 0
        #     game_over_text()
        game_loss()
                
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2 + moving_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -(2 + moving_speed)
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion(enemyX[i],enemyY[i])
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            if shots < 9:
                shots += 2
            elif shots == 9:
                shots += 1
        enemy(enemyX[i],enemyY[i])

    

    # Bullet Movement
    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'


    shots_remaining(shotsX,shotsY)
    show_score(textX,textY)

    # loss = game_loss()
    if game_loss():
        ship_explosion(275,325)
        # ship_explosion_sound = mixer.Sound('ship-explosion.wav')
        # ship_explosion_sound.play(loops=0,maxtime=1,fade=0)
        
    else:
        player(playerX,playerY)
    


    pygame.display.update()
    # pygame.display.update is updating the screen as the game goes on







