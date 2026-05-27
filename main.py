

import sys
from cky import cky
from utils.grammar_parser import leer_gramatica
from utils.cli import obtener_argumentos

def main():
    parser, args = obtener_argumentos()

    #  Validamos los argumentos
    if not args.batch and not args.palabra:
        parser.error("Debes proporcionar una 'palabra' o usar el flag '--batch' con un archivo.")

    #  Leemos la gramática
    try:
        gramatica, es_pcfg = leer_gramatica(args.gramatica)
        print(f"[INFO] Gramática '{args.gramatica}' cargada correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo leer la gramática: {e}")
        sys.exit(1)
        
    # Transformación a CNF (POR HACER)
    if args.cnf:
        print("[INFO] Transformando la gramática a Forma Normal de Chomsky (CNF)...")
        # gramatica = convertir_a_cnf(gramatica)
        
    #  Validaciones de coherencia
    if es_pcfg and not args.pcky:
        print("[AVISO] La gramática es probabilística, pero no se activó --pcky. Se ignorarán las probabilidades.\n")
    elif not es_pcfg and args.pcky:
        print("[AVISO] Se activó --pcky, pero la gramática no contiene probabilidades reales. Se procederá con probabilidades = 1.\n")
    
    #  Preparamos la lista de palabras a analizar (esto lo hemos añadido meramente para implementar el argumento --batch)
    palabras_a_analizar = []
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                #  Leemos línea a línea, quitando espacios y saltos de línea vacíos
                palabras_a_analizar = [linea.strip() for linea in f if linea.strip()]
            print(f"[INFO] Modo Batch: Se han cargado {len(palabras_a_analizar)} palabras del archivo '{args.batch}'.\n")
        except Exception as e:
            print(f"[ERROR] No se pudo leer el archivo batch: {e}")
            sys.exit(1)
    else:
        palabras_a_analizar.append(args.palabra)

    #  Ejecución del algoritmo para cada palabra
    print("-" * 50)
    for palabra in palabras_a_analizar:
        if args.pcky:
            # resultado = pcky_probabilistico(gramatica, word)
            print(f"Palabra: '{palabra}' -> [PCKY NO IMPLEMENTADO]")
        else:
            resultado = cky(gramatica, palabra)
            
            if resultado:
                print(f"Palabra: '{palabra}' -> [RESULTADO: TRUE]")
            else:
                print(f"Palabra: '{palabra}' -> [RESULTADO: FALSE]")
    print("-" * 50)

if __name__ == "__main__":
    main()