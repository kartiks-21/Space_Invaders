# importing pygame
import pygame
import random
import math
from pygame import mixer
# initialising pygame
pygame.init()

# setting pygame screen
screen = pygame.display.set_mode((800, 600))

# setting background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# setting icon and caption
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ss.png')
pygame.display.set_icon(icon)
# Player
playerimage = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_images = 6
for i in range(num_images):
    enemyimage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 749))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(3.0)
    enemyY_change.append(40)

# Bullet
bulletimage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 100)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (155, 155, 255))
    screen.blit(score,(x,y))

def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (90, 150))

def Player(x, y):
    screen.blit(playerimage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# loop for exiting the pygame screen
running = True
while running:

    # setting RGB
    screen.fill((0, 0, 0))
    # set background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # setting function for keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    enemyX += enemyX_change

    # setting up boundary
    if playerX < 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

    # ENEMY movement
    for i in range(num_images):
        #Game over
        if enemyY[i] > 440:
            for j in range(num_images):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            laser_sound = mixer.Sound('laser.wav')
            laser_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # BULLET movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    Player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
