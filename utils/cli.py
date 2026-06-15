

import argparse

def obtener_argumentos():
    #  Configuración de la interfaz de terminal
    parser = argparse.ArgumentParser(description="Analizador sintáctico CKY / PCKY para CFGs.", add_help=False,
                                     usage="main.py [--pcky] [--cnf] [--batch <archivo>] [--help] gramatica [palabra]")
    
    parser.add_argument("gramatica", help="ruta al archivo .txt con la gramática")
    # nargs='?' para que la palabra sea opcional (por si el usuario usa --batch)
    parser.add_argument("palabra", nargs='?', default="", help="palabra a analizar")
    parser.add_argument("--pcky", "-p", action="store_true", help="ejecuta la versión probabilística (PCKY)")
    parser.add_argument("--cnf", "-c", action="store_true", help="convierte la gramática a CNF antes de evaluar")
    parser.add_argument("--batch", "-b", type=str, metavar="", help="ruta a un archivo de texto con una palabra por línea")
    parser.add_argument("--frase", "-f", action="store_true", help="permite analizar frases (añadido para un caso específico de prueba)")
    parser.add_argument("--help","-h", action="help", help="muestra este mensaje de ayuda")
    return parser, parser.parse_args()