from hex_board import HexBoard
import math
import heapq

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)
        

    def play(self, board: HexBoard) -> tuple:
        moves = board.get_possible_moves()
        return moves[0]
    
class AIPlayer:
    def __init__(self, player_id: int, depth: int = 2, not_checked = True):
        self.player_id = player_id
        self.depth = depth
        self.not_checked = not_checked
        
        if player_id == 1: self.enemy_id = 2
        else: self.enemy_id = 1
        print(f"soy ia soy player {player_id}")
    def play(self, board:HexBoard) -> tuple:
        
        if self.not_checked:
            self.not_checked = False
            if self.is_empty_board(board): 
                return self.first_move(board)
                
        
        best_move = [0,0]
        best_move_eval = -math.inf
        first = True

        for move in board.get_possible_moves():
            if first:
                board_clone = board.clone()
                best_move = move
                board_clone.place_piece(best_move[0], best_move[1], self.player_id)
                best_move_eval = self.minimax(False, -math.inf, math.inf, self.depth, board_clone)
                first = False
                continue
            board_clone = board.clone()
            row, col = move
            board_clone.place_piece(row, col, self.player_id)
            move_eval = self.minimax(False, -math.inf, math.inf, self.depth, board_clone)
          
            if best_move_eval < move_eval:
                best_move = move
                best_move_eval = move_eval

        print(f"soy ia jugue en {best_move}")
        return best_move
    
    def is_empty_board(self, board: HexBoard):
        
        for row in board.board:
            for cell in row:
                if cell != 0: return False
            
        return True

            

    def first_move(self, board: HexBoard):

        center_q = len(board.board) // 2
        center_r = len(board.board) // 2
        return (center_q, center_r)
    
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
                row, col = m  
                board_clone.place_piece(row, col, self.player_id) # ponemos ficha en dicho lugar
                
                current_alpha = max(current_alpha, self.minimax(False, alpha, beta, depth-1, board_clone)) # llamado recursivo

                alpha = max(alpha, current_alpha) # nos quedamos con el mayor
                
                if(beta <= alpha): break  #poda alpha beta, si el beta es menor o igual al alpha no tiene sentido seguir explorando
                    
            return current_alpha
        else:
            # lo mismo que en la condicion anterior pero teniendo en cuenta que ahora juega el enemy
            current_beta = math.inf
            for m in moves:
                board_clone = board.clone()
                row, col = m
                board_clone.place_piece(row, col, self.enemy_id)

                current_beta = min(current_beta, self.minimax(True, alpha, beta, depth-1, board_clone))

                beta = min(beta, current_beta)

                if(beta <= alpha): break

            return current_beta
        
    # implementacion de la evaluacion del tablero
    def eval(self, board: HexBoard):
        # verificamos conexiones completas, de la ia o del enemy, cualquiera de las 2 es un return automatico
        if board.check_connection(self.player_id): return math.inf
        if board.check_connection(self.enemy_id): return -math.inf
        
        iap_a_star_score, iap_a_star_path = self.a_star_init(board, self.player_id)
        en_a_star_score, en_a_star_path = self.a_star_init(board, self.enemy_id)
        
        critical_point_score = self.eval_critical_point(board, iap_a_star_path, en_a_star_path)
        iaplayer_score = iap_a_star_score + critical_point_score
        
        # combinacion lineal de intrigas( condiciones, bloqueos, etc) todas positivas
        enemy_score = en_a_star_score # misma intriga

        return iaplayer_score - enemy_score 

    def eval_critical_point(self, board: HexBoard, ia_path: list, enemy_path: list) -> float:
        for ia_node in ia_path:
            if ia_node in enemy_path:
                row, col = ia_node
                if board.board[row][col] == self.player_id: return board.size / 3
                elif board.board[row][col] == self.enemy_id: return -(board.size / 3)
        return 0
        
    # implementacion de a star para encontrar caminos de costo minimo
    def a_star_init(self, board: HexBoard, for_player: int) -> tuple[float, list]: 
        start = [] # lista de los nodos de inicio
        end = [] # lista para almacenar los nodos objetivos

        # determinar si vamos hor o vert
        if for_player == 1:
            for i in range (board.size): 
                    if board.board[i][0] == 2: continue # si la casilla esta tomada por el oponente se ignora
                    start.append((i, 0))  # almacenamos los nodos inciales
                    end.append((i, board.size-1)) # almacenamos los nodos finales
        else:
            start = []
            for i in range (board.size):
                        start.append((0, i))
                        end.append((board.size-1, i)) 
            
        best = self.a_star(board, for_player, start, end)
        best_sc, best_p = best
        return board.size-best_sc, best_p         

    def a_star(self, board:HexBoard, for_player: int, start: list, end: list) -> tuple[float, list]:
        
        open_set = [] # nodos iniciales
        g_score = {} # costos reales desde el inicio
        f_score = {} # costos estimado, (g + h) h: self.hex_distance
        came_from = {} # para recoonstruir el camino
        for node_s in start:
            r, c = node_s
            g_score[node_s] = self.get_cost(board, r, c, for_player) # guardamos el coste del nodo inicial
            came_from[node_s] = None
            # encontramos el valor minimo necesario para llegar al otro lado: linea recta, osea el nodo directamente opuesto
            if for_player == 1: min_h = self.hex_distance(node_s, (r, board.size-1))
            else: min_h = self.hex_distance(node_s, (board.size-1, c))

            f_score[node_s] = g_score[node_s] + min_h # guardamos el costo estimado: costo real(g) + costo faltante estimado(h)
            heapq.heappush(open_set, (f_score[node_s], node_s)) # almacenamos el costo estimado con su respectivo nodo en el heap
        
        open_set_hash = set(start) # para poder verificar elementos en open_set mas eficientemente

        while open_set:
            current = heapq.heappop(open_set)[1] # sacamos un el nodo con mejor estimado
            open_set_hash.remove(current) # lo sacamos del hash

            # si llegamos al final devolvemos el costo del camino
            if current in end:  
                path = []
                score_f = g_score[current]
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return (score_f, path)
            
            r, c = current 
            # recorremos todos los vecinos de este nodo
            for neighbor in self.get_neighbor(board, r, c, for_player):
                nr, nc = neighbor
                
                temp_cost =  self.get_cost(board, nr, nc, for_player)
                if temp_cost == -1: continue # si el vecino esta ocupado por el enemigo nos lo saltamos
                current_neighbor_cost = g_score[current] + temp_cost # obetenemos el costo de movernos hacia aqui para el jugador
                
                # verificamos si el nodo es nuevo, o si no es nuevo si llegamos a el con un menor costo(mejor camino)
                if (neighbor not in g_score) or g_score[neighbor] > current_neighbor_cost: 
                    came_from[neighbor] = current # le asociamos de donde vino en el mejor camino
                    g_score[neighbor] = current_neighbor_cost # en caso de que si: actualizamos su costo

                    # estimamos cuanto falta hasta un nodo objetivo usando nuestra heuristica dependiendo del jugador
                    # o sea si vamos left-rigth, top-bottom
                    if for_player == 1: min_h = self.hex_distance(neighbor, (nr, board.size-1))
                    else: min_h = self.hex_distance(neighbor, (board.size-1, nc))

                    f_score[neighbor] = current_neighbor_cost + min_h # estimacion del costo total del camino

                    # lo agregamos al open_set
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        # en caso de no encontrar ningun camino significa que el jugador perdio: puntuacion -infinito
        return -math.inf, []
    
    # implementacion para obtener un estimado de cuanto falta para completar el camino de costo minimo
    def hex_distance(self, p1: tuple[int,int], p2: tuple[int,int]):
        # convertimos a coordenadas axiales ambos puntos
        q1,r1 = self.offset_to_axial(p1) 
        q2,r2 = self.offset_to_axial(p2)

        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2

    # implementacion para obtener los vecinos disponibles de un nodo en especifico
    def get_neighbor(self, board: HexBoard, row: int, col: int, for_player: int) -> list:
        neighbors = [] # aqui guardamos los vecinos del nodo en que estemos

        for dir in self.get_directions():
            drow, dcol = dir
            if row == 0 and drow == -1: continue
            if col == 0 and dcol == -1: continue
            if row == board.size-1 and drow == 1: continue
            if col == board.size-1 and dcol == 1: continue

            neighbors.append((row + drow, col + dcol)) # agregamos el vecino para su posible recorrido + el costo del mismo
        
        return neighbors

    # implementacion para determinar cuanto cuesta moverse a una determinada casilla
    def get_cost(self, board:HexBoard, row:int, col:int, for_player: int)-> float:
        
        if board.board[row][col] == for_player: return 0 # si ya esta controlada por el jugador el costo es 0
        if board.board[row][col] == 0: return 1 # si no esta controlada por ninguno el costo es 1
        
        return -1 # si esta controlada por el oponente no se puede tomar este camino: el costo es negativo
    
    # implementacion para convertir a coordenadas axiales
    def offset_to_axial(self, p: tuple[int,int]):
        row, col = p
        q = col - (row // 2)  # Para even-r
        r = row
        return (q, r)

    # direcciones apropiadas segun la docu para even-r
    def get_directions(self):
        
            return [
                (0, -1),   # izq
                (0, 1),    # der
                (-1, 0),    # arriba
                (1, 0),     # abajo
                (-1, 1),   # arriba-derecha
                (1, -1)     # abajo-izq
            ]
    
        