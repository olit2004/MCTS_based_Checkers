try:
    from .board import Board
except (ImportError, ValueError):
    from board import Board

board = Board()

board.print_board()