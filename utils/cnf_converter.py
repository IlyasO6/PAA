


def es_cnf(gramatica):
    """
    Comprueba si una gramática está estrictamente en Forma Normal de Chomsky.
    """
    for producciones in gramatica.values():
        for der, _ in producciones:
            #  regla A -> a
            if len(der) == 1 and der[0].islower():
                continue
            #  regla A -> BC 
            elif len(der) == 2 and not der[0].islower() and not der[1].islower():
                continue
            #  si no es ninguna de las dos, no está en CNF
            else:
                return False
    return True


def crear_nuevo_simbolo_inicial(gramatica, inicial_antiguo='S'):
    g = gramatica.copy()
    nuevo_inicial = inicial_antiguo + "0"
    g[nuevo_inicial] = [((inicial_antiguo,), 1.0)]
    return g, nuevo_inicial

def es_terminal(simbolo):
    return simbolo.islower()

def aislar_terminales(gramatica):
    g_nueva = {}
    nuevas_reglas_terminales = {}
    
    for izq, producciones in gramatica.items():
        g_nueva[izq] = []
        for der, prob in producciones:
            #  solo nos importan reglas con más de 1 símbolo (ej. A -> a B)
            if len(der) > 1:
                nuevo_der = []
                for sim in der:
                    if es_terminal(sim):
                        nuevo_nt = f"T_{sim}"
                        #  guardamos la regla T_a -> a (con prob 1.0)
                        nuevas_reglas_terminales[nuevo_nt] = [((sim,), 1.0)]
                        nuevo_der.append(nuevo_nt)
                    else:
                        nuevo_der.append(sim)
                g_nueva[izq].append((tuple(nuevo_der), prob))
            else:
                #  si es longitud 1 o vacía, se queda igual
                g_nueva[izq].append((der, prob))
                
    #  añadimos las nuevas reglas al diccionario principal
    for nt, prod in nuevas_reglas_terminales.items():
        if nt not in g_nueva:
            g_nueva[nt] = prod
            
    return g_nueva


def binarizar(gramatica):
    """ Binariza producciones n-arias. """
    g_nueva = {}
    contador = 1 #  para la creación de NTs: X_1, X_2...
    
    for izq, producciones in gramatica.items():
        g_nueva[izq] = []
        for der, prob in producciones:
            if len(der) > 2:
                #  binarización en cascada
                simbolo_actual = izq
                
                #  iteramos hasta el penúltimo símbolo
                for i in range(len(der) - 2):
                    nuevo_nt = f"X_{contador}"
                    contador += 1
                    
                    if simbolo_actual not in g_nueva:
                        g_nueva[simbolo_actual] = []
                    
                    #  la probabilidad original se queda en la primera división.
                    #  las divisiones artificiales posteriores tienen prob 1.0
                    p = prob if i == 0 else 1.0
                    g_nueva[simbolo_actual].append(((der[i], nuevo_nt), p))
                    
                    simbolo_actual = nuevo_nt
                    
                #  el último eslabon de la cascada se queda con los 2 últimos simbolos
                if simbolo_actual not in g_nueva:
                    g_nueva[simbolo_actual] = []
                g_nueva[simbolo_actual].append(((der[-2], der[-1]), 1.0))
            else:
                g_nueva[izq].append((der, prob))
                
    return g_nueva

def eliminar_vacios(gramatica):
    #  encontramos símbolos anulables (que pueden derivar en el carácter vacio)
    anulables = set()
    for izq, producciones in gramatica.items():
        for der, prob in producciones:
            if der == ('e',):
                anulables.add(izq)
                
    #  si A -> BC y tanto B como C son anulables, A también lo es
    cambio = True
    while cambio:
        cambio = False
        for izq, producciones in gramatica.items():
            if izq not in anulables:
                for der, prob in producciones:
                    if len(der) == 2 and der[0] in anulables and der[1] in anulables:
                        anulables.add(izq)
                        cambio = True
                        
    #  construimos la nueva gramática sin carácteres vacios y con las reglas compensatorias
    g_nueva = {}
    for izq, producciones in gramatica.items():
        g_nueva[izq] = []
        for der, prob in producciones:
            if der == ('e',):
                continue
                
            g_nueva[izq].append((der, prob))
            
            #  si es una regla binaria, comprobamos si alguna parte es anulable
            if len(der) == 2:
                B, C = der
                if B in anulables:
                    g_nueva[izq].append(((C,), prob)) # A -> C
                if C in anulables:
                    g_nueva[izq].append(((B,), prob)) # A -> B

    #  limpiamos posibles duplicados (convirtiendo a set y luego a lista)
    for izq in g_nueva:
        g_nueva[izq] = list(set(g_nueva[izq]))
        
    return g_nueva

def eliminar_unitarias(gramatica):
    alcanzables = {nt: set([nt]) for nt in gramatica}
    
    #  encontramos las conexiones directas (A -> B)
    for izq, producciones in gramatica.items():
        for der, prob in producciones:
            if len(der) == 1 and not es_terminal(der[0]):
                alcanzables[izq].add(der[0])
                
    #  aplicamos la propiedad transitiva
    cambio = True
    while cambio:
        cambio = False
        for A in alcanzables:
            elementos_actuales = list(alcanzables[A])
            for B in elementos_actuales:
                if B in alcanzables:
                    for C in alcanzables[B]:
                        if C not in alcanzables[A]:
                            alcanzables[A].add(C)
                            cambio = True
                            
    #  construimos la gramática final
    g_nueva = {}
    for A in gramatica:
        g_nueva[A] = set()
        for B in alcanzables[A]:
            if B in gramatica:
                for der, prob in gramatica[B]:
                    if len(der) != 1 or es_terminal(der[0]):
                        g_nueva[A].add((der, prob))
                        
    #  convertimos los sets de vuelta a listas y eliminamos claves vacías
    g_final = {}
    for k, v in g_nueva.items():
        if v: #  si la lista no está vacía
            g_final[k] = list(v)
            
    return g_final

def eliminar_inalcanzables(gramatica, simbolo_inicial):
    """
    Realiza un recorrido DFS desde el símbolo inicial para encontrar todos los No Terminales alcanzables.
    """
    visitados = set()
    pila = [simbolo_inicial]
    
    while pila:
        actual = pila.pop()
        if actual not in visitados:
            visitados.add(actual)
            
            #  si el símbolo actual tiene producciones en la gramática
            if actual in gramatica:
                for der, _ in gramatica[actual]:
                    for simbolo in der:
                        #  si el símbolo de la derecha es un No Terminal, lo añadimos a la pila
                        if not es_terminal(simbolo):
                            pila.append(simbolo)
                            
    #  construimos la gramática final solo con los símbolos visitados
    g_limpia = {}
    for nt in visitados:
        if nt in gramatica:
            g_limpia[nt] = gramatica[nt]
            
    return g_limpia

def convertir_a_cnf(gramatica, simbolo_inicial='S'):
    """
    Ejecuta el pipeline completo de conversión a CNF.
    """
    g, nuevo_inicial = crear_nuevo_simbolo_inicial(gramatica, simbolo_inicial)
    
    g = aislar_terminales(g)
    g = binarizar(g)
    g = eliminar_vacios(g)
    g = eliminar_unitarias(g)
    g = eliminar_inalcanzables(g, nuevo_inicial)

    return g, nuevo_inicial