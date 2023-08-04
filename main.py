from setting import *
import pygame
import numpy
import time
import game
import math


pygame.init()
pygame.font.init()
pygame.display.set_caption("")
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
max_fps = 60
screen_x, screen_y = screen.get_size()
pygame.mouse.set_visible(False)
font = pygame.font.Font("assets/pixel.ttf", 25)

game = game.Game()
previous_mouse_pos = 0

def calculate_new_xy(old_xy, speed, angle_in_radians):
    new_x = old_xy[0] + -(speed * math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed * math.sin(angle_in_radians))
    return new_x, new_y


def clip3D(p1, p2):

    step = ((zcd-p1[2])/(p2[2]-p1[2]))
    return ((p1[0] + (p2[0]-p1[0])*step) * game.player.fov / zcd + screen_x/2, (p1[1] + (p2[1]-p1[1])*step) * game.player.fov / zcd + screen_y/2)


playing = True
while playing:
    
    if pygame.mouse.get_pos()[0] != screen_x/2:
        game.player.camY -= ((pygame.mouse.get_pos()[0] - screen_x/2) * cam) * cam*3
        pygame.mouse.set_pos((screen_x/2, pygame.mouse.get_pos()[1]))
    if pygame.mouse.get_pos()[1] != screen_y/2:
        if (pygame.mouse.get_pos()[1] - screen_y/2 > 0 and not math.degrees(game.player.camX) > 85) or (pygame.mouse.get_pos()[1] - screen_y/2 < 0 and not math.degrees(game.player.camX) < -85):
            game.player.camX += ((pygame.mouse.get_pos()[1] - screen_y/2) * cam) * cam*3
        pygame.mouse.set_pos((pygame.mouse.get_pos()[0], screen_y/2))
    
    screen.fill((0, 0, 0))

    view_matrix = game.view_matrix()
    a = 0
    if len(game.points) > 0:
        for k in game.points:  # k[0] = points, k[1] = block center coords, k[2] = faces, k[3] = matrix coords, k[4] = color
            ps, vspoints = game.display_rect(k[0], view_matrix, screen_x, screen_y, screen)
            k[2] = []
            if game.player.pos[2] < k[1][2] - half_block:  #front
                if k[3][0] == 0:
                    k[2].append((3, 2, 1, 0))
                    # k[2].append((3, 2, 1))
                    # k[2].append((3, 0, 1))
                elif game.map[k[3][0] - 1][k[3][1]] == 0:
                    k[2].append((3, 2, 1, 0))
                    # k[2].append((3, 2, 1))
                    # k[2].append((3, 0, 1))
                        
            if game.player.pos[2] > k[1][2] + half_block:  # back
                if k[3][0] == len(game.map)-1:
                    k[2].append((7, 6, 5, 4))
                    # k[2].append((7, 6, 5))
                    # k[2].append((7, 4, 5))
                elif game.map[k[3][0] + 1][k[3][1]] == 0:
                    k[2].append((7, 6, 5, 4))
                    # k[2].append((7, 6, 5))
                    # k[2].append((7, 4, 5))
                    
            if game.player.pos[0] > k[1][0] + half_block:  # right
                if k[3][1] == len(game.map[k[3][0]])-1:
                    k[2].append((1, 5, 4, 0))
                    # k[2].append((4, 0, 1))
                    # k[2].append((4, 5, 1))
                elif game.map[k[3][0]][k[3][1] + 1] == 0:
                    k[2].append((1, 5, 4, 0))
                    # k[2].append((4, 0, 1))
                    # k[2].append((4, 5, 1))
                    
            if game.player.pos[0] < k[1][0] - half_block:  # left
                if k[3][1] == 0:
                    k[2].append((7, 6, 2, 3))
                    # k[2].append((7, 3, 2))
                    # k[2].append((7, 6, 2))
                elif game.map[k[3][0]][k[3][1] - 1] == 0:
                    k[2].append((7, 6, 2, 3))
                    # k[2].append((7, 3, 2))
                    # k[2].append((7, 6, 2))
                    
                    
            if game.player.pos[1] > k[1][1] + half_block:  # bottom
                k[2].append((3, 7, 4, 0))
                # k[2].append((7, 3, 0))
                # k[2].append((7, 4, 0))
            if game.player.pos[1] < k[1][1] - half_block:  # top
                k[2].append((2, 6, 5, 1))
                # k[2].append((6, 2, 1))
                # k[2].append((6, 5, 1))
            for i in k[2]:
                points = []
                if (type(ps[i[0]]) == tuple and type(ps[i[1]]) == tuple and type(ps[i[2]]) == tuple and type(ps[i[3]]) == tuple) and\
                   ((0 - block_size*5 <= ps[i[0]][0] <= screen_x + block_size*5 and 0 - block_size*5 <= ps[i[0]][1] <= screen_y + block_size*5) or
                    (0 - block_size*5 <= ps[i[1]][0] <= screen_x + block_size*5 and 0 - block_size*5 <= ps[i[1]][1] <= screen_y + block_size*5) or
                    (0 - block_size*5 <= ps[i[2]][0] <= screen_x + block_size*5 and 0 - block_size*5 <= ps[i[2]][1] <= screen_y + block_size*5) or
                    (0 - block_size*5 <= ps[i[3]][0] <= screen_x + block_size*5 and 0 - block_size*5 <= ps[i[3]][1] <= screen_y + block_size*5)):
                    points.append(ps[i[0]])
                    points.append(ps[i[1]])
                    points.append(ps[i[2]])
                    points.append(ps[i[3]])
                    
                
                
                    pts = [(vspoints[i[0]]), (vspoints[i[1]]), (vspoints[i[2]]), (vspoints[i[3]])]
                    if False in points:
                        lst = []
                        for x in range(len(points)):
                            if points[x] != False:
                                lst.append(points[x])
                            if (points[(x+1)%len(points)] == False and points[x] != False) or (points[(x+1)%len(points)] != False and points[x] == False):
                                lst.append(clip3D(pts[(x+1)%len(points)], pts[x]))
                        if len(lst)>=3:
                            pygame.draw.polygon(screen, k[4], lst)
                            a +=1
                        pass
                    else:
                        pygame.draw.polygon(screen, k[4], points)
                        a +=1


    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x, y = calculate_new_xy((game.player.pos[0], game.player.pos[2]), player_speed, -game.player.camY + math.radians(180))
        game.player.pos = [x, game.player.pos[1], y]
    if keys[pygame.K_q]:
        x, y = calculate_new_xy((game.player.pos[0], game.player.pos[2]), player_speed, -game.player.camY)
        game.player.pos = [x, game.player.pos[1], y]
    if keys[pygame.K_z]:
        x, y = calculate_new_xy((game.player.pos[0], game.player.pos[2]), player_speed, -game.player.camY + math.radians(360)/4)
        game.player.pos = [x, game.player.pos[1], y]
    if keys[pygame.K_s]:
        x, y = calculate_new_xy((game.player.pos[0], game.player.pos[2]), -player_speed, -game.player.camY + math.radians(360)/4)
        game.player.pos = [x, game.player.pos[1], y]
    if keys[pygame.K_SPACE]:
        game.player.pos[1] -= player_speed
    if keys[pygame.K_LCTRL]:
        game.player.pos[1] += player_speed

    if keys[pygame.K_LEFT]:
        game.player.camY += cam
    if keys[pygame.K_RIGHT]:
        game.player.camY -= cam
    if keys[pygame.K_DOWN] and not math.degrees(game.player.camX) > 90:
        game.player.camX += cam
    if keys[pygame.K_UP] and not math.degrees(game.player.camX) < -90:
        game.player.camX -= cam

    screen.blit(font.render(f"Coords: {round(game.player.pos[0], 1)}, {round(game.player.pos[1], 1)}, {round(game.player.pos[2], 1)}, CamX: {round(math.degrees(game.player.camX), 1)}, CamY: {round(math.degrees(game.player.camY), 1)}", True, (255, 255, 255)), (5, 5))
    screen.blit(font.render(f"Rendered Faces: {a}", True, (255, 255, 255)), (5, 25))
    screen.blit(font.render(f"Fps: {round(clock.get_fps(), 1)}", True, (255, 255, 255)), (5, 45))
    
    pygame.display.flip()
    clock.tick(max_fps)
    pygame.display.set_caption(f"{game.player.camY}")
    # 
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            time.sleep(0.2)
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                time.sleep(0.2)
                playing = False