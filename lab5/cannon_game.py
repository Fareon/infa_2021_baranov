from random import randint
import numpy as np
import pygame

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH, HEIGHT = SPACE = 800, 600


def random_color():
    """
    :return: random_color parameters
    """
    return randint(0, 254), randint(0, 254), randint(0, 254)


class Ball:
    def __init__(self, position, vx, vy, color=None, r=15):
        """
        Initializes ball's initial parameters

        :param position: ball's initial velocity
        :param vx: ball's initial velocity (x axis)
        :param vy: ball's initial velocity (y axis)
        :param r: ball's radius
        :param color: ball's color
        """
        if color is None:
            color = random_color()
        self.screen = screen
        self.position = position
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.live = 150

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

    def move(self, reflection_cut=0.4, times_moved=1):
        """
        Moves the ball according to its velocity and position

        :param reflection_cut: part of velocity value cut by single reflection
        :param times_moved: stands for visible velocity of the ball
        """
        for _ in range(times_moved):
            self.vy -= gravity
            if self.check_and_reflect(reflection_cut):
                self.position[0] += self.vx / (1 - 1.1 * reflection_cut)
                self.position[1] -= self.vy / (1 - 1.1 * reflection_cut)
            else:
                self.position[0] += self.vx
                self.position[1] -= self.vy

    def check_and_reflect(self, reflection_cut):
        """
        Checks if the ball touches the walls and reflect if needed

        :param reflection_cut: part of velocity value cut by single reflection
        :return: Whether touched any of the walls (bool)
        """
        touched_wall = self.position[0] <= (self.r + 1) or self.position[0] >= (SPACE[0] - self.r - 1)
        touched_floor = self.position[1] <= (self.r + 1) or self.position[1] >= (SPACE[1] - self.r - 1)
        if touched_wall or touched_floor:
            if touched_wall:
                self.vx = -(self.vx * (1 - reflection_cut))
            if self.position[1] <= (self.r + 1) or self.position[1] >= (SPACE[1] - self.r - 1):
                self.vy = -(self.vy * (1 - reflection_cut))
            return True
        else:
            return False

    def hit_test(self, obj):
        """
        The function checks whether the ball hits the aim or not

        :param obj: object, for which the test takes place
        :return: Whether has hit or not (bool)
        """
        # Pifagor theorem
        hit = (self.position[0] - obj.position[0]) ** 2 + \
              (self.position[1] - obj.position[1]) ** 2 <= (self.r + obj.r) ** 2
        if hit:
            return True
        else:
            return False

    def tick_and_kill(self):
        """
        Makes the ball "older" and kills if too "old"
        """
        global balls
        if self.live > 0:
            self.live -= 1
        else:
            balls.remove(self)


class Gun:
    """
    Creates a gun. Controls its power, position and movement
    """

    def __init__(self):
        self.screen = screen
        self.power = 10
        self.is_active = False
        self.angle = 0
        self.color = GREY
        self.position = (WIDTH / 2, HEIGHT * 0.9)

    def fire_start(self):
        self.is_active = True

    def fire_end(self):
        """
        Fires with a ball
        """
        global balls, bullet
        bullet += 1
        ball_vx, ball_vy = self.power * np.cos(self.angle) / FPS * 30, self.power * np.sin(self.angle) / FPS * 30
        new_ball = Ball(list(self.position), ball_vx, ball_vy)
        new_ball.r += 5
        balls.append(new_ball)
        self.is_active = 0
        self.power = 10

    def targeting(self, position):
        """
        Sets gun's head according to mouse position
        :param position: mouse position
        """
        if event:
            if position[0] - self.position[0] != 0:
                tg = -(position[1] - self.position[1]) / (position[0] - self.position[0])
                if tg >= 0:
                    self.angle = np.arctan(tg)
                else:
                    self.angle = np.pi + np.arctan(tg)
        if self.is_active:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen,
                         self.color,
                         self.position,
                         (self.position[0] + np.cos(self.angle) * self.power,
                          self.position[1] - np.sin(self.angle) * self.power),
                         2)

    def power_up(self):
        if self.is_active:
            if self.power < 100:
                self.power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    """
    Initializes a target, controls its parameters
    """

    def __init__(self):
        self.r = randint(5, 40)
        self.position = [randint(self.r, WIDTH - self.r), randint(self.r, HEIGHT * 0.75 - self.r)]
        self.color = RED
        self.points = 0
        self.is_alive = True
        self.screen = screen
        self.velocity = [int(randint(-10, 10) / FPS * 30), int(randint(-10, 10) / FPS * 30)]

    def hit(self, points=1):
        """
        Ball hits the target
        :param points: added points
        """
        self.points += points

    def move(self):
        self.check_and_reflect()
        for _ in range(2):
            self.position[_] -= self.velocity[_]

    def check_and_reflect(self):
        """
        Checks if the target touches the walls and reflect if needed
        """
        touched_wall = self.position[0] <= (self.r + 1) or self.position[0] >= (SPACE[0] - self.r - 1)
        touched_floor = self.position[1] <= (self.r + 1) or self.position[1] >= (SPACE[1] * 0.75)
        if touched_wall:
            self.velocity[0] = np.sign(self.velocity[0]) * randint(-10, - np.abs(self.velocity[0]))
        if touched_floor:
            self.velocity[1] = np.sign(self.velocity[1]) * randint(-10, - np.abs(self.velocity[1]))

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.r)


pygame.init()
screen = pygame.display.set_mode(SPACE)
bullet = 0
balls = []
number_of_targets = 2
targets = []
gravity = 1
for _ in range(number_of_targets):
    targets.append(Target())

clock = pygame.time.Clock()
gun = Gun()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    for ball in balls:
        ball.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire_start()  # deleted event here
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire_end()
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(pygame.mouse.get_pos())

    gun.power_up()
    for ball in balls:
        ball.move()
        ball.tick_and_kill()
    for target in targets:
        for ball in balls:
            if ball.hit_test(target) and target.is_alive:
                target.is_alive = False
                target.hit()
                targets.remove(target)
                targets.append(Target())
                ball.live -= 150
        target.move()

pygame.quit()
