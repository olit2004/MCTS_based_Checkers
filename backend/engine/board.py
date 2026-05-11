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

        all_capture_moves = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                piece = self.get_piece(row, col)

                if piece == EMPTY:
                    continue

                if piece * player <= 0:
                    continue

                capture_sequences = self.find_capture_sequences(
                    row,
                    col
                )

                all_capture_moves.extend(capture_sequences)

        return all_capture_moves
    
    def find_capture_sequences(
        self,
        row,
        col,
        visited=None,
        start=None,
        captures=None
    ):

        if visited is None:
            visited = set()

        if captures is None:
            captures = []

        if start is None:
            start = (row, col)

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

        found_capture = False

        all_moves = []

        for dr, dc in directions:

            enemy_row = row + dr
            enemy_col = col + dc

            landing_row = row + (2 * dr)
            landing_col = col + (2 * dc)

            if not self.is_inside_board(landing_row, landing_col):
                continue

            enemy_piece = self.get_piece(enemy_row, enemy_col)

            landing_piece = self.get_piece(landing_row, landing_col)

            if landing_piece != EMPTY:
                continue

            if enemy_piece == EMPTY:
                continue

            
            if enemy_piece * piece > 0:
                continue

            if (enemy_row, enemy_col) in visited:
                continue

            found_capture = True

            # Simulate move
            temp_board = self.clone()

            temp_board.set_piece(row, col, EMPTY)
            temp_board.set_piece(enemy_row, enemy_col, EMPTY)
            temp_board.set_piece(landing_row, landing_col, piece)

            new_visited = visited.copy()
            new_visited.add((enemy_row, enemy_col))

            new_captures = captures + [(enemy_row, enemy_col)]

            future_moves = temp_board.find_capture_sequences(
                landing_row,
                landing_col,
                new_visited,
                start,
                new_captures
            )

            if future_moves:
                all_moves.extend(future_moves)

            else:
                all_moves.append(
                    Move(
                        start=start,
                        end=(landing_row, landing_col),
                        captures=new_captures
                    )
                )

        return all_moves
    
    def apply_move(self, move):

        start_row, start_col = move.start
        end_row, end_col = move.end

        piece = self.get_piece(start_row, start_col)

        
        self.set_piece(start_row, start_col, EMPTY)

        
        self.set_piece(end_row, end_col, piece)

        
        for capture_row, capture_col in move.captures:
            self.set_piece(capture_row, capture_col, EMPTY)

     
        self.promote_if_needed(end_row, end_col)

        
        self.current_player *= -1


    def promote_if_needed(self, row, col):

        piece = self.get_piece(row, col)

        
        if piece == WHITE_PIECE and row == 0:
            self.set_piece(row, col, WHITE_KING)

        
        elif piece == BLACK_PIECE and row == BOARD_SIZE - 1:
            self.set_piece(row, col, BLACK_KING)    


    def get_all_pieces(self, player):

        pieces = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                piece = self.get_piece(row, col)

                if piece * player > 0:
                    pieces.append((row, col))

        return pieces

    def has_moves(self, player):
        return len(self.generate_moves(player)) > 0

  
    def is_terminal(self):

        white_exists = len(self.get_all_pieces(WHITE_PLAYER)) > 0
        black_exists = len(self.get_all_pieces(BLACK_PLAYER)) > 0

        if not white_exists or not black_exists:
            return True

        if not self.has_moves(WHITE_PLAYER):
            return True

        if not self.has_moves(BLACK_PLAYER):
            return True

        return False

    def get_winner(self):

        white_exists = len(self.get_all_pieces(WHITE_PLAYER)) > 0
        black_exists = len(self.get_all_pieces(BLACK_PLAYER)) > 0

        if not white_exists:
            return BLACK_PLAYER

        if not black_exists:
            return WHITE_PLAYER

        if not self.has_moves(WHITE_PLAYER):
            return BLACK_PLAYER

        if not self.has_moves(BLACK_PLAYER):
            return WHITE_PLAYER

        return None
