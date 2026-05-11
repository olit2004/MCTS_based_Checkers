import math


#  defining the node of our search tree 

class MCTSNode:

    def __init__( self, board, parent=None, move=None):

        self.board = board
        self.parent = parent
        self.move = move
        self.children = []

        self.visits = 0
        self.wins = 0
        self.untried_moves = board.generate_moves(
            board.current_player
        )

    def is_fully_expanded(self):

        return len(self.untried_moves) == 0

    def best_child(self, exploration_weight=1.41):

        best_score = float("-inf")

        best_node = None

        for child in self.children:

            exploitation = child.wins / child.visits

            exploration = math.sqrt(
                math.log(self.visits) / child.visits
            )

            uct_score = (
                exploitation
                +
                exploration_weight * exploration
            )

            if uct_score > best_score:

                best_score = uct_score

                best_node = child

        return best_node
    
    def expand(self):

        move = self.untried_moves.pop()

        new_board = self.board.clone()

        new_board.apply_move(move)

        child_node = MCTSNode(
            board=new_board,
            parent=self,
            move=move
        )

        self.children.append(child_node)

        return child_node
    
    def is_terminal_node(self):

        return self.board.is_terminal()