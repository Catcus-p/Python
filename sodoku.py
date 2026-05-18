# Auto Sudoku Generator + Player

import random
import copy

# Create empty board
board = [[0 for _ in range(9)] for _ in range(9)]

# Print board
def print_board(board):
    print()

    for i in range(9):

        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(9):

            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            if board[i][j] == 0:
                print(".", end=" ")
            else:
                print(board[i][j], end=" ")

        print()

    print()

# Check valid number
def is_valid(board, num, pos):

    row, col = pos

    # Check row
    for i in range(9):
        if board[row][i] == num and i != col:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num and i != row:
            return False

    # Check box
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):

            if board[i][j] == num and (i, j) != pos:
                return False

    return True

# Fill board
def fill_board(board):

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:

                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for num in numbers:

                    if is_valid(board, num, (row, col)):

                        board[row][col] = num

                        if fill_board(board):
                            return True

                        board[row][col] = 0

                return False

    return True

# Remove numbers to make puzzle
def remove_numbers(board, amount=40):

    for _ in range(amount):

        row = random.randint(0, 8)
        col = random.randint(0, 8)

        board[row][col] = 0

# Generate Sudoku
fill_board(board)

solution = copy.deepcopy(board)

remove_numbers(board)

# Game loop
while True:

    print_board(board)

    user = input("Enter row col number (example: 1 3 9) or 'q' to quit: ")

    if user.lower() == "q":
        print("Game exited.")
        break

    try:
        row, col, num = map(int, user.split())

        row -= 1
        col -= 1

        # Check correct answer
        if solution[row][col] == num and board[row][col] == 0:

            board[row][col] = num
            print("Correct!\n")

        else:
            print("Wrong number!\n")

    except:
        print("Invalid input!\n")

    # Check win
    if board == solution:

        print_board(board)
        print("You solved the Sudoku!")
        break