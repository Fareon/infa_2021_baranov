import math
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH, HEIGHT = SPACE = 800,600


def random_color():
    """
    :return: random_color parameters
    """
    return randint(0, 254), randint(0, 254), randint(0, 254)


class Ball:
    def __init__(self, position, velocity, color=None, r=15):
        """
        Initializes ball's initial parameters

        :param position: ball's initial velocity
        :param velocity: ball's initial velocity
        :param r: ball's radius
        :param color: ball's color
        """
        if color is None:
            color = random_color()
        self.screen = screen
        self.position = position
        self.r = r
        self.velocity = velocity
        self.color = color
        self.live = 30

    def draw(self):
        """
        Draws the ball
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            self.position,
            self.r
        )

    def move(self, reflection_cut=0.2, times_moved=1):
        """
        Moves the ball according to its velocity and position

        :param reflection_cut: part of velocity value cut by single reflection
        :param times_moved: stands for visible velocity of the ball
        """
        for _ in range(times_moved):
            self.check_and_reflect(reflection_cut)
            self.velocity[1] -= gravity
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]

    def check_and_reflect(self, reflection_cut):
        """
        Checks if the ball touches the walls and reflect if needed
        :param reflection_cut: part of velocity value cut by single reflection
        """
        for _ in range(2):
            if self.position[_] <= (self.r + 1) or self.position[_] >= (SPACE[_] - self.r - 1):
                self.velocity[_] = -(self.velocity[_] * (1 - reflection_cut))

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # Pifagor theorem
        hit = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= self.r ** 2 + obj.r ** 2
        if hit:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, position):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.angle = math.atan2((position[1] - new_ball.y), (position[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = - self.f2_power * math.sin(self.angle)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, position):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - 20 != 0:
                self.angle = math.atan(-(position[1] - 450) / (position[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen,
                         self.color,
                         (20, 450),
                         (20 + math.cos(self.angle) * self.f2_power, 450 - math.sin(self.angle) * self.f2_power),
                         2)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # FIXME: don't work!!! How to call this functions when object is created?

    def __init__(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED
        self.points = 0
        self.live = 1
        self.screen = screen

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode(SPACE)
bullet = 0
balls = []
gravity = 1

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()  # deleted event here
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(pygame.mouse.get_pos())

    for b in balls:
        b.move()
        if b.hit_test(target) and target.live:
            target.live = 0
            target.hit()
            target = Target()
    gun.power_up()

pygame.quit()
