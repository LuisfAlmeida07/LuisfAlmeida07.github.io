import turtle
import pandas

# Reading the dataset and creating variables for it
data = pandas.read_csv('day-25-us-states-game-start/50_states.csv') # Reading the file


# Setup the screen
screen = turtle.Screen() 
screen.title('U.S. States Game')

# Setup the image in the screen
image = "C:/Trabalho/Python/Day 25/day-25-us-states-game-start/blank_states_img.gif" 
screen.addshape(image)
turtle.shape(image)

# Creating  a turtle for writing text
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

# List to store Guessed States
guessed_states = []

# Game Loop
while len(guessed_states) < 50:
    
    # Creating the text input
    answer_state = screen.textinput(
        title=f'{len(guessed_states)}/50 States Correct', 
        prompt="Guess a state's name?").title() # title() is to let all uppercase, lowercase being recognized as 'Title'. 


    if not answer_state or answer_state.lower() == "exit":
        missed_states = []
        for state in data['state'].values:
            if state not in guessed_states:
                missed_states.append(state)

        missed_states_df = pandas.DataFrame(missed_states, columns=['Missed States'])
        missed_states_df.to_csv('day-25-us-states-game-start/missed_states.csv', index=False)
        break

    # Checking if the answer corresponds to a state
    if answer_state in data['state'].values:
        state_data = data[data['state'] == answer_state]
        x, y = int(state_data['x'].values[0]), int(state_data['y'].values[0])
        writer.goto(x, y)
        writer.write(answer_state, align='center', font=('Times New Roman', 12, 'bold'))
    if answer_state in data["state"].values and answer_state not in guessed_states:
        guessed_states.append(answer_state)    

        



























# To discover the coordinates:
# def get_mouse_click_coor(x, y):
#     print(x, y)

# turtle.onscreenclick(get_mouse_click_coor)

# To let the game run
 



