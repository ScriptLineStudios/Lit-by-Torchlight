import pygame
import random
import math

from scripts.bullet import Bullet

class Enemy:
    def __init__(self, x, y):
        self.images = [pygame.image.load("enemy1.png"),
            pygame.image.load("enemy2.png"), pygame.image.load("enemy3.png"), pygame.image.load("enemy4.png"),
            pygame.image.load("enemy5.png"), pygame.image.load("enemy6.png"), pygame.image.load("enemy7.png"),
            pygame.image.load("enemy8.png"), pygame.image.load("enemy9.png"), pygame.image.load("enemy10.png"),
            pygame.image.load("enemy11.png"), pygame.image.load("enemy12.png")]

        self.death_images = [pygame.image.load("enemy_death1.png"),
            pygame.image.load("enemy_death2.png"), pygame.image.load("enemy_death3.png"), pygame.image.load("enemy_death4.png"),
            pygame.image.load("enemy_death5.png"), pygame.image.load("enemy_death6.png"), pygame.image.load("enemy_death7.png"),
            pygame.image.load("enemy_death8.png"), pygame.image.load("enemy_death9.png"), pygame.image.load("enemy_death10.png"),
            pygame.image.load("enemy_death11.png"), pygame.image.load("enemy_death12.png")]

        self.health = 1200 * 2
        self.dead = False

        self.enemy_hit = pygame.image.load("enemy_hit.png").convert()

        self.image = self.images
        
        self.animation_index = 0
        self.rect = pygame.Rect(x, y, 8, 8)
        self.move = 0

    def do(self, game):
        if self.health <= 0:
            self.image = self.death_images
        if self.move <= 0:
            game.bullets.append(Bullet(self.rect.x, self.rect.y, 1, 1))
            game.bullets.append(Bullet(self.rect.x, self.rect.y, -1, 1))
            game.bullets.append(Bullet(self.rect.x, self.rect.y, -1, -1))
            game.bullets.append(Bullet(self.rect.x, self.rect.y, 1, -1))

            self.move = 100
        else:
            self.move -= 1

    def animate(self, game):
        if (self.animation_index + 1 >= len(self.image) * 300):
            self.animation_index = 0;
            if self.health <= 0:
                self.dead = True
        self.animation_index += 1;