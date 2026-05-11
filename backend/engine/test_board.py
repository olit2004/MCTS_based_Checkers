from .game import Game


game = Game()

print("INITIAL STATE")

print(game.get_state())

print("\nLEGAL MOVES")

moves = game.get_legal_moves()

for move in moves:
    print(move)

print("\nMAKE MOVE")
result = game.make_move(
    {
        "from": [5, 0],
        "to": [0, 7],
        "captures": []
    }
)

print(result)

print("\nUPDATED STATE")

print(game.get_state())