import pygame

class Player:
    def __init__(self, x, y, ball_image_path, score_file_path):
        self.x = x
        self.y = y
        self.ball = pygame.transform.scale(pygame.image.load(ball_image_path), (50, 50))
        self.direction = -1
        self.y_speed = 0
        self.g = 0.2
        self.x_speed = 3
        self.x_direction = 0
        self.score = 0
        self.total_distance = 0
        file = open(score_file_path, 'r')
        read = file.readlines()
        self.high_score = int(read[0])

    def draw(self, screen):
        screen.blit(self.ball, (self.x, self.y))
        player_rect = pygame.rect.Rect((self.x + 4, self.y + 3), (45, 45))
        return player_rect

    def update_position(self):
        self.y_speed += self.g
        self.y += self.y_speed
        self.x += self.x_speed * self.x_direction

        if self.y_speed < 0:
            self.direction = 1
        else:
            self.direction = -1

        if self.direction == -1:
            if self.y_speed > 11:
                self.y_speed = 11

        if self.x > 450:
            self.x = 450
        elif self.x < 0:
            self.x = 0

    def update_score(self):
        self.total_distance += self.y_speed
        self.score = round(self.total_distance / 100)

    def reset(self):
        self.x = 240
        self.y = 40
        self.direction = -1
        self.y_speed = 0
        self.x_direction = 0
        self.score = 0
        self.g = 0.2
        self.total_distance = 0
