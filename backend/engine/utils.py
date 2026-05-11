from .constants import (
    EMPTY,
    WHITE_PIECE,
    WHITE_KING,
    BLACK_PIECE,
    BLACK_KING
)


PIECE_MAP = {
    EMPTY: "empty",
    WHITE_PIECE: "white_piece",
    WHITE_KING: "white_king",
    BLACK_PIECE: "black_piece",
    BLACK_KING: "black_king"
}


def serialize_board(board):

    serialized = []

    for row in board:

        serialized_row = []

        for piece in row:

            serialized_row.append(
                PIECE_MAP[piece]
            )

        serialized.append(serialized_row)

    return serialized