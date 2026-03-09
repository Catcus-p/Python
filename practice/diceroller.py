import random

while True:
    input("Press Enter to roll dice")
    
    dice = random.randint(1,6)
    print("You rolled:", dice)

    again = input("Roll again? (y/n): ")
    if again != "y":
        break