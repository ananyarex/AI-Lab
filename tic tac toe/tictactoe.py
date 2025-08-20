def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, is_maximizing):
    if check_winner(board, "X"):
        return 1
    if check_winner(board, "O"):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(best_score, score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe! You are 'O'. Computer is 'X'.")
    print_board(board)

    while True:
        # Human move
        while True:
            try:
                row = int(input("Enter your move row (0-2): "))
                col = int(input("Enter your move col (0-2): "))
                if board[row][col] == " ":
                    board[row][col] = "O"
                    break
                else:
                    print("Cell already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Enter numbers between 0 and 2.")

        print("\nYour move:")
        print_board(board)

        if check_winner(board, "O"):
            print("You win! 🎉")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

        # Computer move
        move = best_move(board)
        if move:
            board[move[0]][move[1]] = "X"
            print("\nComputer's move:")
            print_board(board)

            if check_winner(board, "X"):
                print("Computer wins! 🤖")
                break
            if is_board_full(board):
                print("It's a draw!")
                break
        else:
            print("No moves left!")
            break

play_game()
