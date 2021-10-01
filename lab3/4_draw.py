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


def background(sand_height: int, sea_height: int):  # background
    screen.fill(LIGHT_BLUE)  # sky
    pygame.draw.line(screen, YELLOW, (0, 650), (800, 650), sand_height)  # sand
    pygame.draw.line(screen, BLUE, (0, sand_height + sea_height), (800, sand_height + sea_height), sea_height)  # sea


# clouds and sun
def cloud(number: int, x_range = [], y_range = []):
    # number - amoung of ckouds
    # x_range, y_range - area where will be clouds drew
    for i in range(number):
        cloud_x = randint(x_range[0], x_range[1])
        cloud_y = randint(y_range[0], y_range[1])
        pygame.draw.circle(screen, WHITE, (cloud_x, cloud_y), 25)
        pygame.draw.circle(screen, BLACK, (cloud_x, cloud_y), 25, 1)

pygame.draw.circle(screen, YELLOW, (700, 100), 60)

# umbrella
pygame.draw.line(screen, ORANGE, (150, 700), (150, 430), 10)
pygame.draw.polygon(screen, RED, ((145, 430), (35, 500), (265, 500), (155, 430)))
umbrella_lines = [x for x in range(0, 90, 27)]
for j in umbrella_lines:
    pygame.draw.line(screen, BLACK, (145, 430), (145 - j, 500), 1)
    pygame.draw.line(screen, BLACK, (155, 430), (155 + j, 500), 1)

# ship
pygame.draw.line(screen, BROWN, (399, 425), (650, 425), 60)
pygame.draw.polygon(screen, BROWN, [(650, 455), (650, 396), (750, 396)])
for f in range(0, 61, 3):
    pygame.draw.circle(screen, BROWN, (399, 396), 60, 850,
                       draw_bottom_left=True)
pygame.draw.line(screen, BLACK, (450, 395), (450, 225), 10)
pygame.draw.polygon(screen, LIGHT_BROWN, [(455, 225), (555, 310), (455, 395), (490, 310)])
pygame.draw.polygon(screen, BLACK, [(455, 225), (555, 310), (455, 395), (490, 310)], 1)
pygame.draw.line(screen, BLACK, (490, 310), (555, 310), 1)
pygame.draw.circle(screen, WHITE, (650, 425), 25)
pygame.draw.circle(screen, BLACK, (650, 425), 25, 5)

def lets_drow ():
    background(300, 150)
    cloud(15, [130, 261], [70, 201])
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
