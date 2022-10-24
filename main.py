import pygame
import math
import pygame_shaders

from scripts.player import Player

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.global_time = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL)
        self.display = pygame.Surface((self.width, self.height))
        self.display.set_colorkey((0, 0, 0))

        self.shader = pygame_shaders.Shader(size=(self.width, self.height), display=(self.width, self.height), 
                        pos=(0, 0), vertex_path="shaders/vertex.glsl", 
                        fragment_path="shaders/default_frag.glsl", target_texture=self.display)

        self.clock = pygame.time.Clock()

        self.temp_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.collide_indexers = [[0] * len(self.temp_map[0])] * len(self.temp_map)
        self.colliders = []
        i = 0
        for y, row in enumerate(self.temp_map):
            for x, col in enumerate(row):
                if self.temp_map[y][x] == 1:
                    self.colliders.append(pygame.Rect(x * 32, y * 32, 32, 32))
                    self.collide_indexers[y][x] = pygame.Rect(x * 32, y * 32, 32, 32)

        self.player = Player(200, 200)

        self.img = pygame.image.load("test.png")

        self.torch = 7000

        self.enemy = pygame.Rect(128, 128, 32, 32)
        self.enemy_rects = [self.enemy]

        self.lines_per_enemy = 0
    def main(self):
        pygame.mouse.set_visible(False)
        running = True
        while running:
            self.global_time += 1
            pygame_shaders.clear((0, 0, 0)) #Fill with the color you would like in the background
            self.display.fill((0, 0, 0)) #Fill with the color you set in the colorkey

            # for y, row in enumerate(self.temp_map):
            #     for x, col in enumerate(row):
            #         if self.temp_map[y][x] == 1:
            #             pygame.draw.rect(self.display, (255, 255, 255), (x * 32, y * 32, 32, 32))
            #         else: 
            #             pygame.draw.rect(self.display, (100, 100, 100), (x * 32, y * 32, 32, 32))

            self.player.draw(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            keys = pygame.key.get_pressed()
            self.player.moving = False
            if keys[pygame.K_w]:
                self.player.x += math.sin(self.player.angle - self.player.fov)
                self.player.y += math.cos(self.player.angle - self.player.fov)
                self.player.moving = True
            if keys[pygame.K_s]:
                self.player.x -= math.sin(self.player.angle - self.player.fov)
                self.player.y -= math.cos(self.player.angle - self.player.fov)
                self.player.moving = True

            if keys[pygame.K_a]:
                self.player.y -= 2
                self.player.moving = True
            if keys[pygame.K_d]:
                self.player.y += 2
                self.player.moving = True


            if keys[pygame.K_t]:
                self.torch -= 100

            #print(self.player.angle)


            if pygame.mouse.get_focused():
                difference = pygame.mouse.get_pos()[0] - 600
                pygame.mouse.set_pos((600, 500))
                self.player.angle += difference * 0.01


            self.shader.render(self.display) #Render the display onto the OpenGL display with the shaders!
            pygame.display.flip()
            self.clock.tick()
            pygame.display.set_caption(f"{self.clock.get_fps()}")

Game(1200, 1000).main()