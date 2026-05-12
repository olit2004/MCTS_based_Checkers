from fastapi import APIRouter, HTTPException
import uuid

from ..engine.game import Game
from .schemas import MoveRequest
from ..mcts.mcts import MCTS

router = APIRouter()


games = {}


def get_game_or_404(game_id: str):

    game = games.get(game_id)

    if not game:

        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


@router.post("/game/new")
def new_game():

    game_id = str(uuid.uuid4())

    game = Game()

    games[game_id] = game

    return {
        "game_id": game_id,
        "state": game.get_state()
    }


@router.get("/game/{game_id}/state")
def get_game_state(game_id: str):

    game = get_game_or_404(game_id)

    return game.get_state()


@router.get("/game/{game_id}/legal-moves")
def get_legal_moves(game_id: str):

    game = get_game_or_404(game_id)

    return {
        "moves": game.get_legal_moves()
    }


@router.post("/game/{game_id}/move")
def make_move(game_id: str, move: MoveRequest):

    game = get_game_or_404(game_id)

    move_data = {
        "from": move.from_pos,
        "to": move.to_pos,
        "captures": move.captures
    }

    result = game.make_move(move_data)

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@router.get("/game/{game_id}/history")
def get_move_history(game_id: str):

    game = get_game_or_404(game_id)

    return {
        "history": [
            move.to_dict()
            for move in game.move_history
        ]
    }


@router.post("/game/{game_id}/ai-move")
def ai_move(game_id: str):

    game = get_game_or_404(game_id)

    if game.game_over:

        raise HTTPException(
            status_code=400,
            detail="Game is already over"
        )

    # Search for best move using MCTS
    mcts = MCTS(iterations=800)

    best_node = mcts.search(game.board)

    if best_node is None:

        raise HTTPException(
            status_code=500,
            detail="AI failed to find a move"
        )

    move = best_node.move

    move_data = {
        "from": move.start,
        "to": move.end,
        "captures": move.captures
    }

    result = game.make_move(move_data)

    return result