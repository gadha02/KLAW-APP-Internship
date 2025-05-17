# filename: mult_table.py

# Function to print multiplication table of a given number
def print_multiplication_table(num, file=None):
    for i in range(1, 11):
        if file is not None:
            print(f"{num} x {i} = {num * i}", file=file)
        else:
            print(f"{num} x {i} = {num * i}")