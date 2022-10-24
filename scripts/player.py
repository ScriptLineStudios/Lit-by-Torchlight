import pygame
import math
import geometry

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.fov = 100
        self.increment_angle = self.fov / (1200 - 1)

        self.weapon_idle = pygame.image.load("assets/images/gun.png").convert()
        self.weapon_loaded = pygame.image.load("assets/images/gun_loaded.png").convert()

        self.weapon = self.weapon_idle

        self.enemy = pygame.image.load("enemy.png").convert()

        self.weapon_idle.set_colorkey((255, 255, 255))
        self.weapon_loaded.set_colorkey((255, 255, 255))
        
        self.depths = [0] * 1200
        self.moving = False
        self.sprinting = False

        self.y_off = 0

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi) 
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def draw_sprites(self, game):
        sprite_a = math.atan2(128 - self.y, 128 - self.x)   # why atan2? https://stackoverflow.com/a/12011762
        

        sprite_d = ((self.x - 128)**2 + (self.y - 128)**2)**0.5
        sprite_size = (500/sprite_d) * 70

        sprite_x = 500 + (sprite_a - self.angle)*500/self.fov + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        pygame.draw.circle(game.display, (255, 0, 0), (sprite_x, sprite_y), 32)


    def raycast(self, game):
        self.depths = [0] * 1200
        game.temp_map_data = [[0] * 10] * 9
        ray_angle = self.clamp_angle(self.angle)
        game.lines_per_enemy = 0
        for ray_count in range(1200):
            dx = self.x + math.sin(ray_angle) * 1000
            dy = self.y + math.cos(ray_angle) * 1000

            origin = (self.x, self.y)
            endpoint = (dx, dy)

            ray = geometry.Line(origin, endpoint)
            point = ray.raycast(game.colliders ) 

            off = 0
            subject_rect = game.collide_indexers[int(point[1] // 32)][int(point[0] // 32)]
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
            img = game.img.subsurface(offset, 0, 1, 32)
            img = pygame.transform.scale(img, (1, dist*2))
            i = img.copy()
            color = min(game.torch / dist, 255)
            i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
            game.display.blit(i, (draw_line.x1, draw_line.y1))
            self.depths[ray_count] = dist

            point = ray.raycast(game.enemy_rects)
            if point is not None:
                final_line = geometry.Line(origin, (game.enemy_rects[0].x, game.enemy_rects[0].y))

                dist = final_line.length;

                dist = 15000 / dist

                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)

                offset = int(game.lines_per_enemy / (dist / 26)) % 32
                img = self.enemy.subsurface(offset, 0, 1, 32)
                img = pygame.transform.scale(img, (1, dist*2))
                i = img.copy()
                color = min(game.torch / dist, 255)
                i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
                if game.lines_per_enemy < dist * 1.4 and dist > self.depths[ray_count] and dist < 300:
                    game.display.blit(i, (draw_line.x1, draw_line.y1))


                game.lines_per_enemy += 1

            ray_angle += self.increment_angle / self.fov

    def draw(self, game):
        self.raycast(game)
       # self.draw_sprites(game)
        game.display.blit(pygame.transform.scale(self.weapon, (800, 800)), (300, 300+(math.sin(game.global_time / 10)*10) * int(self.moving)))
        #pygame.draw.circle(game.display, (255, 0, 0), (self.x, self.y), 10)
