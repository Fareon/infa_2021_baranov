from random import randint


def init():
    """
    initializes model's computation
    """
    global screen_width, screen_height, space
    global number_of_balls, balls, super_balls, super_ball_possibility, targets_speed
    global GREEN, GREY, RED, BLUE, YELLOW, MAGENTA, CYAN, BLACK, COLORS

    screen_width, screen_height = space = (1500, 800)

    number_of_balls = 4
    balls = [gen_ball() for i in range(number_of_balls)]
    super_balls = []
    super_ball_possibility = 20
    targets_speed = 8

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


def gen_super_ball():
    """
    Generates parameters of a super ball
    :return: parameters for drawing a super ball
    """
    super_ball_radius = 80
    super_ball_x = randint(super_ball_radius, screen_width - super_ball_radius)
    super_ball_y = randint(super_ball_radius, screen_height - super_ball_radius)
    super_ball_color = (RED, BLUE, YELLOW, GREEN)
    return [super_ball_color, super_ball_x, super_ball_y, super_ball_radius]


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


def tick():
    move_balls(targets_speed)
    move_super_balls(targets_speed * 2)


def move_balls(times_moved):
    """
    Moves every ball according their position and velocity
    :param times_moved: indicates the speed of time
    :return:
    """
    for time in range(times_moved):
        for ball in balls:
            touched_border_1 = ball[1] <= ball[3] + 1 or ball[1] >= screen_width - (ball[3] + 1)
            touched_border_2 = ball[2] <= ball[3] + 1 or ball[2] >= screen_height - (ball[3] + 1)
            # checking the position and changing velocity if needed
            if touched_border_1 or touched_border_2:
                if touched_border_1:
                    ball[4] *= -1
                elif touched_border_2:
                    ball[5] *= -1

            ball[1] += ball[4]  # adding velocity to ball_x
            ball[2] += ball[5]  # adding velocity to ball_y


def move_super_balls(times_moved):
    """
    Moves a super ball according its position and velocity
    :param times_moved: indicates the speed of time
    :return:
    """
    for super_ball in super_balls:
        if super_ball[3] != 0:
            super_ball[3] -= 1
        else:
            super_balls.remove(super_ball)
            create_ball()
    for time in range(times_moved):
        for ball in super_balls:
            # checking the position and changing horizontal velocity if needed
            if ball[1] <= ball[3] + 1 or ball[1] >= screen_width - (ball[3] + 1):
                ball[4] *= -1

            # checking the position and changing vertical velocity if needed
            elif ball[2] <= ball[3] + 1 or ball[2] >= screen_height - (ball[3] + 1):
                ball[5] *= -1

            ball[1] += ball[4]  # adding velocity to ball_x
            ball[2] += ball[5]  # adding velocity to ball_y


def create_ball():
    """
    Creates a new ball
    :return:
    """
    balls.append(gen_ball())
    generate_velocity(balls)