from .board import Board


class Game:

    def __init__(self):

        self.board = Board()
        self.move_history = []
        self.winner = None
        self.game_over = False

    def reset(self):

        self.board = Board()

        self.move_history = []

        self.winner = None

        self.game_over = False

    def get_state(self):

        return {
            "board": self.board.board,
            "current_player": self.board.current_player,
            "winner": self.winner,
            "game_over": self.game_over,
            "move_history": [
                move.to_dict()
                for move in self.move_history
            ]
        }    
    
    def get_legal_moves(self):

        moves = self.board.generate_moves(
            self.board.current_player
        )

        return [
            move.to_dict()
            for move in moves
        ]
    

    
    def is_valid_move(self, move_data):

        legal_moves = self.board.generate_moves(
            self.board.current_player
        )

        for move in legal_moves:

            if (
                move.start == tuple(move_data["from"])
                and
                move.end == tuple(move_data["to"])
                and
                move.captures == move_data.get("captures", [])
            ):
                return move

        return None
    
    def make_move(self, move_data):

        if self.game_over:
            return {
                "success": False,
                "message": "Game is already over"
            }

        validated_move = self.is_valid_move(move_data)

        if not validated_move:
            return {
                "success": False,
                "message": "Illegal move"
            }

        self.board.apply_move(validated_move)

        self.move_history.append(validated_move)

        # Terminal check
        if self.board.is_terminal():

            self.game_over = True

            self.winner = self.board.get_winner()

        return {
            "success": True,
            "state": self.get_state()
        }