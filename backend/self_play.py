from .engine.board import Board
from .mcts.mcts import MCTS


def print_separator():

    print("\n" + "=" * 50 + "\n")


def main():

    board = Board()

    move_count = 0

    MAX_MOVES = 200

    while not board.is_terminal():

        print_separator()

        print(f"MOVE: {move_count}")

        print(
            "CURRENT PLAYER:",
            "WHITE"
            if board.current_player == 1
            else "BLACK"
        )

        board.print_board()

        mcts = MCTS(iterations=1000)

        best_node = mcts.search(board)

        if best_node is None:

            print("NO VALID MOVE FOUND")

            break

        move = best_node.move

        print("\nSELECTED MOVE:")

        print(move.to_dict())

        board.apply_move(move)

        move_count += 1

        if move_count >= MAX_MOVES:

            print("\nMAX MOVES REACHED")

            break

    print_separator()

    print("FINAL BOARD:")

    board.print_board()

    print("\nGAME OVER")

    winner = board.get_winner()

    if winner == 1:

        print("WINNER: WHITE")

    elif winner == -1:

        print("WINNER: BLACK")

    elif winner == 0:

        print("DRAW")

    else:

        print("UNKNOWN RESULT")    

    



if __name__ == "__main__":

    main()