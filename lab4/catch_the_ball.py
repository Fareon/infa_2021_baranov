import pygame
from pygame.draw import *
from random import randint
import numpy as np
pygame.init()

FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = SPACE = (1500, 800)
screen = pygame.display.set_mode(SPACE)

GREY = (200, 200, 200)
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
    ball_radius = randint(30, 80)
    ball_x = randint(ball_radius, SCREEN_WIDTH - ball_radius)
    ball_y = randint(ball_radius, SCREEN_HEIGHT - ball_radius)
    ball_color = COLORS[randint(0, len(COLORS) - 1)]
    return [ball_color, ball_x, ball_y, ball_radius]


def draw_balls():
    """
    Draws a ball on the screen
    :return:
    """
    for ball in balls:
        circle(screen, ball[0], (ball[1], ball[2]), ball[3])  # Unpacking the tuple


def erase_definer(position):
    """
    Checks whether mouse clicked on an object or not.
    If yes, erases the object and adds some scores.
    Otherwise, takes away 10 points from player's scores.
    :param position: Position of the mouse when clicked on the surface
    :return: How many scores should be added
    """
    inner_counter = 0
    mouse_x = position[0]
    mouse_y = position[1]
    for ball in balls:
        if (mouse_x - ball[1]) ** 2 + (mouse_y - ball[2]) ** 2 <= ball[3] ** 2:  # Pifagor theorem
            pop_ball(ball)
            inner_counter += int(np.sqrt(ball[4] ** 2 + ball[5] ** 2) * (80 - ball[3])) + 1
    if inner_counter == 0:
        inner_counter -= 10
    return inner_counter


def pop_ball(ball):
    """
    Erases the ball from the screen and creates a new one
    :return:
    """
    balls.remove(ball)
    balls.append(gen_ball())
    generate_velocity(-1)


def generate_velocity(ball_index):
    """
    generates parameters for velocity of a ball
    :param ball_index: index of a ball in a list of balls
    :return:
    """
    horizontal_velocity, vertical_velocity = randint(-100, 100) / 100, randint(-100, 100) / 100
    balls[ball_index].append(horizontal_velocity)
    balls[ball_index].append(vertical_velocity)


def generate_velocity_all_balls():
    """
    sets velocity for each ball
    :return:
    """
    for ball in balls:
        generate_velocity(balls.index(ball))


def move_balls(times_moved=1):
    """
    Moves every ball according their position and velocity
    :param times_moved: indicates the speed of time
    :return:
    """
    for time in range(times_moved):
        for ball in balls:
            # checking the position and changing horizontal velocity if needed
            if ball[1] <= ball[3] + 1 or ball[1] >= SCREEN_WIDTH - (ball[3] + 1):
                ball[4] *= -1

            # checking the position and changing vertical velocity if needed
            elif ball[2] <= ball[3] + 1 or ball[2] >= SCREEN_HEIGHT - (ball[3] + 1):
                ball[5] *= -1

            ball[1] += ball[4]  # adding velocity to ball_x
            ball[2] += ball[5]  # adding velocity to ball_y


number_of_balls = 5
balls = [gen_ball() for i in range(number_of_balls)]
generate_velocity_all_balls()
time_speed = 10
scores = 0
scores_counter_position = (30, 30)

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)

    # Control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            scores += erase_definer(mouse_position)

    # Model
    move_balls(time_speed)

    # View
    screen.fill(BLACK)
    text = pygame.font.Font(None, 36)
    scores_counter = text.render(str(scores), True, GREY)
    screen.blit(scores_counter, scores_counter_position)
    draw_balls()
    pygame.display.update()


pygame.quit()
