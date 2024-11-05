import io
import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()
pygame.mixer.init()

def bytes_fonts(font):
    with open(font, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# set display
display = pygame.display.set_mode((800, 600))

# set title, icon and background
icon = pygame.image.load('ovni.png')
pygame.display.set_caption('Space Game')
pygame.display.set_icon(icon)
background = pygame.image.load('fondo.jpg')

# add music
mixer.music.load('MusicaFondo.mp3')
mixer.music.play(-1)

# player variables
img_player = pygame.image.load('cohete.png')
player_x = 368
player_y = 500
player_x_change = 0

# enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
amount_enemies = 8

for e in range(amount_enemies):
    img_enemy.append(pygame.image.load('enemigo.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(1)
    enemy_y_change.append(50)

# bullet variables
bullets = []
img_bullet = pygame.image.load('bala.png')
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 3
bullet_show = False

points = 0

# Fonts
bytes_font_points = bytes_fonts('freesansbold.ttf')
font = pygame.font.Font(bytes_font_points, 32)
text_x = 10
text_y = 10

# final text
bytes_font_final_text = bytes_fonts('biergartenli.ttf')
final_font = pygame.font.Font(bytes_font_final_text, 40)

# functions
def final_text():
    my_font_final = final_font.render('GAME OVER', True, (255, 255, 255))
    display.blit(my_font_final, (300, 200))

def show_points(x, y):
    text = font.render(f'Points: {points}', True, (255, 255, 255))
    display.blit(text, (x, y))


def player(x, y):
    display.blit(img_player, (x, y))

def enemy(x, y, ene):
    display.blit(img_enemy[ene], (x, y))

def shot_bullet(x, y):
    global bullet_show
    bullet_show = True
    display.blit(img_bullet, (x + 16, y + 10))

def is_crash(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False

#Game loop
execute = True
while execute:

    # background
    display.blit(background, (0,0))

    # event iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execute = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('disparo.mp3')
                bullet_sound.play()
                new_bullet = {"x": player_x, "y": player_y, "velocity": -5}
                bullets.append(new_bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # modify player location
    player_x += player_x_change

    # keep player in display
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736


    for e in range(amount_enemies):

        # game over
        if enemy_y[e] > 456:
            for k in range(amount_enemies):
                enemy_y[k] = 1000
            final_text()
            break

        # modify enemy location
        enemy_x[e] += enemy_x_change[e]

        # keep enemy in display
        if enemy_x[e] <= 0:
            enemy_x_change[e] = 1
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -1
            enemy_y[e] += enemy_y_change[e]

        # crash
        for bullet in bullets:
            crash = is_crash(enemy_x[e], enemy_y[e], bullet["x"], bullet["y"])
            if crash:
                crash_sound = mixer.Sound('Golpe.mp3')
                crash_sound.play()
                bullets.remove(bullet)
                points += 1
                enemy_x[e] = random.randint(0, 736)
                enemy_y[e] = random.randint(50, 200)
        enemy(enemy_x[e], enemy_y[e], e)

    # bullet movement
    for bullet in bullets:
        bullet["y"] += bullet["velocity"]
        display.blit(img_bullet, (bullet["x"] + 16, bullet["y"] + 10))
        if bullet["y"] < 0:
            bullets.remove(bullet)

    player(player_x, player_y)

    # show points
    show_points(text_x, text_y)

    # refresh display
    pygame.display.update()

