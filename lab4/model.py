from random import randint


def init():
    """
    initializes model's computation
    """
    global screen_width, screen_height, space
    global number_of_balls, balls, super_balls, super_ball_possibility
    global GREEN, GREY, RED, BLUE, YELLOW, MAGENTA, CYAN, BLACK, COLORS

    screen_width, screen_height = space = (1500, 800)

    number_of_balls = 4
    balls = [gen_ball() for i in range(number_of_balls)]
    super_balls = []
    super_ball_possibility = 20

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
    ball_x = randint(ball_radius, screen_width - ball_radius)
    ball_y = randint(ball_radius, screen_height - ball_radius)
    ball_color = COLORS[randint(0, len(COLORS) - 1)]
    return [ball_color, ball_x, ball_y, ball_radius]


def generate_velocity_all_balls():
    """
    sets velocity for each ball
    :return:
    """
    for ball in balls:
        generate_velocity(balls, balls.index(ball))
    for super_ball in super_balls:
        generate_velocity(super_balls, super_balls.index(super_ball))


def generate_velocity(object_type, index=-1):
    """
    generates parameters for velocity of a ball
    :param object_type: defines which object will get a velocity
    :param index: index of a ball in a list of balls
    :return:
    """
    horizontal_velocity, vertical_velocity = randint(-100, 100) / 100, randint(-100, 100) / 100
    object_type[index].append(horizontal_velocity)
    object_type[index].append(vertical_velocity)


