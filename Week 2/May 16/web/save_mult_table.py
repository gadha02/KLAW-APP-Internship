# filename: save_mult_table.py

# Import the print_multiplication_table function
from mult_table import print_multiplication_table

# Empty the multiplication_table.txt file
with open("multiplication_table.txt", "w") as file:
    pass

# Redirect the output to the multiplication_table.txt file
with open("multiplication_table.txt", "a") as file:
    print_multiplication_table(7, file=file)