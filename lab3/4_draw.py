import pygame
from pygame.draw import *


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
screen.fill(LIGHT_BLUE)

pygame.draw.line(screen, YELLOW, (0, 650), (800, 650), 300)
pygame.draw.line(screen, BLUE, (0, 450), (800, 450), 150)




pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()