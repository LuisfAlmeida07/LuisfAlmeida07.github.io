import turtle

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.color('black')
        self.penup()
        self.goto(0, -250)
        self.setheading(90)

    def move_up(self):
        if self.ycor() < 280:
            self.sety(self.ycor() + 20)

    def reset_position(self):
        if self.ycor() > 260:
            self.goto(0, -250)
        


    

