import pandas

data = pandas.read_csv('Squirrel_Data.csv')
unique_colors = data['Primary Fur Color'].unique()
colors_count = data['Primary Fur Color'].value_counts()
print(unique_colors)
print(colors_count)
