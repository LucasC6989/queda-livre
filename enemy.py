import pygame
import random

class Enemy:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def draw(self, screen, helicopter):
        enemy_rect = pygame.rect.Rect((self.x + 10, self.y + 60), (180, 70))
        if self.direction == 1:
            screen.blit(pygame.transform.flip(helicopter, 1, 0), (self.x, self.y))
        elif self.direction == -1:
            screen.blit(helicopter, (self.x, self.y))
        return enemy_rect

    def move(self, speed):
        self.x += speed * self.direction

    def reset_position(self, height):
        self.y = random.randint(height, height + 300)
