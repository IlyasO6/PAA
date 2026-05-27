

import pytest
from cky import cky
from utils.grammar_parser import leer_gramatica


CASOS_DE_PRUEBA = [
    # Pruebas con G1 
    ("datos/g1.txt", "aabb", True),
    ("datos/g1.txt", "aba", False),
    
    # Pruebas con G2 
    ("datos/g2.txt", "ab", True),
    ("datos/g2.txt", "a", False),
    
    # Pruebas con G3
    ("datos/g3.txt", "aaabb", True),
    ("datos/g3.txt", "bbaa", False), 
    
    # Pruebas con G4
    ("datos/g4.txt", "()()", True),
    ("datos/g4.txt", "()(", False),
    
    # Pruebas con G5
    ("datos/g5.txt", "aaaaa", True),
    ("datos/g5.txt", "aaaa", False)
]

@pytest.mark.parametrize("ruta_gramatica, palabra, esperado", CASOS_DE_PRUEBA)
def test_cky_algoritmo(ruta_gramatica, palabra, esperado):
    """
    Test automatizado que inyecta las 10 combinaciones de prueba.
    """
    #  Leemos la gramática
    gramatica, _ = leer_gramatica(ruta_gramatica)
    
    #  Ejecutamos el algoritmo
    resultado = cky(gramatica, palabra)
    
    # Comprobamos que el resultado es el que esperábamos
    assert resultado == esperado