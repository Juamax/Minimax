import random
import copy 

def crear_tabla(fila_columna):
    tabla = [["*" for _ in range(fila_columna)] for _ in range(fila_columna)]
    return tabla


def mostrar_tabla(tabla):
    for f in tabla:
        print(" ".join(f))


def colocar_personajes(fila_columna, tabla):
    #CREA LAS POSICIONES DEL TABLERO PARA LUEGO PONER AL GATO, RATON Y LA SALIDAD
    posiciones = []
    for f in range(fila_columna):
        for c in range(fila_columna):
            posiciones.append((f, c))
    #RANDOM.CHOISE ELEGI UNA POSICION ALEATORIA DE LA LISTA "POSICIONES"
    posf_gato, posc_gato = random.choice(posiciones)
    posiciones.remove((posf_gato, posc_gato))
    posf_raton, posc_raton = random.choice(posiciones)
    posiciones.remove((posf_raton, posc_raton))
    posf_salidad, posc_salidad = random.choice(posiciones)
    #TABLA[0][0] 
    tabla[posf_gato][posc_gato]= "G"
    tabla[posf_raton][posc_raton]="R"
    tabla[posf_salidad][posc_salidad]= "S"

    return tabla, posf_gato, posc_gato, posf_raton, posc_raton, posf_salidad, posc_salidad


def movimientos_posibles(tabla, movimiento, pos):
    direcciones = {"A": (0,-1), "S": (1,0), "D": (0,1), "W": (-1,0)}
    if movimiento not in direcciones:
        return tabla, pos

    df, dc = direcciones[movimiento] 
    fila, columna = pos 
    nueva_fila = fila + df 
    nueva_columna = columna + dc

    #PARA VERIFICAR QUE NO SALGA DE LA MATRIZ
    if not (0 <= nueva_fila < len(tabla) and 0 <= nueva_columna < len(tabla)):
        return tabla, pos
        
    personaje = tabla[fila][columna] #GUARDA EL PERSONAJE
    destino = tabla[nueva_fila][nueva_columna] #GUARDA EL DESTINO DEL PERSONAJE
    
    if (personaje == "G" and destino == "S"):
        return tabla, pos
        
    tabla[fila][columna] = "*" 
    tabla[nueva_fila][nueva_columna] = personaje 
    return tabla, (nueva_fila, nueva_columna)


def distancia_manhattan(pos1, pos2):
    fila1, col1 = pos1
    fila2, col2 = pos2
    distancia = abs(fila1 - fila2) + abs(col1 - col2)
    return distancia


def evaluar_posicion(pos_gato, pos_raton, pos_salidad):
    #ESTADOS TERMINALES
    if pos_raton == pos_salidad:
        return 1000  #VALOR MAXIMO: EL RATON ESCAPA
    if pos_gato == pos_raton:
        return -1000 #VALOR MINIMO: EL GATO ATRAPA AL RATON
    
    #HEURÍSTICA
    #MAYOR VALOR = GATO LEJOS Y SALIDAD CERCA 
    dist_gato_raton = distancia_manhattan(pos_gato, pos_raton)
    dist_raton_salidad = distancia_manhattan(pos_raton, pos_salidad)

    return dist_gato_raton - dist_raton_salidad


def minimax_alfa_beta(tabla, pos_gato, pos_raton, pos_salidad, profundidad, alfa, beta, es_turno_raton):
    #CASOS EN LO QUE PARA LA FUNCION
    if profundidad == 0 or pos_gato == pos_raton or pos_raton == pos_salidad:
        return evaluar_posicion(pos_gato, pos_raton, pos_salidad), None
    
    direcciones = ["A", "D", "W", "S"]

    if es_turno_raton:
        mejor_valor = float("-inf")
        mejor_movimiento = None
        for mov in direcciones:
            nueva_tabla = copy.deepcopy(tabla)
            nueva_tabla, nueva_pos_raton = movimientos_posibles(nueva_tabla, mov, pos_raton)
            
            valor, _ = minimax_alfa_beta(nueva_tabla, pos_gato, nueva_pos_raton, pos_salidad, profundidad-1, alfa, beta, False)
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
            
            #ACTUALIZACION DE ALFA Y PODA
            alfa = max(alfa, valor)
            if beta <= alfa:
                break #PODA EL GATO NO PERMITIRA ESTE CAMINO
        return mejor_valor, mejor_movimiento
    
    else:
        mejor_valor = float("inf")
        mejor_movimiento = None
        for mov in direcciones:
            nueva_tabla = copy.deepcopy(tabla)
            nueva_tabla, nueva_pos_gato = movimientos_posibles(nueva_tabla, mov, pos_gato)
            if nueva_pos_gato == pos_gato: continue
            
            valor, _ = minimax_alfa_beta(nueva_tabla, nueva_pos_gato, pos_raton, pos_salidad, profundidad-1, alfa, beta, True)
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
            
            #ACTUALIZA BETA Y PODA
            beta = min(beta, valor)
            if beta <= alfa:
                break #PODA EL RATON NO ELIGIRA ESTE CAMINO
        return mejor_valor, mejor_movimiento


def iniciar_partida():
    
    while True:
        try:
            N = int(input("ELIGE UN NUMERO('N' DEBE SER MAYOR A 8) PARA QUE TU TABLERO SEA DE NxN: "))
            if 9 <= N <= 30:
                break
            else:
                print("INGRESE UN NUMERO ENTRE 9 Y 30")
                
        except ValueError:
            print("INGRESE UN NUMERO VALIDO ")
    
    tabla = crear_tabla(N)
    tabla, posf_gato, posc_gato, posf_raton, posc_raton, posf_salidad, posc_salidad = colocar_personajes(N, tabla)
    while True:
        try:
            profundidad = int(input("1-FACIL\n2-MEDIO\n3-DICIFIL\nINGRESE LA DIFICULTAD: "))
            if profundidad == 1:
                break
            elif profundidad ==2:
                profundidad = 3
                break
            elif profundidad == 3:
                profundidad = 5
                break
            else:
                print("OPCION NO VALIDO")
        except ValueError:
            print("OPCION NO VALIDAD") 
   
    turno_raton = True
    contador_movimientos = 0
    limite_movimientos = N * N * 2

    while True:
        contador_movimientos += 1
        print("--------------------------------------------------------")
        mostrar_tabla(tabla)
        print(f"MOVIEMIENTOS POSIBLES: {limite_movimientos} \nMOVIMIENTO NUMERO: {contador_movimientos}")
        if contador_movimientos >= limite_movimientos:
            print("EMPATE: EL RATON Y GATO ESTAN AGOTADOS")
            break
        if (posf_gato, posc_gato) == (posf_raton, posc_raton):
            print("El gato atrapó al ratón")
            break

        if (posf_raton, posc_raton) == (posf_salidad, posc_salidad):
            print("El ratón llegó al salidad ")
            break

        if turno_raton:
            movimiento = input("Movimiento (W,A,S,D): ").upper()

            tabla, nueva_pos = movimientos_posibles(tabla, movimiento, (posf_raton, posc_raton))

            posf_raton, posc_raton = nueva_pos
            turno_raton = False

        else:
            print("Turno del gato (IA)...")

            _, movimiento = minimax_alfa_beta(tabla, (posf_gato, posc_gato), (posf_raton, posc_raton), (posf_salidad, posc_salidad), profundidad,
                float("-inf"), float("inf"), False)

            tabla, nueva_pos = movimientos_posibles(tabla, movimiento, (posf_gato, posc_gato))

            posf_gato, posc_gato = nueva_pos
            turno_raton = True

    
def menu_principal():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Nueva Partida")
        print("2. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            iniciar_partida()
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")
           
menu_principal()

