from hex_board import HexBoard
import math

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)
        

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
class AIPlayer:
    def _init_(self, player_id: int, depth: int = 3):
        super().__init__(player_id)
        self.depth = depth
        
        if player_id == 1: self.enemy_id = 2
        else: self.enemy_id = 1
    
    def play(self, board:HexBoard) -> tuple:
        pass

    # implementacion de minimax
    def minimax(self, player_turn: bool, alpha: float, beta: float, depth: int, board: HexBoard) -> float:
        #caso base: paro si llegue al maximo de profundidad admitido, gana la ia o el oponente
        if depth == 0 or board.check_connection(self.player_id) or board.check_connection(self.enemy_id):
            return self.eval(board)
        
        moves = board.get_possible_moves()

        # lo que haga ahora depende de si en esta simulacion es el turno de la ia o del oponente
        if player_turn:
            # definimos un alpha temporal
            current_alpha = -math.inf
            # recorremos los movimientos disponibles
            for m in moves:
                board_clone = board.clone() # hacemos una copia del tablero                
                row, col = m  # separamos la tupla para trabajar mas comodos
                board.place_piece(row, col, self.player_id) # ponemos ficha en dicho lugar
                
                current_alpha = max(current_alpha, self.minimax(False, alpha, beta, depth-1, board_clone)) # llamado recursivo

                alpha = max( alpha, current_alpha) # nos quedamos con el mayor
                
                if(beta <= alpha): break  #poda alpha beta, si el beta es menor o igual al alpha no tiene sentido seguir explorando
                    
            return current_alpha
        else:
            # lo mismo que en la condicion anterior pero teniendo en cuenta que ahora juega el enemy
            current_beta = math.inf
            for m in moves:
                board_clone = board.clone()
                row, col = m
                board.place_piece(row, col, self.enemy_id)

                current_beta = min(current_beta, self.minimax(True, alpha, beta, depth-1, board_clone))

                beta = min(beta, current_beta)

                if(beta <= alpha): break

            return current_beta
        
        pass

    def eval(self, board: HexBoard):
        pass

    def get_directions():
        pass