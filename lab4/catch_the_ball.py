import pygame
from pygame.draw import *
from random import randint
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
    ball_radius = randint(10, 100)
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
    Checks whether mouse clicked on a ball or not. If yes, erases the ball and adds a score point
    :param position: Position of the mouse when clicked on the surface
    :return: How many scores should be added
    """
    inner_counter = 0
    mouse_x = position[0]
    mouse_y = position[1]
    for ball in balls:
        if (mouse_x - ball[1]) ** 2 + (mouse_y - ball[2]) ** 2 <= ball[3] ** 2:  # Pifagor theorem
            erase_ball(ball)
            balls.append(gen_ball())
            generate_velocity(-1)
            inner_counter += 1
    return inner_counter


def erase_ball(ball):
    """
    Erases the ball from the screen
    :return:
    """
    balls.remove(ball)


def generate_velocity(ball_index):
    """
    generates parameters for velocity of a ball
    :param ball_index: index of a ball in a list of balls
    :return:
    """
    horizontal_velocity, vertical_velocity = randint(-20, 20), randint(-20, 20)
    balls[ball_index].append(horizontal_velocity)
    balls[ball_index].append(vertical_velocity)


def generate_velocity_all_balls():
    """

    :return:
    """
    for ball in balls:
        generate_velocity(balls.index(ball))


def move_balls():
    """
    Moves every ball according their position and velocity
    :return:
    """
    for ball in balls:
        ball[1] += ball[4]  # adding velocity to ball_x
        ball[2] += ball[5]  # adding velocity to ball_y


balls = [gen_ball() for i in range(10)]
generate_velocity_all_balls()
scores = 0
scores_counter_position = (30, 30)

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            scores += erase_definer(mouse_position)

    # View
    screen.fill(BLACK)
    text = pygame.font.Font(None, 36)
    scores_counter = text.render(str(scores), True, GREY)
    screen.blit(scores_counter, scores_counter_position)
    move_balls()  # Model string
    draw_balls()
    pygame.display.update()


pygame.quit()