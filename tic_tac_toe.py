# AI Tic-Tac-Toe with Exit Option

import math

# Empty board
board = [" " for _ in range(9)]

# Print board
def print_board():
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("--+---+--")

# Check winner
def check_winner(player):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],  # Rows
        [0,3,6], [1,4,7], [2,5,8],  # Columns
        [0,4,8], [2,4,6]            # Diagonals
    ]

    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True

    return False

# Check draw
def is_draw():
    return " " not in board

# Get available moves
def available_moves():
    return [i for i in range(9) if board[i] == " "]

# Minimax AI
def minimax(is_maximizing):

    if check_winner("O"):
        return 1

    if check_winner("X"):
        return -1

    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf

        for move in available_moves():
            board[move] = "O"
            score = minimax(False)
            board[move] = " "

            best_score = max(score, best_score)

        return best_score

    else:
        best_score = math.inf

        for move in available_moves():
            board[move] = "X"
            score = minimax(True)
            board[move] = " "

            best_score = min(score, best_score)

        return best_score

# AI move
def ai_move():
    best_score = -math.inf
    best_move = None

    for move in available_moves():
        board[move] = "O"
        score = minimax(False)
        board[move] = " "

        if score > best_score:
            best_score = score
            best_move = move

    board[best_move] = "O"

# Player move
def player_move():
    while True:
        move = input("Choose position (1-9) or 0 to exit: ")

        # Exit game
        if move == "0":
            print("Game exited.")
            quit()

        # Valid move
        if move in [str(i) for i in range(1, 10)]:
            move = int(move) - 1

            if board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Spot already taken.")

        else:
            print("Invalid move.")

# Main game loop
while True:

    print()
    print_board()
    print()

    # Player turn
    player_move()

    if check_winner("X"):
        print()
        print_board()
        print("\nYou win!")
        break

    if is_draw():
        print()
        print_board()
        print("\nIt's a draw!")
        break

    # AI turn
    ai_move()

    if check_winner("O"):
        print()
        print_board()
        print("\nAI wins!")
        break

    if is_draw():
        print()
        print_board()
        print("\nIt's a draw!")
        break