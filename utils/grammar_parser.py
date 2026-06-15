

def leer_gramatica(ruta_archivo:str) -> dict:
    """
    Lee un archivo de gramática y devuelve un diccionario.
    Estructura: { 'S': [ (('N1', 'N2', ..., 'Ni'), prob), ... ] }
    El valor 'prob' representa la probabilidad, y es para la implementación del algoritmo
    CKY probabilístico. En el caso de que se use CKY determinista, prob = 1 predeterminadamente.
    """
    gramatica = {}
    pcky = False #  flag para comprobar más adelante la coherencia del input
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            #  eliminamos comentarios y espacios en blanco
            linea = linea.split('#')[0].strip()
            if not linea:  #  si la línea está vacía, pasamos a la siguiente
                continue
            
            #  separamos la parte izquierda de la derecha
            izq, der = linea.split('->')
            izq = izq.strip()
            if izq not in gramatica:
                gramatica[izq] = []
            
            #  separamos las producciones
            producciones = der.split('|')
             
            for prod in producciones:
                #  separamos los símbolos de la producción
                simbolos = prod.strip().split()

                probabilidad = 1.0  #  En caso de que no sea una PCFG, la probabilidad será 1, escogido arbitrariamente, 
                                    #  ya que más adelante se eliminan las probabilidades de la gramatica si se usa CKY. 
                
                #  si la gramatica contiene probabilidades:
                if simbolos and simbolos[-1].startswith('[') and simbolos[-1].endswith(']'):
                    prob_str = simbolos.pop()
                    probabilidad = float(prob_str.strip('[]'))
                    pcky = True
                
                #  finalmente añadimos la tupla al diccionario de la gramática
                gramatica[izq].append((tuple(simbolos), probabilidad))
    
    return gramatica, pcky