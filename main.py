import pygame
import random
import math
import button
from pygame import mixer

# Initialize pygame̥
pygame.init()

# Create the screen r̥
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./Images/background.png')


# Background
quit_img = pygame.image.load('./Images/quit.png')

# Title and Icons
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./Images/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./Images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
num_of_enemies = 6


# for i in range(num_of_enemies):
#     enemyImg.append(pygame.image.load('./Images/alien.png'))
#     enemyX.append(random.randint(0, 729))
#     enemyY.append(random.randint(50, 150))
#     enemyY_change.append(40)
#     enemyX_change.append(4)


def initEnemies():
    global enemyImg
    global enemyX
    global enemyY
    global enemyY_change
    global enemyX_change

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyY_change = []
    enemyX_change = []

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('./Images/alien.png'))
        enemyX.append(random.randint(0, 729))
        enemyY.append(random.randint(50, 150))
        enemyY_change.append(40)
        enemyX_change.append(4)


# Bullet
bulletImg = pygame.image.load('./Images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# Score
score_value = 0

score_font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

high_score_font = pygame.font.Font('freesansbold.ttf', 30)
high_score_extX = 200
high_score_extY = 10

# Play Again
play_again_img = pygame.image.load('./Images/play_again.png').convert_alpha()


play_again_button = button.Button(360, 280, play_again_img, 0.8)
quit_button = button.Button(410, 280, quit_img, 0.8)


def show_score(x, y):
    score = score_font.render(
        "Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Fetch high score from the file
high_score_file = open("high_score.txt", "r")
high_score_value = high_score_file.read()
high_score_file.close()


def show_high_score(x, y, high_score_value):
    high_score = high_score_font.render(
        "High Score: " + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(pow((enemyX - bulletX), 2) +
                         pow((enemyY - bulletY), 2))
    if distance < 27:
        return True


over_font = pygame.font.Font('freesansbold.ttf', 30)

running = True


def game_over(score, high_score):

    over = over_font.render("GAME O VER ", True, (255, 255, 255))
    screen.blit(over, (310, 250))
    global score_value
    global high_score_value

    if score > int(high_score):
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(score))
        high_score_file.close()
        show_high_score(high_score_extX, high_score_extY, score)
        high_score_value = score

    if play_again_button.draw(screen):
        score_value = 0
        initEnemies()
        game(running, playerX, playerX_change, bulletX,
             bulletY, bulletY_change, num_of_enemies)

    if quit_button.draw(screen):
        pygame.display.quit()
        pygame.quit()
        exit()


# Game loop
def game(running, playerX, playerX_change, bulletX, bulletY, bulletY_change, num_of_enemies):
    initEnemies()
    global bullet_state
    global score_value
    while running:
        screen.fill((0, 0, 0))

        # Background
        screen.blit(background, (0, 0))

        # for event in pygame.event.get():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("./sound/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX >= 730:
            playerX = 730
        if playerX < 0:
            playerX = 0

        # Enemy movement
        for i in range(num_of_enemies):

            if enemyY[i] > 420:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over(score_value, high_score_value)
                break

            enemyX[i] += enemyX_change[i]

            if enemyX[i] < 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]

            if enemyX[i] >= 730:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collision_sound = mixer.Sound("./sound/explosion.wav")
                collision_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 729)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_high_score(high_score_extX, high_score_extY, high_score_value)
        pygame.display.update()


game(running, playerX, playerX_change, bulletX,
     bulletY, bulletY_change, num_of_enemies)
