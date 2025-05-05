import random

def number_guess():
    print("The number is between 1 and 100")
    print("Guess the number")
    
    num = random.randint(1, 100)
    attempts = 0

    while True:
            guess = int(input("Enter your guess: "))
            attempts = attempts + 1
            
            if guess < 1 or guess > 100:
                print("Guess a number between 1 and 100")
            elif guess < num:
                print("Too small! Try again.")
            elif guess > num:
                print("Too large! Try again.")
            else:
                print(f"Congratulations! You guessed it in {attempts} attempts.")
                break

number_guess()
