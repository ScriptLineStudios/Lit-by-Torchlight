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

        self.weapon = pygame.image.load("assets/images/gun.png").convert()
        self.enemy = pygame.image.load("enemy.png").convert()

        self.weapon.set_colorkey((255, 255, 255))
        
        self.moving = False

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi) 
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def draw_sprites(self, game):
        dx = 32 + 0.5 - self.x;
        dy = 32 + 0.5 - self.y;

        dist = math.sqrt(dx*dx + dy*dy);

        spriteAngle = math.atan2(dy, dx) - self.angle;

        size = 1 / (math.cos(spriteAngle) * dist);

        x = math.tan(spriteAngle) * dist;

        pygame.draw.rect(game.display, (255,0,0), (x, 100,32, 32))

    def raycast(self, game):
        depths = [0] * 1200
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
            #pygame.draw.line(game.display, (255, 0, 0), final_line.a, final_line.b)
            beta = math.cos(ray_angle - self.angle)
            dist = final_line.length;

            dist = 15000 / dist

            draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)

            offset = int(off) % 32
            img = game.img.subsurface(offset, 0, 1, 32)
            img = pygame.transform.scale(img, (1, dist*2))
            i = img.copy()
            color = min(game.torch / dist, 255)
            #i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
            game.display.blit(i, (draw_line.x1, draw_line.y1))
            depths[ray_count] = dist

            point = ray.raycast(game.enemy_rects)
            if point is not None:
                final_line = geometry.Line(origin, (game.enemy_rects[0].x, game.enemy_rects[0].y))
                dist = final_line.length;

                dist = 15000 / dist

                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)

                subject_rect = game.collide_indexers[int(point[1] // 32)][int(point[0] // 32)]
                if abs(point[1] - subject_rect.y) < 0.00001:
                    off = point[0]

                if (point[1]) - (subject_rect.y - 96) < 0.00001: #i honestly don't know whats going on here but iw works im not complaining
                    off = point[0]

                if abs(point[0] - subject_rect.x) < 0.00001:
                    off = point[1]

                if abs((point[0] + 32) - subject_rect.x) < 0.00001:
                    off = point[1]

                offset = int(game.lines_per_enemy / (dist / 26)) % 32
                img = self.enemy.subsurface(offset, 0, 1, 32)
                img = pygame.transform.scale(img, (1, dist*2))
                i = img.copy()
                color = min(game.torch / dist, 255)
                #i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
                if game.lines_per_enemy < dist * 1.4 and dist > depths[ray_count] and dist < 300:
                    game.display.blit(i, (draw_line.x1, draw_line.y1))
                game.lines_per_enemy += 1



            ray_angle += self.increment_angle / self.fov

    def draw(self, game):
        self.raycast(game)
        game.display.blit(pygame.transform.scale(self.weapon, (800, 800)), (300, 300+(math.sin(game.global_time / 10)*10) * int(self.moving)))
        #pygame.draw.circle(game.display, (255, 0, 0), (self.x, self.y), 10)
