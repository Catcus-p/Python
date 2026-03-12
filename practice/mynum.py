import random

lower = int(input("Enter lower number: "))
upper = int(input("Enter upper number: "))

number = random.randint(lower, upper)

while True:
    guess = int(input("guess the number: "))

    if guess == number:
        print("Correct! You guessed the number.")
        break
    elif guess < number:
        print("Too small")
    else:
        print("Too high")