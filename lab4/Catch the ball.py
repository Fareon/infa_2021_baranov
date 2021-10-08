import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 5
screen = pygame.display.set_mode((1500, 800))
scores = 0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    Рисует новый шарик
    :return: None
    """
    x = randint(100,1100)
    y = randint(100,800)
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def click_the_ball():
    """
    Эта функция будет "удалять" шарик при нажатии на него
    Так же она будет отвечать за подсчет очков 
    :return: 
    """


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')



    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()