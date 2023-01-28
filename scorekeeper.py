import turtle as t


class Scorekeeper(t.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.size = 40

        self.x = x
        self.y = y - (self.size * 2)

        self.goto(self.x, self.y)
        self.hideturtle()
        self.scores = 0

    def generate(self, prompt, x, y, color, size):
        self.penup()
        self.pencolor(color)
        self.goto(x, y)
        self.write(arg=prompt, move=False, align='center', font=('Comic Sans', size, 'bold'))
        self.hideturtle()

    def remove(self):
        self.clear()

    def show_score(self):
        self.remove()
        self.generate(prompt=f"{self.scores}", x=self.x, y=self.y, color="white", size=self.size)

    def show_final_score(self):
        self.remove()
        self.pencolor("red")
        self.generate(prompt=f"Final score: {self.scores}", x=-50, y=0, color="white", size=self.size)

    def add_score(self, amount=1):
        self.scores += amount
