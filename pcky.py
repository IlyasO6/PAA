
from utils.grammar_parser import leer_gramatica
def invertir_gramatica(gramatica):
    """
    Invierte el diccionario de la gramatica.
    ej:
    { 'S': [(('X', 'A'), 0.8)] } -> { ('X', 'A'): [('S', 0.8)] } 
    """
    gramatica_invertida = {}
    for izq, producciones in gramatica.items():
        for der, prob in producciones:
            if der not in gramatica_invertida:
                gramatica_invertida[der] = list()
            gramatica_invertida[der].append((izq, prob))
    return gramatica_invertida

def pcky(gramatica, palabra, simbolo_inicial='S'):
    """
    Implementa el algoritmo PCKY para comprobar la probabilidad de que una palabra pertenezca
    al lenguaje generado por una gramática en PCNF.
    """
    N = len(palabra)
    if N == 0:
        return 0.0
        
    gram_inv = invertir_gramatica(gramatica)

    #  Inicializamos la tabla PCKY
    #  tabla[L][i] = diccionario de No Terminales que generan:  palabra[i : i+L]. con una probabilidad y un puntero para crear
    #  el árbol sintáctico
    #  donde L = longitud de la ventana sobre la palabra, e i = posicion donde empieza la ventana
    tabla = [[dict() for _ in range(N)] for _ in range(N + 1)]
    
    #  Llenamos la base (L = 1) con reglas del tipo NT -> terminal
    for i in range(N):
        letra = (palabra[i],) #  La convertimos a tupla ('a',) para buscar en el diccionario invertido
        if letra in gram_inv:
            for izq, prob in gram_inv[letra]:
                prob_actual = tabla[1][i].get(izq, (0.0, None))[0]
                if prob > prob_actual:
                    tabla[1][i][izq] = (prob, (izq, palabra[i]))
                
    #  Creamos el resto de niveles (1 < L < N+1) con reglas del tipo A -> BC
    for L in range(2, N + 1):
        for i in range(N - L + 1):
            for k in range(1, L):
                
                #  Recuperamos los los diccionarios izquierdo y derecho
                dict_izq = tabla[k][i]
                dict_der = tabla[L - k][i + k]
                
                #  Probamos a unir cada elemento de la izquierda con cada de la derecha
                for B, (prob_B, arbol_B) in dict_izq.items():
                    for C, (prob_C, arbol_C) in dict_der.items():
                        posible_der = (B, C)
                        
                        #  Si la combinación B C está en la gramática, añadimos su generador A
                        if posible_der in gram_inv:
                            for A, prob_regla in gram_inv[posible_der]:
                                #  Calculamos la probabilidad combinada
                                prob_nueva = prob_B * prob_C * prob_regla
                                
                                #  Actualizamos la celda quedándonos con el máximo
                                prob_actual = tabla[L][i].get(A, (0.0, None))[0]
                                if prob_nueva > prob_actual:
                                    tabla[L][i][A] = (prob_nueva, (A, arbol_B, arbol_C))

    #  Miramos la celda que representa la palabra entera (L=N) 
    #  y devolvemos la probabilidad si contiene el simbolo inicial, y 0.0 si no
    return tabla[N][0].get(simbolo_inicial, (0.0, None))