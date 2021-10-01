import pygame
from pygame.draw import *
from random import randint
from numpy import pi

WHITE = (255, 255, 255)
YELLOW = (255, 255, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (204, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 153, 51)
BROWN = (204, 102, 0)
LIGHT_BROWN = (255, 204, 153)

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))


def background(sand_height: int, sea_height: int, sky_color=(), sand_color=(), sea_color=()):  # background
    screen.fill(sky_color)  # sky
    pygame.draw.line(screen, sand_color, (0, 650), (800, 650), sand_height)  # sand
    pygame.draw.line(screen, sea_color, (0, sand_height + sea_height), (800, sand_height + sea_height),
                     sea_height)  # sea


# clouds and sun
def cloud(number: int, x_range=[], y_range=[], color=()):
    # number - amoung of ckouds
    # x_range, y_range - area where will be clouds drew
    # color - color of clouds
    for i in range(number):
        cloud_x = randint(x_range[0], x_range[1])
        cloud_y = randint(y_range[0], y_range[1])
        pygame.draw.circle(screen, color, (cloud_x, cloud_y), 25)
        pygame.draw.circle(screen, BLACK, (cloud_x, cloud_y), 25, 1)


def sun(x: int, y: int, R: int, outlinning: int, color=()):
    # outlining - fatness of outline (set 0 if you wont make outline)
    pygame.draw.circle(screen, color, (x, y), R, outlinning)


# umbrella
def umbrella(main_color = (), pole_color = ()):
    pygame.draw.line(screen, pole_color, (150, 700), (150, 430), 10)
    pygame.draw.polygon(screen, main_color, ((145, 430), (35, 500), (265, 500), (155, 430)))
    umbrella_lines = [x for x in range(0, 90, 27)]
    for j in umbrella_lines:
        pygame.draw.line(screen, BLACK, (145, 430), (145 - j, 500), 1)
        pygame.draw.line(screen, BLACK, (155, 430), (155 + j, 500), 1)


# ship
def sheep(x0, y0, a: int, window_color=(), maincolor1=(), maincolor2=()):
    # x0, y0 - coords of left lower angle of rectangle, where sheep inscribed
    # a: int - scale (default sheep is 47 X 30)
    # draw main part of the sheep (line => nose => stern)
    pygame.draw.line(screen, maincolor1, (x0 + 10 * a, y0 - 5 * a), (x0 + 35 * a, y0 - 5 * a), 10 * a)
    pygame.draw.polygon(screen, maincolor1, [(x0 + 35 * a, y0), (x0 + 47 * a, y0 - 10 * a), (x0 + 35 * a , y0 - 10 * a)])
    pygame.draw.circle(screen, maincolor1, (x0 + 10 * a, y0 - 10 * a), 10 * a, draw_bottom_left=True)
    # mast
    pygame.draw.line(screen, BLACK, (x0 + 17 * a, y0 - 10 * a), (x0 + 17 * a, y0 - 30 * a), 4)
    # sail
    pygame.draw.polygon(screen, maincolor2, [(x0 + 35 * a, y0 - 21 * a), (x0 + 17 * a, y0 - 12 * a), (x0 + 22 * a, y0 - 21 * a), (x0 + 17 * a, y0 - 30 * a)])
    pygame.draw.polygon(screen, BLACK, [(x0 + 35 * a, y0 - 21 * a), (x0 + 17 * a, y0 - 12 * a), (x0 + 22 * a, y0 - 21 * a), (x0 + 17 * a, y0 - 30 * a)], 1)
    pygame.draw.line(screen, BLACK, (x0 + 35 * a, y0 - 21 * a), (x0 + 22 * a, y0 - 21 * a), 1)
    # window
    pygame.draw.circle(screen, window_color, (x0 + 33 * a, y0 - 5 * a), 3 * a)
    pygame.draw.circle(screen, BLACK, (x0 + 33 * a, y0 - 5 * a), 3 * a, 1)


def lets_drow():
    background(300, 150, LIGHT_BLUE, YELLOW, BLUE)
    cloud(20, [130, 261], [70, 201], WHITE)
    sun(700, 100, 60, 0, YELLOW)
    sheep(200, 200, 5, WHITE, BROWN, LIGHT_BROWN)
    umbrella(RED, ORANGE)

lets_drow()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:  # main cycle
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
