from hex_board import HexBoard

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
class AIPlayer:
    def _init_(self, player_id: int):
        self.player_id = player_id
    
    def play(self, board:HexBoard) -> tuple:
        pass

    def minimax(aiplayer_turn: bool):
        pass

    def eval_board():
        pass

    def get_directions():
        pass