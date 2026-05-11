from ..engine.board import Board
from .mcts import MCTS

board = Board()

mcts = MCTS(iterations=500)

best_node = mcts.search(board)

print("BEST MOVE:")

print(best_node.move.to_dict())

print()

print("VISITS:", best_node.visits)

print("WINS:", best_node.wins)