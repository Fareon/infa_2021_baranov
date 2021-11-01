from random import randint, choice
import numpy as np
import pygame


def random_color():
    """
    :return: random_color parameters
    """
    return randint(0, 254), randint(0, 254), randint(0, 254)


class GameManager:
    """"""

    def __init__(self, screen, number_of_targets):
        """
        Initialises the cannon game
        """
        self.screen = screen
        self.bullet = 0
        self.shots = []
        self.number_of_targets = 2
        self.targets = []
        self.clock = pygame.time.Clock()
        self.gun = Gun()
        self.finished = False
        for _ in range(number_of_targets):
            self.create_enemy()
        self.next_shot = choice(['Laser', 'Bomb'])

    def mainloop(self):
        """

        """
        pygame.init()
        while not self.finished:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire_start()  # deleted event here
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.fire()
                    self.gun.fire_end()
                    self.next_shot = choice(['Laser', 'Bomb'])
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targeting(pygame.mouse.get_pos())
            self.gun.power_up()

            for shot in self.shots:
                shot.move()
                shot.tick()
                if shot.live <= 0:
                    self.shots.remove(shot)
            for target in self.targets:
                for shot in self.shots:
                    if shot.hit_test(target, self.gun) == 'the end':
                        self.finished = True
                    elif shot.hit_test(target, self.gun) and target.is_alive:
                        target.is_alive = False
                        target.hit()
                        self.targets.remove(target)
                        self.create_enemy()
                target.move(times_moved=FPS // 2)
            self.screen.fill(WHITE)
            for target in self.targets:
                target.draw()
            for shot in self.shots:
                shot.draw()
            self.gun.draw(next_shot=self.next_shot)
            pygame.display.update()

        pygame.quit()

    def fire(self):
        self.bullet += 1
        shot_vx = self.gun.power * np.cos(self.gun.angle) / FPS * 20
        shot_vy = - self.gun.power * np.sin(self.gun.angle) / FPS * 20
        if self.next_shot == 'Laser':
            new_shot = Laser(list(self.gun.position), shot_vx, shot_vy)
        elif self.next_shot == 'Bomb':
            new_shot = Bomb(list(self.gun.position), shot_vx, -shot_vy)
        self.shots.append(new_shot)

    def create_enemy(self):
        if choice(['Ball', 'Cube']) == 'Ball':
            self.targets.append(Ball())
        else:
            self.targets.append(Cube())


class Gun:
    """
    Creates a gun. Controls its power, position and movement
    """

    def __init__(self):
        self.screen = window
        self.power = 10
        self.is_active = False
        self.angle = 0
        self.color = GREY
        self.position = [WIDTH / 2, HEIGHT * 0.9]

    def fire_start(self):
        self.is_active = True

    def fire_end(self):
        """
        Fires with a ball
        """
        self.is_active = 0
        self.power = 20

    def targeting(self, position):
        """
        Sets gun's head according to mouse position
        :param position: mouse position
        """
        if position[1] <= self.position[1]:
            if position[0] - self.position[0] != 0:
                tg = -(position[1] - self.position[1]) / (position[0] - self.position[0])
                if tg >= 0:
                    self.angle = np.arctan(tg)
                else:
                    self.angle = np.pi + np.arctan(tg)
        elif 30 < position[0] < WIDTH - 30:
            self.angle = np.pi / 2
            self.position[0] = position[0]
        if self.is_active:
            self.color = RED
        else:
            self.color = GREY

    def draw(self, next_shot):
        if next_shot == 'Bomb':
            pygame.draw.line(self.screen,
                             self.color,
                             self.position,
                             (self.position[0] + np.cos(self.angle) * (self.power / 2 + 5),
                              self.position[1] - np.sin(self.angle) * (self.power / 2 + 5)),
                             5)
            pygame.draw.circle(self.screen, BLACK, self.position, 7)
        elif next_shot == 'Laser':
            pygame.draw.line(self.screen,
                             self.color,
                             self.position,
                             (self.position[0] + np.cos(self.angle) * (self.power / 2 + 5),
                              self.position[1] - np.sin(self.angle) * (self.power / 2 + 5)),
                             5)
            pygame.draw.circle(self.screen, BLUE, (self.position[0] + np.cos(self.angle) * (self.power / 2 + 5),
                                                   self.position[1] - np.sin(self.angle) * (self.power / 2 + 5)),
                               int(self.power / 10))

    def power_up(self):
        if self.is_active:
            if self.power < 150:
                self.power += 1
            self.color = RED
        else:
            self.color = GREY


class Shot:
    def __init__(self, position, vx, vy, live, color=None, r=20):
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
        self.screen = window
        self.position = position
        self.r = r
        self.vx = vx
        self.vy = vy
        self.live = live
        self.color = color
        self.gravity = gravity

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

    def tick(self):
        """
        Makes the shot "older"
        """
        if self.live > 0:
            self.live -= 1


class Laser(Shot):
    def __init__(self, position, vx, vy):
        super().__init__(position, vx, vy, 20)
        self.vx = 1000 * vx
        self.vy = 1000 * vy
        self.width = int(np.sqrt(vy ** 2 + vx ** 2) / 15) + 5

    def draw(self):
        pygame.draw.line(self.screen,
                         self.color,
                         self.position,
                         (self.position[0] + self.vx, self.position[1] + self.vy),
                         int(self.width / 20 * self.live))

    def move(self):
        pass

    def hit_test(self, obj, gun):
        """
        The function checks whether the ball hits the aim or not
        :param gun: object, which emits laser
        :param obj: object, for which the test takes place
        :return: Whether has hit or not (bool)
        """
        velocity_abs = np.sqrt(self.vx ** 2 + self.vy ** 2)
        c = -(self.vy * gun.position[0] - self.vx * gun.position[1])
        true_width = self.width / 20 * self.live
        hit = np.abs(obj.position[0] * self.vy + (-self.vx) * obj.position[1] + c) / velocity_abs <= obj.r + true_width
        if hit:
            return True
        else:
            return False


class Bomb(Shot):
    def __init__(self, position, vx, vy):
        super().__init__(position, vx, vy, 100)
        self.live = 50
        self.vx = vx * 0.8
        self.vy = vy * 0.8

    def move(self, reflection_cut=0, times_moved=1):
        """
        Moves the ball according to its velocity and position

        :param reflection_cut: part of velocity value cut by single reflection
        :param times_moved: stands for visible velocity of the ball
        """
        if self.live > 5:
            for _ in range(times_moved):
                self.vy -= self.gravity
                if self.check_and_reflect(reflection_cut):
                    self.position[0] += self.vx / (1 - 1.1 * reflection_cut)
                    self.position[1] -= self.vy / (1 - 1.1 * reflection_cut)
                else:
                    self.position[0] += self.vx
                    self.position[1] -= self.vy

    def hit_test(self, obj, gun):
        """
        The function checks whether the ball hits the aim or not
        :param gun: object, so that everything works  # костыль, пока что не знаю, как без него обойтись
                                                      # потом я превращу это в преимущество, сейчас костыль
        :param obj: object, for which the test takes place
        :return: Whether has hit or not (bool)
        """
        hit_gun = (self.position[0] - gun.position[0]) ** 2 + \
                  (self.position[1] - gun.position[1]) ** 2 <= self.r ** 2
        # Pifagor theorem
        hit_enemy = (self.position[0] - obj.position[0]) ** 2 + \
                    (self.position[1] - obj.position[1]) ** 2 <= (self.r + obj.r) ** 2
        if hit_gun and self.live < 10:
            return 'the end'
        if hit_enemy:
            if self. live > 10:
                self.live = 10
            return True
        else:
            return False

    def draw(self):
        r = self.r
        if self.live <= 10:
            self.r = r + 2 * (10 - self.live)
            pygame.draw.circle(self.screen, ORANGE, self.position, self.r)
        else:
            pygame.draw.line(self.screen, self.color,
                             (self.position[0] - self.r * np.sqrt(0.5), self.position[1] + self.r * np.sqrt(0.5)),
                             (self.position[0] + self.r * np.sqrt(0.5), self.position[1] - self.r * np.sqrt(0.5)), 3)
            pygame.draw.line(self.screen, self.color,
                             (self.position[0] + self.r * np.sqrt(0.5), self.position[1] + self.r * np.sqrt(0.5)),
                             (self.position[0] - self.r * np.sqrt(0.5), self.position[1] - self.r * np.sqrt(0.5)), 3)
            pygame.draw.line(self.screen, self.color,
                             (self.position[0] - self.r, self.position[1]),
                             (self.position[0] + self.r, self.position[1]), 3)
            pygame.draw.line(self.screen, self.color,
                             (self.position[0], self.position[1] + self.r),
                             (self.position[0], self.position[1] - self.r), 3)
            pygame.draw.circle(self.screen, BLACK, self.position, self.r - 6)


class Enemy:
    """
    Initializes a target, controls its parameters
    """

    def __init__(self):
        self.r = randint(5, 40)
        self.position = [randint(self.r, WIDTH - self.r), randint(self.r, HEIGHT * 0.75 - self.r)]
        self.color = RED
        self.points = 0
        self.is_alive = True
        self.screen = window
        self.velocity = [randint(-20, 20) / FPS, randint(-10, 10) / FPS]

    def hit(self, points=1):
        """
        Ball hits the target
        :param points: added points
        """
        self.points += points

    def check_and_reflect(self):
        """
        Checks if the target touches the walls and reflect if needed
        """
        touched_wall = self.position[0] <= (self.r + 1) or self.position[0] >= (SPACE[0] - self.r - 1)
        touched_floor = self.position[1] <= (self.r + 1) or self.position[1] >= (SPACE[1] * 0.75)
        if touched_wall:
            self.velocity[0] = - self.velocity[0]
        if touched_floor:
            self.velocity[1] = - self.velocity[1]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.r)


class Cube(Enemy):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color,
                         (self.position[0] - self.r, self.position[1] - self.r, self.r * 2, self.r * 2))
        pygame.draw.circle(self.screen, WHITE,
                           (self.position[0] - int(self.r / 2), self.position[1] - int(self.r / 2)), int(self.r / 7))
        pygame.draw.circle(self.screen, WHITE,
                           (self.position[0] + int(self.r / 2), self.position[1] - int(self.r / 2)), int(self.r / 5))
        pygame.draw.rect(self.screen, WHITE,
                         (self.position[0] - int(self.r / 2), self.position[1] + int(self.r / 5),
                          self.r, int(self.r / 5)))

    def move(self, times_moved=30):
        for __ in range(times_moved):
            self.check_and_reflect()
            for _ in range(2):
                self.position[_] -= self.velocity[_]


class Ball(Enemy):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.r)
        pygame.draw.circle(self.screen, WHITE,
                           (self.position[0] - int(self.r / 2), self.position[1] - int(self.r / 2)), int(self.r / 7))
        pygame.draw.circle(self.screen, WHITE,
                           (self.position[0] + int(self.r / 2), self.position[1] - int(self.r / 2)), int(self.r / 5))
        pygame.draw.rect(self.screen, WHITE,
                         (self.position[0] - int(self.r / 2), self.position[1] + int(self.r / 5),
                          self.r, int(self.r / 5)))

    def move(self, reflection_cut=0, times_moved=30):
        """
        Moves the ball according to its velocity and position

        :param reflection_cut: part of velocity value cut by single reflection
        :param times_moved: stands for visible velocity of the ball
        """
        for _ in range(times_moved):
            self.velocity[1] -= (gravity / times_moved / FPS)
            if self.check_and_reflect():
                self.position[0] += self.velocity[0] / (1 - reflection_cut)
                self.position[1] -= self.velocity[1] / (1 - reflection_cut)
            else:
                self.position[0] += self.velocity[0]
                self.position[1] -= self.velocity[1]


FPS = 60

ORANGE = (255, 165, 0)
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
window = pygame.display.set_mode(SPACE)

gravity = 1
number_of_enemies = 2

game = GameManager(window, number_of_enemies)
game.mainloop()
