import pygame
import math
import geometry

import functools
import numba

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.fov = 100
        self.increment_angle = self.fov / (1200 - 1)

        self.weapon_idle = pygame.image.load("assets/images/gun.png").convert()
        self.weapon_loaded = pygame.image.load("assets/images/gun_loaded.png").convert()
        self.muzzleflash = pygame.image.load("assets/images/muzzleflash.png").convert()

        self.muzzleflash.set_colorkey((255, 255, 255))


        self.weapon = self.weapon_idle

        self.enemy = pygame.image.load("assets/images/enemy.png").convert()

        self.weapon_idle.set_colorkey((255, 255, 255))
        self.weapon_loaded.set_colorkey((255, 255, 255))
        
        self.depths = [0] * 1200
        self.moving = False
        self.sprinting = False

        self.y_off = 0

        self.shooting = 0

        self.lines_per_enemy = [0] * 1000

        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.movement = [0, 0]
        self.camera = [1, 1]

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi) 
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def memorize(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            if key not in cache:
                cache[key] = func(*args, **kwargs)

            return cache[key]

        return wrapper

    def __cast(self, ray, colliders):
        return ray.raycast(colliders) 

    def cast(self, colliders, origin, endpoint):
        ray = geometry.Line(origin, endpoint)
        point = self.__cast(ray, colliders)

        return ray, point
    
    def ray(self, game, ray_angle, ray_count, dx, dy):
        origin = (self.x, self.y)
        endpoint = (dx, dy)

        ray, point = self.cast(game.colliders, origin, endpoint) 

        #pygame.draw.line(game.display, (255, 0, 0),  origin, point)

        off = 0
        subject_rect = game.collide_indexers[int(point[1] // 32)][int(point[0] // 32)]
        _ = game.imgs[int(point[1] // 32)][int(point[0] // 32)]
        if abs(point[1] - subject_rect.y) < 0.00001:
            off = point[0]

        if (point[1]) - (subject_rect.y - 96) < 0.00001: #i honestly don't know whats going on here but iw works im not complaining
            off = point[0]

        if abs(point[0] - subject_rect.x) < 0.00001:
            off = point[1]

        if abs((point[0] + 32) - subject_rect.x) < 0.00001:
            off = point[1]
        final_line = geometry.Line(origin, point)
        beta = math.cos(ray_angle - self.angle)
        dist = final_line.length;

        dist = 15000 / dist

        draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)
        offset = int(off) % 32
        img = _.subsurface(offset, 0, 1, 32)
        img = pygame.transform.scale(img, (1, dist*2))
        i = img.copy()
        color = min(10000 / dist, 255)
        i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
        game.display.blit(i, (draw_line.x1 * self.camera[0], draw_line.y1 * self.camera[1]))

        # floor_line = geometry.Line(draw_line.x1, draw_line.y2, draw_line.x1, draw_line.y2 + 800)
        # color = min(game.torch / floor_line.length, 255)

        # #pygame.draw.line(game.display, (color, color, color), floor_line.a, floor_line.b)

        # ceiling_line = geometry.Line(draw_line.x1, draw_line.y1, draw_line.x1, draw_line.y1 - 400)
        # #pygame.draw.line(game.display, (color, color, color), ceiling_line.a, ceiling_line.b)

        self.depths[ray_count] = dist




        
        for index, enemy in enumerate(game.enemy_rects):
            point = ray.raycast([enemy.rect]) 
            if point is not None:
                final_line = geometry.Line(origin, (enemy.rect.x, enemy.rect.y))

                dist = final_line.length;

                dist = 15000 / dist

                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)

                offset = int(self.lines_per_enemy[index] / (dist / 32)) % 32
                enemy.animate(game)
                img = enemy.image[enemy.animation_index // 300].subsurface(offset, 0, 1, 32)
                if game.player.shooting > 0:
                    if ray_count > 400 and ray_count < 650:
                        img = enemy.enemy_hit.subsurface(offset, 0, 1, 32)
                        if enemy.health > 0:
                            enemy.health -= 1
                            game.click.play()
                
                img = pygame.transform.scale(img, (1, dist*2))
                i = img.copy()
                color = min(game.torch / dist, 255)
                i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
                if self.lines_per_enemy[index] < dist * 1.4 and dist > self.depths[ray_count] and dist < 300:
                    game.display.blit(i, (draw_line.x1 * self.camera[0], draw_line.y1 * self.camera[1]))

                self.lines_per_enemy[index] += 1

        for index, bullet in enumerate(game.bullets):
            point = ray.raycast([bullet.rect]) 
            if point is not None:
                final_line = geometry.Line(origin, (bullet.rect.x, bullet.rect.y))

                dist = final_line.length;

                dist = 15000 / dist

                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)

                offset = int(self.lines_per_enemy[index] / (dist / 32)) % 32
                img = game.bullet.subsurface(offset, 0, 1, 32)
                img = pygame.transform.scale(img, (1, dist*2))
                i = img.copy()
                color = min(game.torch / dist, 255)
                i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
                if self.lines_per_enemy[index] < dist * 1.4 and dist > self.depths[ray_count] and dist < 300:
                    game.display.blit(i, (draw_line.x1 * self.camera[0], draw_line.y1 * self.camera[1]))

                self.lines_per_enemy[index] += 1

    def raycast(self, game):
        self.depths = [0] * 1200
        game.map1_data = [[0] * 10] * 9
        ray_angle = self.clamp_angle(self.angle)
        self.lines_per_enemy = [0] * 1000
        for ray_count in range(1200):
            dx = self.x + math.sin(ray_angle) * 1000
            dy = self.y + math.cos(ray_angle) * 1000

            self.ray(game, ray_angle, ray_count, dx, dy)

            ray_angle += (self.increment_angle / self.fov)

    def get_colliding_tiles(self, game):
        self.tiles = []
        for y, row in enumerate(game.map1):
            for x, col in enumerate(row):
                if game.map1[y][x] == 1:
                    tile_rect = pygame.Rect(x * 32, y * 32, 32, 32)
                    if tile_rect.colliderect(self.rect):
                        self.tiles.append(tile_rect)

        return self.tiles

    def move(self, game):
        self.x += self.movement[0]
        colliding_tiles = self.get_colliding_tiles(game)
        for tile in colliding_tiles:
            if self.movement[0] > 0:
                self.rect.right = tile.left
            elif self.movement[0] < 0:
                self.rect.left = tile.right

        self.y += self.movement[1]
        colliding_tiles = self.get_colliding_tiles(game)
        for tile in colliding_tiles:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom

    def draw(self, game):
        for enemy in game.enemy_rects:
            enemy.do(game)
            if enemy.dead:
                game.enemy_rects.remove(enemy)
        for bullet in game.bullets:
            if bullet.lifetime >= 0:
                bullet.do(game)
            else:
                game.bullets.remove(bullet)
        self.raycast(game)
        # self.draw_sprites(game)

        if self.camera[0] > 1:
            self.camera[0] -= self.camera[0] / 60
        else:
            self.camera[0] = 1

        if self.camera[1] > 1:
            self.camera[1] -= self.camera[1] / 60
        else:
            self.camera[1] = 1

        if self.shooting > 0:
            game.torch = 6800
            game.display.blit(pygame.transform.scale(self.muzzleflash, (300, 300)), (450, 400+(math.sin(game.global_time / 10)*10) * int(self.moving)))
            self.shooting -= 1
        else:
            game.torch = 7000
        game.display.blit(pygame.transform.scale(self.weapon, (600, 600)), (300, 300+(math.sin(game.global_time / 10)*10) * int(self.moving)))
        #pygame.draw.circle(game.display, (0, 0, 255), (self.x, self.y), 10)