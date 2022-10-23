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

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi) 
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def raycast(self, game):
        game.temp_map_data = [[0] * 10] * 9
        ray_angle = self.clamp_angle(self.angle)
        for ray_count in range(1200):
            looks_up =  not (0 < ray_angle < math.pi)
            looks_right = not (math.pi/2 < ray_angle < 3*math.pi/2)
            horizontal = False
            vertical = False

            #horizontal
            #target_x_hoz = 1000000
            #target_y_hoz = 1000000
            #print(math.tan(ray_angle))
            hoz_dist = 0

            yn = -(self.y - (self.y // 32) * 32)
            if looks_up:
                yn += 32
            xn = yn / math.tan(ray_angle+ 0.00001) 
            ys = -32
            if looks_up:
                ys = -ys
            xs = ys / math.tan(ray_angle+ 0.00001) 


            target_x_hoz = self.x + xn
            target_y_hoz = self.y + yn

            if (looks_right and (target_x_hoz > self.x)): 
                target_x_hoz = -target_x_hoz 
                target_y_hoz = -target_y_hoz 


            wall = 0
            for i in range(40):
                ix = int(target_x_hoz // 32)
                iy = int(target_y_hoz // 32)
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

            #pygame.draw.line(game.display, (0, 0, 255), (self.x, self.y), (target_x_hoz, target_y_hoz)) 

            #vertical there may be some sketchy stuff in here, not anymore!
            if math.tan(ray_angle) != 1:

                vert_dist = 0
                xn = -(self.x - (self.x // 32) * 32)
                if not looks_right:
                    xn += 32
                yn = xn * math.tan(ray_angle)

                xs = -32
                if not looks_right:
                    xs = -xs
                ys = xs * math.tan(ray_angle)

                target_x_vert = self.x + xn
                target_y_vert = self.y + yn
                for i in range(200):
                    ix = int(target_x_vert // 32)
                    iy = int(target_y_vert // 32)

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

                #pygame.draw.line(game.display, (255, 0, 255), (self.x, self.y), (target_x_vert, target_y_vert)) 
                
            #if hoz_dist < vert_dist:
            off = 0
            if horizontal and not vertical:
                l1 = geometry.Line(self.x, self.y, target_x_hoz, target_y_hoz)
                dist = l1.length
                ix = target_x_hoz
                iy = target_y_hoz
                off = ix
            elif vertical and not horizontal:
                l2 = geometry.Line(self.x, self.y, target_x_vert, target_y_vert)
                dist = l2.length
                ix = target_x_vert
                iy = target_y_vert
                off = iy
            else:
                l1 = geometry.Line(self.x, self.y, target_x_hoz, target_y_hoz)
                l2 = geometry.Line(self.x, self.y, target_x_vert, target_y_vert)
                dist = min(l1.length, l2.length)

                if (l1.length < l2.length):
                    #pygame.draw.line(game.display, (0,0,255), (self.x, self.y), (target_x_hoz, target_y_hoz)) 
                    ix = target_x_hoz
                    iy = target_y_hoz
                    off = ix
                else:
                    #pygame.draw.line(game.display, (255,0,255), (self.x, self.y), (target_x_vert, target_y_vert)) 
                    ix = target_x_vert
                    iy = target_y_vert
                    off = iy

            beta = math.cos(math.radians(ray_angle) - math.radians(self.angle))
            dist = 15000 / dist
            dist = dist
            #print(dist)
            try:
                color = (color[0] * dist / 255, color[1] * dist / 255, color[2] * dist/ 255)
                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)
                #pygame.draw.line(game.display, color, (draw_line.x1, draw_line.y1), (draw_line.x2, draw_line.y2))
            except:
                color = (255, 0, 0)
                draw_line = geometry.Line(ray_count, 500 - dist, ray_count, 500 + dist)
                #pygame.draw.line(game.display, color, (draw_line.x1, draw_line.y1), (draw_line.x2, draw_line.y2))

            offset = int(off) % 16
            ray_angle += self.increment_angle / self.fov
            img = game.img.subsurface(offset, 0, 1, 16)
            img = pygame.transform.scale(img, (1, dist * 2))
            i = img.copy()
            color = min(15000 / dist, 255)
            i.fill((color, color, color), special_flags=pygame.BLEND_RGB_SUB)
            game.display.blit(i, (draw_line.x1, draw_line.y1))


    def draw(self, game):
        self.raycast(game)
        pygame.draw.circle(game.display, (255, 0, 0), (self.x, self.y), 10)