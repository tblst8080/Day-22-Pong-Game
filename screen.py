import turtle as t

HEIGHT = 600
WIDTH = 1000
BG_COLOR = "black"


class LineMaker(t.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.pencolor("white")
        self.pensize(3)
        self.speed("fastest")

    def vertical(self, height):
        self.goto(0, -height / 2)
        self.pendown()
        self.goto(0, height / 2)
        self.penup()

    def horizontal(self, width):
        self.goto(-width / 2, 0)
        self.pendown()
        self.goto(width / 2, 0)
        self.penup()


class ScreenMaker:
    def __init__(self, preset = None):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = t.Screen()
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(width=self.width, height=self.height)
        self.screen.title(titlestring="Welcome to the Pong Game!")  # Screen title

        try:
            self.screen.bgpic(preset["bgpic"])
        except:
            pass
        try:
            self.screen.bgcolor(preset["bgcolor"])
        except:
            pass


    def draw_middle_line(self):
        new_line = LineMaker()
        new_line.vertical(height=self.height)

    # def animate(self):

