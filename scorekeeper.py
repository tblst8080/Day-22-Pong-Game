import turtle as t


class Scorekeeper(t.Turtle):
    def __init__(self, x, y, preset = None):
        super().__init__()
        self.size = 60
        self.font = ('Comic Sans', self.size, 'bold')
        self.color = "white"

        self.x = x
        self.y = y - (self.size * 2)

        self.goto(self.x, self.y)
        self.hideturtle()

        self.scores = 0
        try:
            self.color = preset['score_color']
        except:
            pass

    def remove(self):
        self.clear()

    def show_score(self):
        prompt = f"{self.scores}"
        self.remove()
        self.pen(pencolor = self.color)
        self.goto(self.x, self.y)
        self.write(arg=prompt, move=False, align='center', font=self.font)

    def add_score(self, amount=1):
        self.scores += amount
