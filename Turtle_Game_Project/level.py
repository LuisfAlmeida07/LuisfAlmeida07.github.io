import turtle

class Level:
    def __init__(self):
        self.level = 1
        self.level_display = turtle.Turtle()
        self.level_display.color('black')
        self.level_display.penup()
        self.level_display.hideturtle()
        self.update_level()

    def update_level(self):
        self.level_display.clear()
        self.level_display.goto(-250, 260)
        self.level_display.write(f'LEVEL: {self.level}', align='left', font=('Arial', 20, 'bold'))
    
    def increase_level(self):
        self.level += 1
        self.update_level()