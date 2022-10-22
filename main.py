import pygame
import math

from scripts.player import Player

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.temp_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.player = Player(200, 200)

    def main(self):
        pygame.mouse.set_visible(False)
        running = True
        while running:
            self.display.fill((0, 0, 0))

            for y, row in enumerate(self.temp_map):
                for x, col in enumerate(row):
                    if self.temp_map[y][x] == 1:
                        pygame.draw.rect(self.display, (255, 255, 255), (x * 32, y * 32, 32, 32))
                    else: 
                        pygame.draw.rect(self.display, (100, 100, 100), (x * 32, y * 32, 32, 32))


            self.player.draw(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.x -= math.cos(self.player.angle - self.player.fov)
                self.player.y -= math.sin(self.player.angle - self.player.fov)
            if keys[pygame.K_s]:
                self.player.x += math.cos(self.player.angle - self.player.fov)
                self.player.y += math.sin(self.player.angle - self.player.fov)

            #print(self.player.angle)


            if pygame.mouse.get_focused():
                difference = pygame.mouse.get_pos()[0] - 600
                pygame.mouse.set_pos((600, 500))
                self.player.angle += difference * 0.01


            self.clock.tick(60)
            pygame.display.set_caption(f"{self.clock.get_fps()}")
            pygame.display.update()

Game(1200, 1000).main()