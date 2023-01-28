import turtle as t

HEIGHT = 600
WIDTH = 1000
color_set = ("red", "orange", "yellow", "green", "blue", "purple", "grey")
controls_left = {
    "left": "a",
    "right": "d",
    "up": "w",
    "down": "s"
}

controls_right = {
    "left": "Left",
    "right": "Right",
    "up": "Up",
    "down": "Down"
}


class Paddle:
    def __init__(self, side):
        self.maxspeed = 6
        self.minspeed = 1
        self.diminish = 0.3
        self.size = 5
        self.side = side
        self.speed = {
            "l": self.maxspeed,
            "r": self.maxspeed,
            "u": self.maxspeed,
            "d": self.maxspeed
        }
        self.bounds = {
            "l": True,
            "r": True,
            "u": True,
            "d": True,
        }
        self.switches = {
            "l": False,
            "r": False,
            "u": False,
            "d": False,
        }
        self.coord = {
            "left": -1,
            "right": 1
        }
        self.origin = {
            "left": (-WIDTH / 2 + 10, 0),
            "right": (WIDTH / 2 - 10, 0)
        }
        self.starting_point = (self.origin[side][0], 0)

        self.paddle = t.Turtle(shape="circle", visible=False)
        self.paddle.color("white")
        self.paddle.shapesize(self.size)
        self.paddle.penup()
        self.paddle.goto(self.starting_point)
        self.paddle.showturtle()

        self.shadow = t.Turtle(shape="circle", visible=False)
        self.shadow.penup()
        self.shadow.goto(self.origin[side][0], 0)

    def single_motion(self, direct):
        if direct == "l":
            self.paddle.setheading(180)
            self.paddle.forward(self.speed['l'])
        if direct == "r":
            self.paddle.setheading(0)
            self.paddle.forward(self.speed['r'])
        if direct == "u":
            self.paddle.setheading(90)
            self.paddle.forward(self.speed['u'])
        if direct == "d":
            self.paddle.setheading(270)
            self.paddle.forward(self.speed['d'])
        for way in self.speed:
            if self.speed[way] > self.minspeed:
                self.speed[way] -= self.diminish

    def continuous_motion(self):
        self.shadow_follow()
        for direction in self.switches:
            if self.switches[direction] and self.bounds[direction]:
                self.single_motion(direct=direction)

    def initiate_l(self):
        self.switches["l"] = True

    def initiate_r(self):
        self.switches["r"] = True

    def initiate_u(self):
        self.switches["u"] = True

    def initiate_d(self):
        self.switches["d"] = True

    def stop_l(self):
        self.switches["l"] = False
        self.speed['l'] = self.maxspeed

    def stop_r(self):
        self.switches["r"] = False
        self.speed['r'] = self.maxspeed

    def stop_u(self):
        self.switches["u"] = False
        self.speed['u'] = self.maxspeed

    def stop_d(self):
        self.switches["d"] = False
        self.speed['d'] = self.maxspeed

    def initiate(self, controls):
        t.onkeypress(fun=self.initiate_l, key=f"{controls['left']}")
        t.onkeypress(fun=self.initiate_r, key=f"{controls['right']}")
        t.onkeypress(fun=self.initiate_u, key=f"{controls['up']}")
        t.onkeypress(fun=self.initiate_d, key=f"{controls['down']}")

    def stop(self, controls):
        t.onkeyrelease(fun=self.stop_l, key=f"{controls['left']}")
        t.onkeyrelease(fun=self.stop_r, key=f"{controls['right']}")
        t.onkeyrelease(fun=self.stop_u, key=f"{controls['up']}")
        t.onkeyrelease(fun=self.stop_d, key=f"{controls['down']}")

    def check_boundaries(self, tl, br):
        if self.paddle.xcor() <= tl[0]:  # + (self.size*10):  # left bound
            self.bounds['l'] = False
        else:
            self.bounds['l'] = True
        if self.paddle.xcor() >= br[0]:  # - (self.size*10):  # right bound
            self.bounds['r'] = False
        else:
            self.bounds['r'] = True
        if self.paddle.ycor() >= tl[1]:  # - (self.size*10):  # upper bound
            self.bounds['u'] = False
        else:
            self.bounds['u'] = True
        if self.paddle.ycor() <= br[1]:  # + (self.size*10):  # lower bound
            self.bounds['d'] = False
        else:
            self.bounds['d'] = True

    def shadow_follow(self):
        self.shadow.goto(self.paddle.position())

    def raw_speed(self):
        return self.paddle.distance(self.shadow) # magnitude of motion

    def raw_angle(self):
        return self.shadow.towards(self.paddle) # direction of motion
