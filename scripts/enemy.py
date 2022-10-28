import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.images = [pygame.image.load("enemy1.png"),
            pygame.image.load("enemy2.png"), pygame.image.load("enemy3.png"), pygame.image.load("enemy4.png"),
            pygame.image.load("enemy5.png"), pygame.image.load("enemy6.png"), pygame.image.load("enemy7.png"),
            pygame.image.load("enemy8.png"), pygame.image.load("enemy9.png"), pygame.image.load("enemy10.png"),
            pygame.image.load("enemy11.png"), pygame.image.load("enemy12.png")]
        
        self.animation_index = 0
        self.rect = pygame.Rect(x, y, 8, 8)
        self.move = 0

    def do(self, game):
        if self.move <= 0:
            self.rect.x += math.sin()
            self.move = 1
        else:
            self.move -= 1
        print(self.rect.x)

    def animate(self, game):
        if (self.animation_index + 1 >= len(self.images) * 300):
            self.animation_index = 0;
        self.animation_index += 1;