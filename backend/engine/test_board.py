try:
    from .board import Board
except (ImportError, ValueError):
    from board import Board




EMPTY=0




board = Board()


board.board = [[0 for _ in range(8)] for _ in range(8)]

board.set_piece(0, 1, 1)
print(" the state of the board ")
board.print_board()

print(board.is_terminal()) # state if the game is over or not returns boolean 

print(board.get_winner())  # gives us who the winner is 