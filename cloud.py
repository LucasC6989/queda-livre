import pygame

class Cloud:
    def __init__(self, x, y, cloud_type):
        self.x = x
        self.y = y
        self.cloud_type = cloud_type

    def draw(self, screen, cloud_images):
        image = cloud_images[self.cloud_type - 1]
        screen.blit(image, (self.x, self.y))
        platform = pygame.rect.Rect((self.x, self.y + 40), (120, 10))
        return platform
