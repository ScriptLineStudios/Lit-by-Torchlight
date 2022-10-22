import pygame
import math
import geometry

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.fov = 100
        self.increment_angle = self.fov / 1000

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi) 
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def raycast(self, game):
        ray_angle = self.clamp_angle(self.angle - self.fov / 2)
        for ray_count in range(1000):
            looks_up =  not (0 < ray_angle < math.pi)
            looks_right = not (math.pi/2 < ray_angle < 3*math.pi/2)

            horizontal = False
            vertical = False

            #horizontal
            if math.tan(ray_angle) != 0:
                hoz_dist = 0

                yn = -(self.y - (self.y // 33) * 33)
                if looks_up:
                    yn += 33
                xn = yn / math.tan(ray_angle)
                
                ys = -33
                if looks_up:
                    ys = -ys
                xs = ys / math.tan(ray_angle)

                target_x_hoz = self.x + xn
                target_y_hoz = self.y + yn


                wall = 0
                for i in range(200):
                    ix = int(target_x_hoz // 33)
                    iy = int(target_y_hoz // 33)
                    if not looks_up:
                        iy -= 1

                    if ix < 0 or iy < 0 or ix > len(game.temp_map[0]) - 1 or iy > len(game.temp_map) - 1:
                        break
                    if game.temp_map[iy][ix] == 1:
                        horizontal = True
                        hoz_dist = math.hypot(target_x_hoz, target_y_hoz)
                        break

                    target_x_hoz += xs
                    target_y_hoz += ys



            #vertical there may be some sketchy stuff in here, not anymore!
            if math.tan(ray_angle) != 1:

                vert_dist = 0
                xn = -(self.x - (self.x // 33) * 33)
                if not looks_right:
                    xn += 33
                yn = xn * math.tan(ray_angle)

                xs = -33
                if not looks_right:
                    xs = -xs
                ys = xs * math.tan(ray_angle)

                target_x_vert = self.x + xn
                target_y_vert = self.y + yn
                for i in range(200):
                    ix = int(target_x_vert // 33)
                    iy = int(target_y_vert // 33)

                    if looks_right:
                        ix -= 1 

                    if ix < 0 or iy < 0 or ix > len(game.temp_map[0]) - 1 or iy > len(game.temp_map) - 1:
                        break
                    if game.temp_map[iy][ix] == 1:
                        vertical = True
                        vert_dist = math.hypot(target_x_vert, target_y_vert)
                        break

                    target_x_vert += xs
                    target_y_vert += ys

            #if hoz_dist < vert_dist:
            l1 = geometry.Line(self.x, self.y, target_x_hoz, target_y_hoz)
            l2 = geometry.Line(self.x, self.y, target_x_vert, target_y_vert)
            dist = min(l1.length, l2.length)
            if (l1.length < l2.length):
                pygame.draw.line(game.display, (0,0,255), (self.x, self.y), (target_x_hoz, target_y_hoz)) 
            else:
                pygame.draw.line(game.display, (255,0,255), (self.x, self.y), (target_x_vert, target_y_vert)) 
            dist = 10000 / dist
            draw_line = geometry.Line(ray_count, 400 - dist, ray_count, 400 + dist)
            pygame.draw.line(game.display, (255, 0, 0), (draw_line.x1, draw_line.y1), (draw_line.x2, draw_line.y2))
            #else:
             #   pygame.draw.line(game.display, (0,0,255), (self.x, self.y), (target_x_vert, target_y_vert)) 

            ray_angle += self.increment_angle / self.fov


    def draw(self, game):
        self.raycast(game)
        pygame.draw.circle(game.display, (255, 0, 0), (self.x, self.y), 10)