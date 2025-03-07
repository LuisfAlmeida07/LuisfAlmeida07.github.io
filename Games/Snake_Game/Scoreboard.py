from turtle import Turtle

f = open('data.txt')
contents = f.read()
f.close()

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = int(contents)
        self.color('white')
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()
    
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align='center', font=('Courier', 24, 'normal'))
        
    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('data.txt', mode='w') as file:
                file.write(str(self.high_score))
        self.score = 0
        self.update_scoreboard()

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()
    