

def leer_gramatica(ruta_archivo:str) -> dict:
    """
    Lee un archivo de gramática y devuelve un diccionario.
    Estructura: { 'S': [ (('N1', 'N2', ..., 'Ni'), prob), ... ] }
    El valor 'prob' representa la probabilidad, i es para la implementación del algoritmo
    CKY probabilístico. En el caso de que se use CKY determinista, prob = 1 predeterminadamente.
    """
    gramatica = {}
    pcky = False #  flag para comprobar más adelante la coherencia del input
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            #  Eliminamos comentarios y espacios en blanco
            linea = linea.split('#')[0].strip()
            if not linea:  #  Si la línea está vacía, pasamos a la siguiente
                continue
            
            #  Separamos la parte izquierda de la derecha
            izq, der = linea.split('->')
            izq = izq.strip()
            if izq not in gramatica:
                gramatica[izq] = []
            
            # Separamos las producciones
            producciones = der.split('|')
             
            for prod in producciones:
                #  Separamos los símbolos de la producción
                simbolos = prod.strip().split()

                probabilidad = 1.0  # Probabilidad por defecto
                
                #  Si se ha añadido una probabilidad
                if simbolos and simbolos[-1].startswith('[') and simbolos[-1].endswith(']'):
                    prob_str = simbolos.pop()  # Extrae y elimina el elemento de la lista
                    probabilidad = float(prob_str.strip('[]'))
                    pcky = True
                
                #  Finalmente añadimos la tupla al diccionario de la gramática
                gramatica[izq].append((tuple(simbolos), probabilidad))
                
    return gramatica, pcky