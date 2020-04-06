#importing libraries
import pygame
import sys
import random

#initializing pygame to start the game window
pygame.init()

#variable declarations 
width = 800
height = 600
red = (255,0,0)
blue = (0 , 0, 255)
background_color = (0,0,0)

#player and enemy size/ locations
player_size = width/16
player_pos = [width/2,height-2*player_size]
enemy_size = width/16
enemy_pos = [random.randint(0,width-enemy_size), 0]
enemy_list = [enemy_pos]

#misc. game variables, necessary for functions and logic
game_over = False
speed = 10
clock = pygame.time.Clock()
score = 0 
myFont = pygame.font.SysFont("monospace", 35)
#difficulty = [1,2,3,4,5]
#user_difficulty = input
#difficulty[i]

#collision detection pixel by pixel
def collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

#adds progression to the game by increasing speed based on score value
def set_level(score, speed):
    speed = score/5 + 3
    return speed


#function to spawn and drop enemy blocks
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < score/10+4 and delay < 0.1:
        x_pos = random.randint(0,width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
            pygame.draw.rect(screen, blue, (enemy_pos[0],enemy_pos[1],enemy_size,enemy_size))

def update_enemy_pos(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):

        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += speed

        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if collision(enemy_pos, player_pos):
            return True
    return False



#setting screen
screen = pygame.display.set_mode((width,height))

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                if x > 0:
                    x -= player_size
            elif event.key == pygame.K_RIGHT:
                if x < width-player_size:
                    x += player_size

            player_pos = [x,y]

    screen.fill(background_color)

    drop_enemies(enemy_list)

    score = update_enemy_pos(enemy_list, score)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, (255,255, 0))
    screen.blit(label, (width-200, height-40))

    speed = set_level(score, speed)
    if collision_check(enemy_list, player_pos):
        game_over = True

    draw_enemies(enemy_list)
    
    pygame.draw.rect(screen, red, (player_pos[0],player_pos[1],player_size,player_size))
    
    clock.tick(30)
    
    pygame.display.update()
