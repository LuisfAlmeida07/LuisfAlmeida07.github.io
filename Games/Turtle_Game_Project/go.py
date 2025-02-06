import turtle 

def display_game_over():
    game_over_text = turtle.Turtle()
    game_over_text.color('black')
    game_over_text.penup()
    game_over_text.hideturtle()
    game_over_text.goto(0, 0)
    game_over_text.write('GAME OVER', align='center', font=('Arial', 30, 'bold'))



