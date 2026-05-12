from ..engine.constants import (
    WHITE_PIECE,
    WHITE_KING,
    BLACK_PIECE,
    BLACK_KING
)
import random



def score_move(board, move):

    score = 0

    start_row, start_col = move.start
    end_row, end_col = move.end

    piece = board.get_piece(start_row, start_col)

    
    score += len(move.captures) * 20

    
    if piece == WHITE_PIECE and end_row == 0:
        score += 15

    elif piece == BLACK_PIECE and end_row == 7:
        score += 15

    
    center_distance = abs(3.5 - end_col)

    score += (4 - center_distance)

   
    if abs(piece) == 2:
        score += 2

    return score


def select_weighted_move(board, legal_moves):

    scored_moves = []

    total_score = 0

    for move in legal_moves:

        score = score_move(board, move)

        # Ensure positive weights
        score = max(score, 1)

        scored_moves.append(
            (move, score)
        )

        total_score += score

    random_value = random.uniform(0, total_score)

    current = 0

    for move, score in scored_moves:

        current += score

        if current >= random_value:
            return move

    return legal_moves[0]