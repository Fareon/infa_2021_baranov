import pygame
from pygame.draw import *
import lab4.model as model

player_name = input("Enter your name or nickname: ")

FPS = 60

pygame.init()
model.init()
scores = 0
scores_counter_position = (30, 30)
play_time = 60000

screen = pygame.display.set_mode(model.space)


def draw_balls():
    """
    Draws a ball on the screen
    :return:
    """
    for ball in model.balls:
        circle(screen, ball[0], (ball[1], ball[2]), ball[3])  # Unpacking the list
    for super_ball in model.super_balls:
        circle(screen, super_ball[0][0], (super_ball[1], super_ball[2]), super_ball[3])  # Unpacking the list
        circle(screen, super_ball[0][1], (super_ball[1], super_ball[2]), super_ball[3] - 20)
        circle(screen, super_ball[0][2], (super_ball[1], super_ball[2]), super_ball[3] - 40)
        circle(screen, super_ball[0][3], (super_ball[1], super_ball[2]), super_ball[3] - 60)


clock = pygame.time.Clock()
finished = False

while not finished:
    # Control
    clock.tick(FPS)
    if pygame.time.get_ticks() >= play_time:
        finished = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            scores += model.handler(mouse_position)

    # Model
    model.tick()

    # View
    screen.fill(model.BLACK)
    text = pygame.font.Font(None, 36)
    scores_counter = text.render(str(scores), True, model.GREY)
    screen.blit(scores_counter, scores_counter_position)
    draw_balls()

    pygame.display.update()

pygame.quit()

print("Congratulations,", player_name + "!", "You've scored", scores)
