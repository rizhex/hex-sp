# Proyecto de IA: Jugador Hex

## General:
La idea general de la estrategia consiste en identificar:
-Los mejores caminos para ambos jugadores
-Identificar puntos criticos: Intersecciones de los mejores caminos

## Estrategias
Minimax: Se utilizo minimax con poda alfa-beta para recorrer el arbol de adyacencias y asi ir buscando las mejores jugadas. Se evalua con una combinacion de Heuristicas:

-A*: Se utilizo el algoritmo de busqueda A* para identificar los caminos mas cortos de ambos jugadores pues son prioritarios. Como Heuristica se toma la menor distancia entre el nodo actual y alguno de los nodos finales. Se espera de forma general nunca sobreestimar el costo, ya que con la misma probabilidad que pueden haber casillas intermedias del menor camino ocupadas por la IA pueden estar ocupadas por el oponente lo que aumentaria el costo nuevamente(mas que la reduccion de que haya una casilla tomada por la IA). Por tanto se espera por lo general nunca sobreestimar el costo y obtener la mayoria de las veces el mejor camino

-Puntos criticos: Se intersectan estos mejores caminos para identificar puntos que son necesarios para ambos jugadores, y se les da un peso que puede ser positivo o no en dependencia de si lo tomamos nosotros en el futuro que vimos o no, en caso de que no lo hayamos tomado niguno de los dos, tendra peso cero en este futuro estado del tablero

