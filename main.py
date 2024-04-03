import pygame
import random #Será responsável pela geração aleatória dos inimigos

pygame.init()
pygame.mixer.init
WIDTH = 400
HEIGHT = 640
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_caption('Queda Livre')

screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (135, 206, 235)

#Variáveis do Jogador
player_x = 170
player_y = 20
ball = pygame.transform.scale(pygame.image.load('assets\\images\\ball.png'), (50,50))
y_speed = 0.5 #Gravidade provisória
g = 0 #Aceleração da gravidade desativada por enquanto.
x_speed = 3
x_direction = 0.1

#Efeitos Sonoros
pygame.mixer.music.load("assets\\sounds\\theme.mp3") #Música livre de direitos autorais.
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)

def draw_player(x_pos, y_pos, player_img):
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos+4, y_pos+3), (45, 45))
    pygame.draw.rect(screen, 'green', player_rect, 3)
    return player_rect

run = True
while run:
    screen.fill(bg)
    timer.tick(fps)
    player = draw_player(player_x, player_y, ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0
    y_speed += g
    player_y += y_speed
    player_x += x_speed * x_direction

    pygame.display.flip()
pygame.quit()

