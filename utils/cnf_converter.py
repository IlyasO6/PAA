


def es_cnf(gramatica):
    """
    Comprueba si una gramática está estrictamente en Forma Normal de Chomsky.
    """
    for producciones in gramatica.values():
        for rhs, _ in producciones:
            # Regla A -> a (Longitud 1, y es minúscula/terminal)
            if len(rhs) == 1 and rhs[0].islower():
                continue
            # Regla A -> BC (Longitud 2, y ambos son mayúsculas/no terminales)
            elif len(rhs) == 2 and not rhs[0].islower() and not rhs[1].islower():
                continue
            # Si no es ninguna de las dos, no está en CNF
            else:
                return False
    return True

def es_terminal(simbolo):
    # Asumimos la convención estándar: los terminales son minúsculas
    return simbolo.islower()

def aislar_terminales(gramatica):
    g_nueva = {}
    nuevas_reglas_terminales = {} # Para guardar cosas como T_a -> a
    
    for lhs, producciones in gramatica.items():
        g_nueva[lhs] = []
        for rhs, prob in producciones:
            # Solo nos importan reglas con más de 1 símbolo (ej. A -> a B)
            if len(rhs) > 1:
                nuevo_rhs = []
                for sim in rhs:
                    if es_terminal(sim):
                        nuevo_nt = f"T_{sim}" # Inventamos el No Terminal "T_a"
                        # Guardamos la regla T_a -> a (con prob 1.0)
                        nuevas_reglas_terminales[nuevo_nt] = [((sim,), 1.0)]
                        nuevo_rhs.append(nuevo_nt)
                    else:
                        nuevo_rhs.append(sim)
                g_nueva[lhs].append((tuple(nuevo_rhs), prob))
            else:
                # Si es longitud 1 (A -> a) o vacía, se queda igual
                g_nueva[lhs].append((rhs, prob))
                
    # Añadimos las reglas inventadas al diccionario principal
    for nt, prod in nuevas_reglas_terminales.items():
        if nt not in g_nueva:
            g_nueva[nt] = prod
            
    return g_nueva


def binarizar(gramatica):
    g_nueva = {}
    contador = 1 # Para inventar nombres únicos: X_1, X_2...
    
    for lhs, producciones in gramatica.items():
        g_nueva[lhs] = []
        for rhs, prob in producciones:
            if len(rhs) > 2:
                # Binarización en cascada
                simbolo_actual = lhs
                
                # Iteramos hasta el penúltimo símbolo
                for i in range(len(rhs) - 2):
                    nuevo_nt = f"X_{contador}"
                    contador += 1
                    
                    if simbolo_actual not in g_nueva:
                        g_nueva[simbolo_actual] = []
                    
                    # La probabilidad original se queda en la primera división.
                    # Las divisiones artificiales posteriores tienen prob 1.0
                    p = prob if i == 0 else 1.0
                    g_nueva[simbolo_actual].append(((rhs[i], nuevo_nt), p))
                    
                    simbolo_actual = nuevo_nt
                    
                # El último eslabón de la cascada se queda con los 2 últimos símbolos
                if simbolo_actual not in g_nueva:
                    g_nueva[simbolo_actual] = []
                g_nueva[simbolo_actual].append(((rhs[-2], rhs[-1]), 1.0))
            else:
                # Reglas que ya son binarias (A -> BC) o unitarias (A -> a)
                g_nueva[lhs].append((rhs, prob))
                
    return g_nueva

def eliminar_vacios(gramatica):
    # 1. Encontrar símbolos "anulables" (que pueden derivar en 'e')
    anulables = set()
    for lhs, producciones in gramatica.items():
        for rhs, prob in producciones:
            if rhs == ('e',):
                anulables.add(lhs)
                
    # Propagación: Si A -> BC y tanto B como C son anulables, A también lo es.
    cambio = True
    while cambio:
        cambio = False
        for lhs, producciones in gramatica.items():
            if lhs not in anulables:
                for rhs, prob in producciones:
                    if len(rhs) == 2 and rhs[0] in anulables and rhs[1] in anulables:
                        anulables.add(lhs)
                        cambio = True
                        
    # 2. Construir la nueva gramática sin 'e' y con las reglas compensatorias
    g_nueva = {}
    for lhs, producciones in gramatica.items():
        g_nueva[lhs] = []
        for rhs, prob in producciones:
            if rhs == ('e',):
                continue  # ¡La eliminamos!
                
            g_nueva[lhs].append((rhs, prob))
            
            # Si es una regla binaria, comprobamos si alguna parte es anulable
            if len(rhs) == 2:
                B, C = rhs
                if B in anulables:
                    g_nueva[lhs].append(((C,), prob)) # A -> C
                if C in anulables:
                    g_nueva[lhs].append(((B,), prob)) # A -> B

    # Limpiamos posibles duplicados (convirtiendo a set y luego a lista)
    for lhs in g_nueva:
        g_nueva[lhs] = list(set(g_nueva[lhs]))
        
    return g_nueva

def eliminar_unitarias(gramatica):
    # 1. Identificar qué puede alcanzar cada No Terminal (A ->* B)
    # Inicialmente, todo símbolo se alcanza a sí mismo
    alcanzables = {nt: set([nt]) for nt in gramatica}
    
    # Encontramos las conexiones directas (A -> B)
    for lhs, producciones in gramatica.items():
        for rhs, prob in producciones:
            if len(rhs) == 1 and not es_terminal(rhs[0]):
                alcanzables[lhs].add(rhs[0])
                
    # Propagación transitiva: Si A llega a B, y B llega a C, entonces A llega a C
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
                            
    # 2. Construir la gramática final
    g_nueva = {}
    for A in gramatica:
        g_nueva[A] = set()
        # Para todo B que A pueda alcanzar...
        for B in alcanzables[A]:
            if B in gramatica:
                # ... copiamos las producciones de B hacia A
                for rhs, prob in gramatica[B]:
                    # PERO solo copiamos las que NO son unitarias
                    if len(rhs) != 1 or es_terminal(rhs[0]):
                        g_nueva[A].add((rhs, prob))
                        
    # Convertimos los sets de vuelta a listas y eliminamos claves vacías
    g_final = {}
    for k, v in g_nueva.items():
        if v: # Si la lista no está vacía
            g_final[k] = list(v)
            
    return g_final

def eliminar_inalcanzables(gramatica, simbolo_inicial):
    """
    Realiza un recorrido DFS desde el símbolo inicial para encontrar
    todos los No Terminales que realmente pueden ser usados.
    """
    visitados = set()
    pila = [simbolo_inicial]
    
    # Recorrido DFS estándar
    while pila:
        actual = pila.pop()
        if actual not in visitados:
            visitados.add(actual)
            
            # Si el símbolo actual tiene producciones en la gramática
            if actual in gramatica:
                for rhs, _ in gramatica[actual]:
                    for simbolo in rhs:
                        # Si el símbolo de la derecha es un No Terminal, lo añadimos a la pila
                        if not es_terminal(simbolo):
                            pila.append(simbolo)
                            
    # Construimos la gramática final solo con los símbolos visitados
    g_limpia = {}
    for nt in visitados:
        if nt in gramatica:
            g_limpia[nt] = gramatica[nt]
            
    return g_limpia

def crear_nuevo_simbolo_inicial(gramatica, inicial_antiguo='S'):
    g = gramatica.copy()
    nuevo_inicial = inicial_antiguo + "0"
    g[nuevo_inicial] = [((inicial_antiguo,), 1.0)]
    return g, nuevo_inicial

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