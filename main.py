import turtle as t
from screen import ScreenMaker
from round_paddle import Paddle, controls_left, controls_right
from ball import Ball
from scorekeeper import Scorekeeper
import time
from presets import orangeblue as my_package


# my_package = None

def switch_mode():
    if t.tracer():
        t.tracer(False)
    else:
        t.tracer(True)


t.tracer(False)

# Set up Screen
my_screen = ScreenMaker(preset=my_package)
my_screen.draw_middle_line()

# Set up paddles
left_paddle = Paddle(side="left", preset=my_package)
right_paddle = Paddle(side="right", preset=my_package)

# Set up scoreboard
my_scores = {
    "left": Scorekeeper(x=-my_screen.width / 4, y=my_screen.height / 2, preset=my_package),
    "right": Scorekeeper(x=my_screen.width / 4, y=my_screen.height / 2, preset=my_package),
}

# Set up ball
my_ball = Ball(preset=my_package)

t.update()
t.listen()

while True:
    # show updated score
    for sides in my_scores:
        my_scores[sides].show_score()

    # left paddle motion
    left_paddle.check_boundaries(tl=(-my_screen.width / 2, my_screen.height / 2), br=(0, - my_screen.height / 2))
    left_paddle.continuous_motion()
    left_paddle.initiate(controls_left)
    left_paddle.stop(controls_left)

    # right paddle motion
    right_paddle.check_boundaries(tl=(0, my_screen.height / 2), br=(my_screen.width / 2, - my_screen.height / 2))
    right_paddle.continuous_motion()
    right_paddle.initiate(controls_right)
    right_paddle.stop(controls_right)

    # update paddle information fed to ball class methods
    ball_positions = [
        {"position": left_paddle.paddle.position(),
         "direction": left_paddle.raw_angle(),
         "radius": left_paddle.size * 10,
         "speed": left_paddle.raw_speed()},
        {"position": right_paddle.paddle.position(),
         "direction": right_paddle.raw_angle(),
         "radius": right_paddle.size * 10,
         "speed": right_paddle.raw_speed()}
    ]

    # ball motion
    my_ball.moving()

    # check ball collision with paddle
    my_ball.collision_paddle(paddles=ball_positions)

    # check for out-of-bounds
    if my_ball.check_win():
        # return paddles to starting point
        left_paddle.paddle.goto(left_paddle.starting_point)
        right_paddle.paddle.goto(right_paddle.starting_point)
        # adds point to winner's side of the scoreboard
        my_scores[my_ball.winner].add_score()

    t.onkey(fun=switch_mode, key="c")  # manually starts animation to check for bugs
    time.sleep(0.0005)
    t.update()
