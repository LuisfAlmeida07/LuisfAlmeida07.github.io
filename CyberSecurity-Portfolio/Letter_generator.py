# Read invited names within the file and transform in a list
with open('C:/Trabalho/Python/Day 24/Mail+Merge+Project+Start/Mail Merge Project Start/Input/Names/invited_names.txt') as letter:
    invited = letter.readlines()

# Strip characters within the list
stripped_list = [s.strip('\n') for s in invited]

# Read the template letter
with open('C:\Trabalho\Python\Day 24\Mail+Merge+Project+Start\Mail Merge Project Start\Input\Letters\starting_letter.txt') as letter2:
    text = letter2.read()

# Generate letters for each name 
for name in stripped_list:
    personalized_letter = text.replace('[name]', name)
    
    # Save each letter as a file 
    with open(f"C:/Trabalho/Python/Day 24/Mail+Merge+Project+Start/Mail Merge Project Start/Output/ReadyToSend/{name}.txt", mode="w") as completed_letter:
        completed_letter.write(personalized_letter)