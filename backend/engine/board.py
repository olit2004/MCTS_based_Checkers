import copy

try:
    from .constants import (
        BOARD_SIZE,
        EMPTY,
        WHITE_PIECE,
        BLACK_PIECE,
        WHITE_KING,
        BLACK_KING,
        WHITE_PLAYER,
        BLACK_PLAYER
    )
    from .move import Move
except (ImportError, ValueError):
    from constants import (
        BOARD_SIZE,
        EMPTY,
        WHITE_PIECE,
        BLACK_PIECE,
        WHITE_KING,
        BLACK_KING,
        WHITE_PLAYER,
        BLACK_PLAYER
    )
    from move import Move


class Board:

    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = WHITE_PLAYER

    def initialize_board(self):
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = BLACK_PIECE

        for row in range(5, 8):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = WHITE_PIECE

        return board

    def clone(self):
        return copy.deepcopy(self)

    def print_board(self):
        for row in self.board:
            print(row)

    def is_inside_board(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, value):
        self.board[row][col] = value

    def generate_moves(self, player):
        capture_moves = self.generate_capture_moves(player)

        if capture_moves:
            return capture_moves

        return self.generate_simple_moves(player)

    def generate_simple_moves(self, player):
        moves = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                piece = self.get_piece(row, col)

                if piece == EMPTY:
                    continue

                if piece * player <= 0:
                    continue

                moves.extend(
                    self.get_piece_simple_moves(row, col)
                )

        return moves

    def get_piece_simple_moves(self, row, col):

        piece = self.get_piece(row, col)

        directions = []

        if piece == WHITE_PIECE:
            directions = [(-1, -1), (-1, 1)]

        elif piece == BLACK_PIECE:
            directions = [(1, -1), (1, 1)]

        elif abs(piece) == 2:
            directions = [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1)
            ]

        moves = []

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if not self.is_inside_board(new_row, new_col):
                continue

            if self.get_piece(new_row, new_col) == EMPTY:
                moves.append(
                    Move(
                        start=(row, col),
                        end=(new_row, new_col)
                    )
                )

        return moves

    def generate_capture_moves(self, player):
        return []