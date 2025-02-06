import turtle
import random

class Obstacle(turtle.Turtle):

    COLORS=['red', 'blue', 'orange', 'black', 'green', 'yellow', 'purple']
    MIN_SPEED = 0.25
    MAX_SPEED = 0.5
    MOVE_INCREMENT = 0

    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(stretch_wid=1, stretch_len=1.5)
        self.color(random.choice(self.COLORS))
        self.penup()
        self.goto(300, random.randint(-200, 250))
        self.move_speed = random.uniform(self.MIN_SPEED, self.MAX_SPEED)
    
    def move(self):
        self.setx(self.xcor() - self.move_speed)
    
    def reset_position(self):
        if self.xcor() < -320:
            self.goto(300, random.randint(-200, 250))
            self.move_speed = random.uniform(self.MIN_SPEED, self.MAX_SPEED)

