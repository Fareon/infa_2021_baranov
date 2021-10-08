import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
SCREEN_WIDTH, SCREEN_HEIGHT = SPACE = (1500, 800)
screen = pygame.display.set_mode(SPACE)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def gen_ball():
    """
    Generates parameters of a ball
    :return: parameters for drawing a ball
    """
    ball_radius = randint(10, 100)
    ball_x = randint(ball_radius, SCREEN_WIDTH - ball_radius)
    ball_y = randint(ball_radius, SCREEN_HEIGHT - ball_radius)
    ball_color = COLORS[randint(0, len(COLORS) - 1)]
    return ball_color, ball_x, ball_y, ball_radius


def draw_ball():
    """
    Draws a ball on the screen
    :return:
    """
    for ball in balls:
        circle(screen, ball[0], (ball[1], ball[2]), ball[3])


def erase_ball():
    """
    Erases the ball from the screen
    :return:
    """


balls = []

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    balls.append(gen_ball())
    draw_ball()
    pygame.display.update()


pygame.quit()