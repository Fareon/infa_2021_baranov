import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 50
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

global ball_x, ball_y, ball_r
ball_x, ball_y, ball_r = 0, 0, 0


def draw_new_ball():
    """
    Функция рисует шарик
    :return:
    """
    global ball_x, ball_y, ball_r
    ball_x, ball_y, ball_r = randint(100, 1400), randint(100, 700), randint(30, 100)
    ball_color = COLORS[randint(0, 5)]
    balls.append(circle(screen, ball_color, (ball_x, ball_y), ball_r))


clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            finished = True
        # Создаём первый шарик
        elif len(balls) == 0:
            draw_new_ball()
        # Проверяем, попали ли мы мышкой в шарик по т. Пифагора
        elif event.type == pygame.MOUSEBUTTONDOWN and \
                (ball_x - mouse_position[0]) ** 2 + (ball_y - mouse_position[1]) ** 2 <= ball_r ** 2:
            screen.fill(BLACK)
            scores += 1
            draw_new_ball()

    pygame.display.update()

print("Congratulations! Your score:", scores)
scores = 0
pygame.quit()