

import argparse

def obtener_argumentos():
    #  Configuración de la interfaz de terminal
    parser = argparse.ArgumentParser(description="Analizador Sintáctico CKY / PCKY para Gramáticas Libres de Contexto.")
    
    parser.add_argument("gramatica", help="Ruta al archivo .txt con la gramática.")
    # nargs='?' para que la palabra sea opcional (por si el usuario usa --batch)
    parser.add_argument("palabra", nargs='?', default="", help="Palabra a analizar (ignorado si se usa --batch).")
    parser.add_argument("--pcky", action="store_true", help="Ejecuta la versión probabilística (PCKY).")
    parser.add_argument("--cnf", action="store_true", help="Convierte la gramática a CNF antes de evaluar.")
    parser.add_argument("--batch", type=str, help="Ruta a un archivo de texto con una palabra por línea.")
    
    return parser, parser.parse_args()