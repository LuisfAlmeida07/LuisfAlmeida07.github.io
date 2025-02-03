import turtle
from player import Player
from enemy import Obstacle
from go import display_game_over
from level import Level

screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.bgcolor('white')
screen.title('The Turtle Game')


player = Player()
level = Level()

obstacles = [Obstacle() for _ in range(5)]

screen.listen()
screen.onkey(player.move_up, 'Up')

game_is_on = True
while game_is_on:
    screen.update()

    for obstacle in obstacles:
        obstacle.move()
        obstacle.reset_position()

        if player.distance(obstacle) < 20:
            display_game_over()
            game_is_on = False

    if player.ycor() > 260:
        player.reset_position()
        level.increase_level()
        for obstacle in obstacles:
            obstacle.move_speed += Obstacle.MOVE_INCREMENT

screen.exitonclick() 