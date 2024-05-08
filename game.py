import pygame
import random
from cloud import Cloud
from enemy import Enemy
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.WIDTH = 500
        self.HEIGHT = 700
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('assets/font/Terserah.ttf', 26)
        self.screen = pygame.display.set_caption('Queda Livre')
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.bg = (135, 206, 235)
        self.game_over = False
        self.clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 570, 1]]
        self.cloud_images = []
        for i in range(1, 4):
            img = pygame.image.load(f'assets\\images\\cloud{i}.png')
            self.cloud_images.append(img)
        self.player = Player(240, 40, 'assets\\images\\ball.png', 'score.txt')
        self.enemies = [[0, random.randint(400, self.HEIGHT - 100), 1]]
        self.helicopter = pygame.transform.scale(pygame.image.load('assets\\images\\enemy.png'), (200,150))
        self.bounce = pygame.mixer.Sound("assets\\sounds\\bounce.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets\\sounds\\game_over.mp3")
        pygame.mixer.music.load("assets\\sounds\\theme.mp3") #Música livre de direitos autorais.
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)

    def draw_clouds(self):
        platforms = []
        for j in range(len(self.clouds)):
            image = self.cloud_images[self.clouds[j][2] - 1]
            platform = pygame.rect.Rect((self.clouds[j][0], self.clouds[j][1] + 40), (120, 10))
            self.screen.blit(image, (self.clouds[j][0], self.clouds[j][1]))
            platforms.append(platform)
        return platforms

    def draw_enemies(self):
        enemy_rects = []
        for j in range(len(self.enemies)):
            enemy_rect = pygame.rect.Rect((self.enemies[j][0] + 10, self.enemies[j][1] + 60), (180, 70))
            enemy_rects.append(enemy_rect)
            if self.enemies[j][2] == 1:
                self.screen.blit(pygame.transform.flip(self.helicopter, 1, 0), (self.enemies[j][0], self.enemies[j][1]))
            elif self.enemies[j][2] == -1:
                self.screen.blit(self.helicopter, (self.enemies[j][0], self.enemies[j][1]))
        return enemy_rects

    def move_enemies(self):
        enemy_speed = 2 + self.player.score // 30
        for j in range(len(self.enemies)):
            if self.enemies[j][2] == 1:
                if self.enemies[j][0] < self.WIDTH:
                    self.enemies[j][0] += enemy_speed
                else:
                    self.enemies[j][2] = -1
            elif self.enemies[j][2] == -1:
                if self.enemies[j][0] > -200:
                    self.enemies[j][0] -= enemy_speed
                else:
                    self.enemies[j][2] = 1
            if self.enemies[j][1] < -100:
                self.enemies[j][1] = random.randint(self.HEIGHT, self.HEIGHT + 300)

    def update_objects(self):
        lowest_cloud = 0
        update_speed = 10
        if self.player.y > 350:
            self.player.y -= update_speed
            for j in range(len(self.enemies)):
                self.enemies[j][1] -= update_speed
            for j in range(len(self.clouds)):
                self.clouds[j][1] -= update_speed
                if self.clouds[j][1] > lowest_cloud:
                    lowest_cloud = self.clouds[j][1]
            if lowest_cloud < 650:
                num_clouds = random.randint(1, 2)
                if num_clouds == 1:
                    x_pos = random.randint(0, self.WIDTH - 70)
                    y_pos = random.randint(self.HEIGHT + 100, self.HEIGHT + 300)
                    cloud_type = random.randint(1, 3)
                    self.clouds.append([x_pos, y_pos, cloud_type])
                else:
                    x_pos = random.randint(0, self.WIDTH // 2 - 70)
                    y_pos = random.randint(self.HEIGHT + 100, self.HEIGHT + 300)
                    cloud_type = random.randint(1, 3)
                    x_pos2 = random.randint(self.WIDTH // 2 + 70, self.WIDTH - 70)
                    y_pos2 = random.randint(self.HEIGHT + 100, self.HEIGHT + 300)
                    cloud_type2 = random.randint(1, 3)
                    self.clouds.append([x_pos, y_pos, cloud_type])
                    self.clouds.append([x_pos2, y_pos2, cloud_type2])

    def run(self):
        while True:
            self.screen.fill(self.bg)
            self.timer.tick(self.fps)
            cloud_platforms = self.draw_clouds()
            player_rect = self.player.draw(self.screen)
            enemy_boxes = self.draw_enemies()
            self.move_enemies()
            self.update_objects()
            if self.game_over:
                end_text = self.font.render('Pressione Enter para Reiniciar', True, 'Black')
                self.screen.blit(end_text, (70,20))
                self.player.y = -300
                self.player.y_speed = 0
                self.player.g = 0

            for cloud in cloud_platforms:
                if self.player.direction == -1 and player_rect.colliderect(cloud):
                    self.player.y_speed *= -1
                    if self.player.y_speed > -2:
                        self.player.y_speed = -2
                    self.bounce.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.x_direction = -1
                    elif event.key == pygame.K_RIGHT:
                        self.player.x_direction = 1
                    if event.key == pygame.K_RETURN and self.game_over:
                        self.game_over = False
                        self.player.reset()
                        self.enemies = [[0, random.randint(400, self.HEIGHT - 100), 1]]
                        self.clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 570, 1]]
                        pygame.mixer.music.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.x_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        self.player.x_direction = 0

            self.player.update_position()
            for enemy in enemy_boxes:
                if player_rect.colliderect(enemy) and not self.game_over:
                    self.game_over_sound.play()
                    self.game_over = True

            self.player.update_score()
            score_text = self.font.render(f'Pontos:  {self.player.score}', True, 'black')
            self.screen.blit(score_text, (10, self.HEIGHT - 70))

            if self.player.score > self.player.high_score:
                self.player.high_score = self.player.score

            score_text2 = self.font.render(f'Recorde: {self.player.high_score}', True, 'red')
            self.screen.blit(score_text2, (10, self.HEIGHT - 40))

            pygame.display.flip()
