import turtle as t
import random as r
import time
import numpy as np

HEIGHT = 600
WIDTH = 1000

color_set = ("red", "orange", "yellow", "green", "blue", "purple")


class Ball:
    def __init__(self):
        self.max_speed = 5
        self.flightspeed = 3
        self.speed = 2
        self.min_speed = 1.5
        self.increment = 0.5
        self.size = 1
        self.movable = True

        self.start_time = None
        self.winner = None
        self.body = t.Turtle(shape="circle", visible=True)
        self.body.penup()
        self.body.shapesize(self.size)
        self.body.color("red")
        self.body.setheading(r.randint(0, 360))

        self.distance_history = None

    def moving(self):
        if self.speed < 0:
            self.speed = -self.speed
            self.body.left(180)
        if self.movable:
            self.body.forward(self.speed)
            self.collision_wall()
            if self.speed > self.flightspeed:
                self.speed -= self.increment * 2

    def fine_moving(self):
        self.body.forward(1)
        self.collision_wall()

    def collision_wall(self):
        collision = False

        # upper wall
        if HEIGHT / 2 - self.body.ycor() <= 10:
            collision = True
            if self.body.heading() == 90:
                self.body.right(180)
            elif 90 < self.body.heading() < 180:
                angle = 2 * (180 - self.body.heading())
                self.body.left(angle)
            elif 0 < self.body.heading() < 90:
                angle = 2 * (self.body.heading())
                self.body.right(angle)

        # lower wall
        if self.body.ycor() + HEIGHT / 2 <= 10:
            collision = True
            if self.body.heading() == 270:
                self.body.right(180)
            elif 270 < self.body.heading() < 360:
                angle = 2 * (360 - self.body.heading())
                self.body.left(angle)
            elif 180 < self.body.heading() < 270:
                angle = 2 * (self.body.heading() - 180)
                self.body.right(angle)

        if collision is True and self.speed > self.min_speed:
            self.speed -= self.increment

    def collision_paddle(self, paddles):
        activated = False  # boolean for external functions
        for pad in paddles:

            if self.body.distance(pad["position"]) < pad["radius"] + (self.size * 10):
                self.movable = True
                initial_direction = self.body.heading()
                from_pad = self.body.towards(pad["position"])  # direction from pad
                criterion = (initial_direction - from_pad) % 360
                print(criterion)

                # Condition for if the paddle hits the ball from the front
                if 90 >= criterion or criterion >= 270:
                    # adjust direction
                    reverse_initial = (initial_direction + 180) % 360  # reverse direction
                    delt_angle = reverse_initial - from_pad
                    final_direction = from_pad - delt_angle
                    remainder = (final_direction) % 360  # rearrange ball direction to 0<x<360

                    self.body.setheading(remainder)

                    # adjust force
                    force_vector = pad["direction"]  # whole vector
                    theta = np.radians(final_direction - force_vector)
                    final_speed = pad["speed"] * np.cos(theta)

                    self.speed = final_speed*.7 + self.speed*.7

                # Condition for if the paddle hits the ball from behind ( 90 < angle < 270)
                elif 90 < criterion < 270 or not self.movable:
                    initial_speed = self.speed
                    angle_c = np.radians(180 - initial_direction + from_pad)
                    final_speed = np.sqrt(np.square(pad["speed"])+np.square(initial_speed)-(2*pad['speed']*initial_speed*np.cos(angle_c)))

                    self.speed = final_speed*2.5

                    sin_theta = (initial_speed*np.sin(angle_c))/final_speed
                    theta = np.arcsin(sin_theta)
                    d_theta = np.degrees(theta)
                    self.body.setheading(pad["direction"] + d_theta)

                # prevent trapping ball inside the pad
                while self.body.distance(pad["position"]) - 1 <= pad["radius"] + (self.size * 10):
                    self.moving()
                activated = True
        return activated

    def check_win(self):
        # right-bound out
        if self.body.xcor() - (self.size * 10) - 50 > WIDTH / 2 and not self.start_time:
            self.start_time = time.perf_counter()
            self.winner = 'left'

        # left-bound out
        if self.body.xcor() + (self.size * 10) + 50 < -WIDTH / 2 and not self.start_time:
            self.start_time = time.perf_counter()
            self.winner = 'right'

        if self.start_time:
            if time.perf_counter() - self.start_time >= 1:
                self.movable = False
                self.start_time = None
                self.serve(server=self.winner)
                return True

    def serve(self, server):
        if server == 'left':
            self.body.goto(-WIDTH / 4, 0)
            self.body.setheading(180)
        elif server == 'right':
            self.body.goto(WIDTH / 4, 0)
            self.body.setheading(0)

    def change_color(self):
        color_now = self.body.fillcolor()
        print(color_now)
        pos = color_set.index(color_now)
        new_pos = (pos + 1) % len(color_set)
        self.body.color(color_set[new_pos])
