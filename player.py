from hex_board import HexBoard
import math
import heapq

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)
        

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
class AIPlayer:
    def _init_(self, player_id: int, depth: int = 3):
        self.player_id = player_id
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
        
    # implementacion de la evaluacion del tablero
    def eval(self, board: HexBoard):
        # verificamos conexiones completas, de la ia o del enemy, cualquiera de las 2 es un return automatico
        if board.check_connection(self.player_id): return math.inf
        if board.check_connection(self.enemy_id): return -math.inf

        #iaplayer_score = # combinacion lineal de intrigas( condiciones, bloqueos, etc) todas positivas
        #enemy_score = # misma intriga

        #return iaplayer_score - enemy_score 
        pass
    
    def path_score(self, board: HexBoard, for_player: int) -> float:
        
        
        pass
    
    # implementacion de a star para encontrar caminos de costo minimo
    def a_star_init(self, board: HexBoard, for_player: int) -> float: 
        pair_dir = self.get_directions(True) # direcciones para filas par
        odd_dir = self.get_directions(False) # direcciones para filas impares
        
                   

        pass
    def a_star(self, board:HexBoard, for_player: int, tracking_taken_tiles: list, pair_dir, odd_dir) -> float:
        # determinar si vamos hor o vert
        if for_player == 1:
            start = [] # lista de los nodos de inicio
            for i in range (board.size):
                tile_val = board.board[i][0]
                if tile_val == for_player or tile_val == 0:
                    start[i] = tile_val #le asignamos el valor inicial
                    if tile_val == for_player: tracking_taken_tiles[i] = tracking_taken_tiles[i]+1  
        else:
            start = []
            for i in range (board.size):
                if board.board[0][i] == for_player:
                    start.append([0,i]) 
        pass
    

    
    # implementacion para obtener un estimado de cuanto falta para completar el camino de costo minimo
    def get_a_star_heuristic() -> float:
        pass
    # implementacion para obtener los vecinos disponibles de un nodo en especifico
    def get_neighbor(self, board: HexBoard, row: int, col: int, enemy: int) -> list:
        neighbors = [] # aqui guardamos los vecinos del nodo en que estemos
        board_size_odd = board.size%2 # obtenemos la paridad del tamano del tablero para saber si el la ultima fila es par o impar

        if row%2 == 0: 
            pair_dir = self.get_directions(True)

            for p in pair_dir:
                prow, pcol = p
                
                if row == 0 and prow == -1: continue # a partir de aqui se ignoran salidas de limites
                if col == 0 and pcol == -1: continue 
                if col == board.size-1 and pcol == 1: continue
                if not board_size_odd and row == board.size-1 and prow == 1: continue
                
                neighbors.append(board.board[row + prow][col + pcol]) # agregamos el vecino para su posible recorrido
        else:
            # lo mismo pero para filas impares
            odd_dir = self.get_directions(False)

            for o in odd_dir:
                orow, ocol = o
                
                if col == 0 and ocol == -1: continue
                if col == board.size-1 and ocol == 1: continue
                if board_size_odd and row == board.size-1 and orow == 1: continue

                neighbors.append(board.board[row+orow][col+ocol])
        
        return neighbors

    # implementacion para determinar cuanto cuesta moverse a una determinada casilla
    def get_cost(self, board:HexBoard, row:int, col:int, for_player: int)-> int:
        
        if board.board[row][col] == for_player: return 0 # si ya esta controlada por el jugador el costo es 0
        if board.board[row][col] == 0: return 1 # si no esta controlada por ninguno el costo es 1
        
        return -1 # si esta controlada por el oponente no se puede tomar este camino: el costo es negativo

    # direcciones apropiadas segun la docu para even-r
    def get_directions(self, parity: bool):
        
            #impares
        if not parity:
            return [
                (0, -1),   # izq
                (0, 1),    # der
                (-1, 0),    # arriba
                (1, 0),     # abajo
                (-1, -1),   # arriba-izq
                (1, -1)     # abajo-izq
            ]
        # pares
        else: 
            return [
                (0, -1),   # izq
                (0, 1),    # der
                (-1, 0),    # arrib
                (1, 0),     # abaj
                (-1, 1),    # arrib-der
                (1, 1)      # abaj-der
            ]
        