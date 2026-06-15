
import sys
from cky import cky
from pcky import pcky
from utils.grammar_parser import leer_gramatica
from utils.cli import obtener_argumentos
from utils.cnf_converter import convertir_a_cnf, es_cnf
from utils.imprimir_arbol import imprimir_arbol

VERDE = '\033[92m'
ROJO = '\033[91m'
AMARILLO = '\033[93m'
GRIS = '\033[2m'
BOLD = '\033[1m'
RESET = '\033[0m'
INFO = f"{VERDE}[INFO]{RESET}"
AVISO = f"{AMARILLO}[AVISO]{RESET}"
ERROR = f"{ROJO}[ERROR]{RESET}"


def main():
    """
    Esta función ejecuta el siguiente pipeline: 
    - Validación de argumentos.
    - Lectura de la gramática.
    - Comprovación de CNF y potencialmente transformación también. 
    - Validación de coherencia entre argumentos y gramática. 
    - Obtención de las palabras dadas en la entrada.
    - Ejecución del algoritmo para cada palabra. 
    - Muestra de resultados.
    """
    parser, args = obtener_argumentos()

    #  validamos los argumentos
    if not args.batch and not args.palabra:
        parser.error("Debes proporcionar una palabra o usar el flag '--batch' con un archivo.")

    #  leemos la gramática
    try:
        gramatica, es_pcnf = leer_gramatica(args.gramatica)
        print(f"{INFO}{GRIS} Gramática '{args.gramatica}' cargada correctamente.{RESET}")
    except Exception as e:
        print(f"{ERROR} No se pudo leer la gramática {args.gramatica}.")
        sys.exit(1)
       
    #  transformamos a CNF
    if not es_cnf(gramatica): #if args.cnf:  # Descomentar para quitar la comprobación automática
        print(f"{INFO} {GRIS}La gramática no está en CNF, se procederá con su transformación....{RESET}", end=" ")
        gramatica, simbolo_inicial = convertir_a_cnf(gramatica)
        print("ok.\n")
    else:
        simbolo_inicial = 'S'

    #  validamos la coherencia (i.e. revisamos que si la gramática es probabilística, se haya usado la flag --pcky, y viceversa)
    if es_pcnf and not args.pcky:
        print(f"{AVISO} La gramática es probabilística, pero no se activó --pcky. Se ignorarán las probabilidades.\n")
    elif not es_pcnf and args.pcky:
        print(f"{AVISO} Se activó --pcky, pero la gramática no contiene probabilidades reales. Se procederá con probabilidades = 1.\n")
    

    #  preparamos la lista de palabras a analizar (esto lo hemos añadido meramente para implementar el argumento --batch)
    palabras_a_analizar = []
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                #  leemos línea a línea, quitando espacios y saltos de linea vacíos
                palabras_a_analizar = [linea.strip() for linea in f if linea.strip()]
            print(f"{INFO} {GRIS}Se han cargado {len(palabras_a_analizar)} palabras del archivo '{args.batch}'.{RESET}\n")
        except:
            print(f"{ERROR} No se pudo leer el archivo batch  '{args.batch}'")
            sys.exit(1)
    else:
        palabras_a_analizar.append(args.palabra)


    #  ejecución del algoritmo para cada palabra
    print(f"\n{BOLD}{'RESULTADOS':^83}{RESET}")
    print(f"{'Palabra':^40} | {'Pertenece a la gramática?':^10}")
    for palabra in palabras_a_analizar:
        w = palabra
        if args.frase:
            w = palabra.split()

        if args.pcky:
            resultado, arbol = pcky(gramatica, w, simbolo_inicial)
        else:
            resultado = f"{cky(gramatica, w, simbolo_inicial)}".upper()
        if resultado:
            color = VERDE
        else:
            color = ROJO
        print(f"{color}{palabra:^40}{RESET} | {color}{resultado}{RESET}")

        if args.pcky and resultado > 1e-15:
            print(f"\n{'Árbol sintáctico'}\n")
            imprimir_arbol(arbol)

if __name__ == "__main__":
    main()