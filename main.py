import pygame
import math
import pygame_shaders
import random

from scripts.player import Player
from scripts.bullet import Bullet
from scripts.enemy import Enemy

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.global_time = 0

        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"LIT BY TORCHLIGHT")

        #self.display = pygame.Surface((self.width, self.height))
        #self.display.set_colorkey((0, 0, 0))

        #self.shader = pygame_shaders.Shader(size=(self.width, self.height), display=(self.width, self.height), 
       #                 pos=(0, 0), vertex_path="shaders/vertex.glsl", 
       #                 fragment_path="shaders/default_frag.glsl", target_texture=self.display)

        self.clock = pygame.time.Clock()

        self.map1 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 9, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 9, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 9, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 9, 0, 0, 0, 1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 1],
            [1, 0, 0, 0, 9, 1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.enemy_kills = 0
        self.enemy = Enemy(128, 128)
        self.enemy2 = Enemy(200, 128)
        self.enemy_rects = []
        self.collide_indexers = [[0] * len(self.map1[0])] * len(self.map1)
        self.imgs = [[0] * len(self.map1[0])] * len(self.map1)
        self.img = pygame.image.load("assets/images/wall.png").convert()
        self.img_painting = pygame.image.load("assets/images/door.png").convert()
        self.game_over = False
        self.colliders = []
        self.door = []
        self.door_indexes = [[0] * len(self.map1[0])] * len(self.map1)


        self.font = pygame.font.Font("assets/font.ttf", 32)
        self.text = self.font.render("Goal: Kill all enemies", False, (255, 255, 255))

        i = 0
        for y, row in enumerate(self.map1):
            for x, col in enumerate(row):
                if self.map1[y][x] == 1:
                    self.colliders.append(pygame.Rect(x * 32, y * 32, 32, 32))
                    self.collide_indexers[y][x] = pygame.Rect(x * 32, y * 32, 32, 32)
                    self.imgs[y][x] = self.img
                if self.map1[y][x] == 2:
                    self.door.append(pygame.Rect(x * 32, y * 32, 32, 32))
                    self.door_indexes[y][x] = pygame.Rect(x * 32, y * 32, 16, 16)
                    

                if self.map1[y][x] == 9:
                    self.enemy_rects.append(Enemy(x * 32, y * 32))
                    self.map1[y][x] = 0

        self.player = Player(128, 128)
        self.torch = 100000

        pygame.mixer.music.set_volume(3)
        pygame.mixer.music.load("assets/sounds/disturb.ogg")
        pygame.mixer.music.play(-1)

        self.shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
        self.click = pygame.mixer.Sound("assets/sounds/click.wav")
        self.footstep1 = pygame.mixer.Sound("assets/sounds/footstep1.wav")
        self.footstep2 = pygame.mixer.Sound("assets/sounds/footsetp2.wav")


        self.click.set_volume(0.05)

        #images
        self.floor = pygame.image.load("assets/images/floor.png").convert()
        self.bullet = pygame.image.load("assets/images/bullet.png").convert_alpha()

        self.bullets = []

        self.firing = False
        self.shot = 0
    def main(self):
        rand = random.randrange(200, 300) 
        pygame.mouse.set_visible(False)
        forward = True
        running = True
        while running:

            self.global_time += 1
            #pygame_shaders.clear((0, 0, 0)) #Fill with the color you would like in the background
            self.display.fill((0, 0, 0)) #Fill with the color you set in the colorkey

            # for y, row in enumerate(self.map1):
            #     for x, col in enumerate(row):
            #         if self.map1[y][x] == 1:
            #             pygame.draw.rect(self.display, (255, 255, 255), (x * 32, y * 32, 32, 32))
            #         else: 
            #             pygame.draw.rect(self.display, (100, 100, 100), (x * 32, y * 32, 32, 32))
            self.player.draw(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.player.weapon == self.player.weapon_loaded:
                            self.firing = True

                    
                    if event.button == 3:
                        self.player.weapon = self.player.weapon_loaded

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.firing = False
                        self.shot = 0
                    if event.button == 3:
                        self.player.weapon = self.player.weapon_idle


            if self.firing:
                if self.shot <= 0:
                    self.shot_sound.play()
                    self.player.shooting = 1
                    self.firing = True
                    for i in range(1):
                        self.player.camera[0] += random.random() / 40
                        self.player.camera[1] += random.random() / 40
                    self.shot = 5
                else:
                    self.shot -= 1

            keys = pygame.key.get_pressed()
            self.player.movement = [0, 0]
            self.player.moving = False
            if keys[pygame.K_w]:
                forward = True
                self.player.x += math.sin(self.player.angle - self.player.fov) * ((7 * self.player.sprinting) + 1)
                self.player.y += math.cos(self.player.angle - self.player.fov) * ((7 * self.player.sprinting)+ 1)
                self.player.moving = True
            if keys[pygame.K_s]:
                forward = False
                self.player.x -= math.sin(self.player.angle - self.player.fov) * ((7 * self.player.sprinting)+ 1)
                self.player.y -= math.cos(self.player.angle - self.player.fov) * ((7 * self.player.sprinting)+ 1)
                self.player.moving = True

            if keys[pygame.K_SPACE] and self.game_over:
                Game(1200, 800).main()


            col = int(self.player.x // 32)
            row = int(self.player.y // 32)
            # player hits the wall (collision detection)
            if self.map1[row][col] == 1:
                if forward:
                    self.player.x -= math.sin(self.player.angle - self.player.fov) * 5
                    self.player.y -= math.cos(self.player.angle - self.player.fov) * 5
                else:
                    self.player.x += math.sin(self.player.angle - self.player.fov) * 5
                    self.player.y += math.cos(self.player.angle - self.player.fov) * 5

            if keys[pygame.K_t]:
                self.torch -= 100

            #print(self.player.angle)


            #self.player.sprinting = False

            if pygame.mouse.get_focused():
                difference = pygame.mouse.get_pos()[0] - 600
                differencey = pygame.mouse.get_pos()[1] - 500

                pygame.mouse.set_pos((600, 500))
                self.player.angle += difference * 0.01
                self.player.y_off += differencey * 0.01

            if self.global_time % 14 == 0:
                rand = random.randrange(300, 301)

            if self.global_time < 100:
                self.display.blit(self.text, (400, 10))

            if self.enemy_kills == 1:
                self.game_over = self.font.render("CONGRATS! YOU HAVE WON!", False, (255, 255, 255))
                self.display.blit(self.game_over, (300, 400))

            if self.game_over:
                if self.enemy_kills != 10:
                    
                    self.player.camera[0] += random.random() / 40
                    self.player.camera[1] += random.random() / 40
                    self.game_over = self.font.render("GAME OVER! PRESS SPACE TO RESTART", False, (255, 255, 255))
                    self.display.blit(self.game_over, (150, 400))

            #self.shader.send("random", [rand])
            #self.shader.render(self.display) #Render the display onto the OpenGL display with the shaders!
            pygame.display.flip()
            self.clock.tick(30)

Game(1200, 800).main()