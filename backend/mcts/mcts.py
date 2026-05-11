from .node import MCTSNode
from .rollout import rollout


class MCTS:

    def __init__(self, iterations=1000):

        self.iterations = iterations

    def search(self, initial_board):

        root = MCTSNode(initial_board)

        root_player = initial_board.current_player

        for _ in range(self.iterations):

            node = root

            # SELECTION
            while (
                not node.is_terminal_node()
                and
                node.is_fully_expanded()
            ):

                node = node.best_child()

            # EXPANSION
            if (
                not node.is_terminal_node()
                and
                not node.is_fully_expanded()
            ):

                node = node.expand()

            # SIMULATION
            winner = rollout(node.board)

            # BACKPROPAGATION
            self.backpropagate(
                node,
                winner,
                root_player
            )

        return root.best_child(exploration_weight=0)

    def backpropagate(
        self,
        node,
        winner,
        root_player
    ):

        while node is not None:

            node.visits += 1

            if winner == root_player:
                node.wins += 1

            node = node.parent