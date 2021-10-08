import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 5
screen = pygame.display.set_mode((1500, 800))
scores = 0
balls = []

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
    x, y, r = (randint(100,1100), randint(100,800), randint(30,100))
    color = COLORS[randint(0, 5)]
    balls.append(circle(screen, color, (x, y), r))


def click_the_ball():
    """
    Эта функция будет "удалять" шарик при нажатии на него
    Так же она будет отвечать за подсчет очков 
    :return: 
    """


clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            scores += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            new_ball()
    pygame.display.update()

print("Congratulations! Your score:", scores)
scores = 0
pygame.quit()