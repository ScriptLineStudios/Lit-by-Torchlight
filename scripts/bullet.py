import pygame
import random
import math

class Bullet:
    def __init__(self, x, y, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

        self.rect = pygame.Rect(x, y, 8, 8)
        self.move = 0
        self.lifetime = 100
    def do(self, game):
        self.lifetime -= 1
        if self.move <= 0:
            self.rect.x += self.x_vel
            self.rect.y += self.x_vel

            self.move = 1
        else:
            self.move -= 1