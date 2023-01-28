import turtle as t
from screen import ScreenMaker
from round_paddle import Paddle, controls_left, controls_right
from ball import Ball
from scorekeeper import Scorekeeper
import time

def switch_mode():
    if t.tracer():
        t.tracer(False)
    else:
        t.tracer(True)


t.tracer(False)

# Set up Screen
my_screen = ScreenMaker()
my_screen.draw_middle_line()
left_paddle = Paddle(side="left")
right_paddle = Paddle(side="right")
my_scores = {
    "left": Scorekeeper(x=-my_screen.width / 4, y=my_screen.height / 2),
    "right": Scorekeeper(x=my_screen.width / 4, y=my_screen.height / 2),
}
my_ball = Ball()
t.update()
t.listen()

while True:
    for sides in my_scores:
        my_scores[sides].show_score()
    left_paddle.check_boundaries(tl=(-my_screen.width / 2, my_screen.height / 2), br=(0, - my_screen.height / 2))
    left_paddle.continuous_motion()
    left_paddle.initiate(controls_left)
    left_paddle.stop(controls_left)

    right_paddle.check_boundaries(tl=(0, my_screen.height / 2), br=(my_screen.width / 2, - my_screen.height / 2))
    right_paddle.continuous_motion()
    right_paddle.initiate(controls_right)
    right_paddle.stop(controls_right)

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
    my_ball.moving()
    my_ball.collision_paddle(paddles=ball_positions)  # Add force vector
    if my_ball.check_win():
        left_paddle.paddle.goto(left_paddle.starting_point)
        right_paddle.paddle.goto(right_paddle.starting_point)
        my_scores[my_ball.winner].add_score()

    t.onkey(fun=switch_mode, key="c")
    time.sleep(0.0005)  # .005
    t.update()

# my_screen.screen.exitonclick()

# TODO: paddle phasing through ball when on max speed
# TODO: setting ball speed as a component vector of ball speed
