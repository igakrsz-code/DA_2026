def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
    print("\n")
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---|---|---")
    print("\n")


def player_input(player, board):
    while True:
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter column (0-2): "))
            if row in range(3) and col in range(3):
                if board[row][col] == " ":
                    return row, col
                else:
                    print("This cell is already taken. Try again.")
            else:
                print("Invalid input. Row and column must be 0, 1, or 2.")
        except ValueError:
            print("Invalid input. Please enter numbers.")


def check_win(board, player):

    for row in board:
        if all(cell == player for cell in row):
            return True
 
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
  
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False


def check_tie(board):
    for row in board:
        if " " in row:
            return False
    return True


def play():
    board = create_board()
    current_player = "X"
    while True:
        display_board(board)
        row, col = player_input(current_player, board)
        board[row][col] = current_player

        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_tie(board):
            display_board(board)
            print("It's a tie!")
            break

    
        current_player = "O" if current_player == "X" else "X"


play()
