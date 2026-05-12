from .heuristics import select_weighted_move


def rollout(board):

    rollout_board = board.clone()

    MAX_ROLLOUT_DEPTH = 80

    depth = 0

    while (
        not rollout_board.is_terminal()
        and
        depth < MAX_ROLLOUT_DEPTH
    ):

        legal_moves = rollout_board.generate_moves(
            rollout_board.current_player
        )

        if not legal_moves:
            break

        move = select_weighted_move(
            rollout_board,
            legal_moves
        )

        rollout_board.apply_move(move)

        depth += 1

    return rollout_board.get_winner()