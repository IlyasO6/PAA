
from utils.grammar_parser import leer_gramatica
def invertir_gramatica(gramatica):
    """
    Invierte el diccionario de la gramatica y elimina las probabilidades.
    ej:
    { 'S': [(('X', 'A'), 1.0)] } -> { ('X', 'A'): {'S'} }
    """
    gramatica_invertida = {}
    for izq, producciones in gramatica.items():
        for der, _ in producciones:
            if der not in gramatica_invertida:
                gramatica_invertida[der] = set()
            gramatica_invertida[der].add(izq)
    return gramatica_invertida

def cky(gramatica, palabra, simbolo_inicial='S'):
    """
    Implementa el algoritmo CKY para comprobar si una palabra pertenece
    al lenguaje generado por una gramática en CNF.
    """
    N = len(palabra)
    if N == 0:
        return False
        
    gram_inv = invertir_gramatica(gramatica)
    
    #  Inicializamos la tabla CKY
    #  tabla[L][i] = conjunto de No Terminales que generan:  palabra[i : i+L]
    #  donde L = longitud de la ventana sobre la palabra, e i = posicion donde empieza la ventana
    tabla = [[set() for _ in range(N)] for _ in range(N + 1)]
    
    #  llenamos la base (L = 1) con reglas del tipo NT -> terminal
    for i in range(N):
        letra = (palabra[i],) #  la convertimos a tupla ('a',) para buscar en el diccionario invertido
        if letra in gram_inv:
            for izq in gram_inv[letra]:
                tabla[1][i].add(izq)
                
    #  creamos el resto de niveles (1 < L < N+1) con reglas del tipo A -> BC
    for L in range(2, N + 1):
        for i in range(N - L + 1):
            for k in range(1, L):
                
                #  recuperamos los conjuntos las partes izquierda y derecha
                conjunto_izq = tabla[k][i]
                conjunto_der = tabla[L - k][i + k]
                
                #  probamos a unir cada elemento de la izquierda con cada uno de la derecha
                for B in conjunto_izq:
                    for C in conjunto_der:
                        posible_der = (B, C)
                        
                        #   si la combinación B C está en la gramática, añadimos su generador A
                        if posible_der in gram_inv:
                            for A in gram_inv[posible_der]:
                                tabla[L][i].add(A)

    #  Miramos la celda que representa la palabra entera (L=N) 
    #  y devolvemos True si contiene el simbolo inicial, y False si no
    return simbolo_inicial in tabla[N][0]
