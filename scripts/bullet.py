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
        if pygame.Rect(game.player.x, game.player.y, 4, 4).colliderect(pygame.Rect(self.rect.x, self.rect.y, 32, 32)):
            if game.enemy_kills != 10:
                game.game_over = True

        self.lifetime -= 1
        if self.move <= 0:
            self.rect.x += self.x_vel
            self.rect.y += self.y_vel

            self.move = 1
        else:
            self.move -= 1