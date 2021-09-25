import pygame
from pygame.draw import *

WHITE = (255, 255, 255)
YELLOW = (255, 255, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

FPS = 30
screen = pygame.display.set_mode((700, 700))
screen.fill(WHITE)

pygame.draw.circle(screen, YELLOW, (350, 350), 100) #face
pygame.draw.circle(screen, BLACK, (350, 350), 100, 1) #face
pygame.draw.circle(screen, RED, (385, 320), 18)
pygame.draw.circle(screen, BLACK, (385, 320), 18, 1)        #right eye
pygame.draw.circle(screen, BLACK, (385, 320), 7)   #right eye center
pygame.draw.circle(screen, RED, (315, 320), 12)
pygame.draw.circle(screen, BLACK, (315, 320), 12, 1)  #left eye
pygame.draw.circle(screen, BLACK, (315, 320), 7)   #left eye center
pygame.draw.line(screen, BLACK, (310, 400), [390, 400], 15) #smile
pygame.draw.polygon(screen, BLACK, ((360, 315), (420, 275), (416, 269), (356, 309))) #right brow
pygame.draw.polygon(screen, BLACK, ((330, 316), (280, 276), (286, 270), (336, 310))) #left brow




pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()