# Archivo: test_cnf.py
from utils.grammar_parser import leer_gramatica
from utils.cnf_converter import convertir_a_cnf

def imprimir_gramatica(titulo, gramatica):
    print(f"\n--- {titulo} ---")
    for lhs, producciones in gramatica.items():
        # Formateamos la salida para que sea legible
        rhs_strs = []
        for rhs, prob in producciones:
            rhs_strs.append(" ".join(rhs))
        print(f"{lhs} -> { ' | '.join(rhs_strs) }")

def main():
    ruta = "datos/gn1.txt"
    print(f"Cargando gramática desde: {ruta}")
    
    # 1. Leer la gramática original
    gramatica_original, _ = leer_gramatica(ruta)
    imprimir_gramatica("GRAMÁTICA ORIGINAL", gramatica_original)
    
    # 2. Convertir a CNF
    gramatica_cnf, nuevo_inicial = convertir_a_cnf(gramatica_original, 'S')
    imprimir_gramatica("GRAMÁTICA EN CNF", gramatica_cnf)
    print(f"\n[INFO] El nuevo símbolo inicial a usar en CKY es: {nuevo_inicial}")

if __name__ == "__main__":
    main()