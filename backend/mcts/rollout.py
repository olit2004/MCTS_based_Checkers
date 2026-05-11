import random


def rollout(board):

    rollout_board = board.clone()

    while not rollout_board.is_terminal():

        legal_moves = rollout_board.generate_moves(
            rollout_board.current_player
        )

        if not legal_moves:
            break

        move = random.choice(legal_moves)

        rollout_board.apply_move(move)

    return rollout_board.get_winner()