
def imprimir_arbol(arbol, nivel=0):
    """
    Imprime el árbol sintáctico dado en la consola con formato jerárquico.
    """
    if arbol is None:
        return
        
    padding = "    " * nivel
    if len(arbol) == 2:
        etiqueta, palabra = arbol
        print(f"{padding} |__ {etiqueta}: '{palabra}'")
    elif len(arbol) == 3:
        etiqueta, izq, der = arbol
        print(f"{padding} |__ {etiqueta}")
        imprimir_arbol(izq, nivel + 1)
        imprimir_arbol(der, nivel + 1)