from fastapi import APIRouter

from ..engine.game import Game
from backend.api.schemas import MoveRequest

router = APIRouter()

game = Game()

@router.get("/game/state")
def get_game_state():

    return game.get_state()


@router.get("/game/legal-moves")
def get_legal_moves():

    return {
        "moves": game.get_legal_moves()
    }

@router.post("/game/move")
def make_move(move: MoveRequest):

    move_data = {
        "from": move.from_pos,
        "to": move.to_pos,
        "captures": move.captures
    }

    result = game.make_move(move_data)

    return result

@router.post("/game/new")
def new_game():

    game.reset()

    return {
        "message": "New game started",
        "state": game.get_state()
    }