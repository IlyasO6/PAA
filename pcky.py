

def invertir_gramatica(gramatica):
    """
    Convierte { 'S': [(('X', 'A'), 1.0)] } 
    en { ('X', 'A'): {'S'} } para búsquedas rápidas en el algoritmo CKY
    """
    gramatica_invertida = {}
    for izq, producciones in gramatica.items():
        for der, prob in producciones: #  ignoramos la probabilidad, pues aqui es inutil
            if der not in gramatica_invertida:
                gramatica_invertida[der] = list()
            gramatica_invertida[der].append((izq, prob))
    return gramatica_invertida

def pcky(gramatica, palabra, simbolo_inicial='S'):
    """
    Implementa el algoritmo CKY para comprobar si una palabra pertenece
    al lenguaje generado por una gramática en CNF.
    """
    N = len(palabra)
    if N == 0:
        return 0.0
        
    gram_inv = invertir_gramatica(gramatica)
    
    #  Inicializamos la tabla CKY
    #  tabla[L][i] = diccionario de No Terminales que generan:  palabra[i : i+L]. con una probabilidad.
    #  donde L = longitud de la ventana sobre la palabra, e i = posicion donde empieza la ventana
    tabla = [[dict() for _ in range(N)] for _ in range(N + 1)]
    
    #  Llenamos la base (L = 1) con reglas del tipo NT -> terminal
    for i in range(N):
        letra = (palabra[i],) #  La convertimos a tupla ('a',) para buscar en el diccionario invertido
        if letra in gram_inv:
            for izq, prob in gram_inv[letra]:
                prob_actual = tabla[1][i].get(izq, 0.0)
                tabla[1][i][izq] = max(prob_actual, prob)
                
    #  Creamos el resto de niveles (1 < L < N+1) con reglas del tipo A -> BC
    for L in range(2, N + 1):
        for i in range(N - L + 1):
            for k in range(1, L):
                
                #  Recuperamos los los diccionarios izquierdo y derecho
                dict_izq = tabla[k][i]
                dict_der = tabla[L - k][i + k]
                
                #  Probamos a unir cada elemento de la izquierda con cada de la derecha
                for B, prob_B in dict_izq.items():
                    for C, prob_C in dict_der.items():
                        posible_der = (B, C)
                        
                        #  Si la combinación B C está en la gramática, añadimos su generador A
                        if posible_der in gram_inv:
                            for A, prob_regla in gram_inv[posible_der]:
                                #  Calculamos la probabilidad combinada
                                prob_nueva = prob_B * prob_C * prob_regla
                                
                                #  Actualizamos la celda quedándonos con el máximo
                                prob_actual = tabla[L][i].get(A, 0.0)
                                tabla[L][i][A] = max(prob_actual, prob_nueva)

    #  Miramos la celda que representa la palabra entera (L=N) 
    #  y devolvemos la probabilidad si contiene el simbolo inicial, y 0.0 si no
    return tabla[N][0].get(simbolo_inicial, 0.0)