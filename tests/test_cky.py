"""
Estructura:
  - Módulo 1: tests sobre el archivo grammar_parser.py
  - Módulo 2: tests sobre el archivo cnf_converter.py
  - Módulo 3: tests sobre el archivo cky.py
  - Módulo 4: tests sobre el archivo pcky.py
  - Módulo 5: tests de integración (conversor + CKY)
"""

import pytest
from cky import cky
from pcky import pcky
from utils.grammar_parser import leer_gramatica
from utils.cnf_converter import es_cnf, convertir_a_cnf


#   GRAMATICAS:
DIR = "datos/"
CNF1 = f"{DIR}g1.txt"
CNF2 = f"{DIR}g2.txt"
CNF3 = f"{DIR}g3.txt"
CNF4 = f"{DIR}g4.txt"
CNF5 = f"{DIR}g5.txt"

PCNF1 = f"{DIR}gp1.txt"
PCNF2 = f"{DIR}gp2.txt"
PCNF3 = f"{DIR}gp3.txt"

CFG1 = f"{DIR}gn1.txt"
CFG2 = f"{DIR}gn2.txt"
CFG3 = f"{DIR}gn3.txt"
CFG4 = f"{DIR}gn4.txt"
CFG5 = f"{DIR}gn5.txt"
CFG6 = f"{DIR}gn6.txt"

#  ________________________ MÓDULO 1: tests sobre el archivo grammar_parser.py _____________________________

class TestGrammarParser:
    """Verifica que se leen las gramáticas correctamente."""

    def test_comprovacion_no_pcgf(self):
        """
        Una gramática CNF para el algoritmo CKY debe devolver es_pcnf=False
        y asignar probabilidad 1.0 a todas las producciones.
        """
        gramatica, es_pcnf = leer_gramatica(CNF1)
        assert es_pcnf is False
        for producciones in gramatica.values():
            for _, prob in producciones:
                assert prob == 1.0

    def test_comprovacion_si_pcgf(self):
        """
        Una gramática PCNF (CNF probabilística) con probabilidades para el algoritmo PCKY 
        debe devolver es_pcnf=True y obtener las probabilidades correctamente.
        """
        gramatica, es_pcfg = leer_gramatica(PCNF1)
        assert es_pcfg is True
        #   S tiene dos producciones con probs 0.8 y 0.2
        probs_s = {prob for _, prob in gramatica["S"]}
        assert 0.8 in probs_s
        assert 0.2 in probs_s

    def test_estructura_correcta_de_parte_derecha(self):
        """
        Cada parte derecha de una producción debe ser una tupla de strings.
        Ej: S -> X A debe dar ('X', 'A').
        """
        gramatica, _ = leer_gramatica(CNF1)
        lista_der = [der for der, _ in gramatica["S"]]
        assert ('X', 'A') in lista_der
        assert ('A', 'X') in lista_der

        assert ('a',) in lista_der

    def test_caracter_vacio_se_extrae_correctamente(self):
        """
        La 'e' en el archivo .txt debe tratarse como cualquier
        otro símbolo: la producción A -> e debe dar der = ('e',).
        """
        gramatica, _ = leer_gramatica(CFG3)
        lista_der = [der for der, _ in gramatica["A"]]
        assert ('e',) in lista_der

    def test_ignora_lineas_vacias_y_comentarios(self):
        """
        Debe ignorar las líneas vacías y los comentarios (tras '#').
        """
        gramatica, _ = leer_gramatica(CNF1)
        assert set(gramatica.keys()) == {"S", "A", "B", "X", "R"}

    def test_multiples_producciones(self):
        """
        Comprovamos que extrae correctamente las producciones multiples.
        """
        gramatica, _ = leer_gramatica(CNF1)
        #   S -> a | X A | A X | b 
        assert len(gramatica["S"]) == 4


# ____________________________ Módulo 2:  archivo cnf_converter.py _____________________________

class TestEsCNF:
    """Verifica que es_cnf() detecta correctamente si una gramática está en CNF."""

    @pytest.mark.parametrize("ruta", [
        CNF1,
        CNF2,
        CNF3,
        CNF4,
        CNF5,
    ])
    def test_es_cnf_true(self, ruta):
        gramatica, _ = leer_gramatica(ruta)
        assert es_cnf(gramatica) is True

    @pytest.mark.parametrize("ruta", [
        CFG1,
        CFG2,
        CFG5,
        CFG6,
    ])
    def test_es_cnf_false(self, ruta):
        gramatica, _ = leer_gramatica(ruta)
        assert es_cnf(gramatica) is False


class TestConvertirACNF:
    """Verifica los 6 pasos del conversor y el pipeline completo."""

    def test_crear_nuevo_simbolo_inicial(self):
        """
        convertir_a_cnf() siempre crea un nuevo símbolo inicial S0
        que no aparece en ninguna producción de la gramática resultante.
        """
        gramatica, _ = leer_gramatica(CFG6)
        g_cnf, nuevo_inicial = convertir_a_cnf(gramatica, "S")
        assert nuevo_inicial == "S0"

        #  Comprovamos que no aparezca en ninguna producción
        for producciones in g_cnf.values():
            for der, _ in producciones:
                assert "S0" not in der

    def test_aislar_terminales(self):
        """
        Tras convertir GN2 (que tiene 'a B' y 'A b'), la gramática CNF
        resultante debe contener los no terminales T_a y T_b.
        """
        gramatica, _ = leer_gramatica(CFG2)
        g_cnf, _ = convertir_a_cnf(gramatica, "S")
        assert "T_a" in g_cnf
        assert "T_b" in g_cnf
        #  T_a -> a y T_b -> b
        assert (("a",), 1.0) in g_cnf["T_a"]
        assert (("b",), 1.0) in g_cnf["T_b"]

    def test_paso3_binarizar_no_hay_reglas_de_aridad_mayor_2(self):
        """
        Tras convertir GN1 (que tiene S -> A B C, aridad 3),
        ninguna producción de la gramática resultante puede tener más de 2 símbolos.
        """
        gramatica, _ = leer_gramatica(CFG1)
        g_cnf, _ = convertir_a_cnf(gramatica, "S")
        for producciones in g_cnf.values():
            for der, _ in producciones:
                assert len(der) <= 2

    def test_paso4_epsilon_se_elimina_completamente(self):
        """
        Tras convertir GN3, no debe quedar ninguna producción con ('e',)
        en la gramática resultante.
        """
        gramatica, _ = leer_gramatica(CFG3)
        g_cnf, _ = convertir_a_cnf(gramatica, "S")
        for producciones in g_cnf.values():
            for der, _ in producciones:
                assert der != ("e",)

    def test_paso4_epsilon_cascada_anulabilidad_propagada(self):
        """
        En GN4, B -> A A donde A es anulable. Por tanto B también es anulable.
        Tras la conversión, el lenguaje {c, ac, aac} debe reconocerse íntegramente.
        """
        gramatica, _ = leer_gramatica(CFG4)
        g_cnf, inicial = convertir_a_cnf(gramatica, "S")
        assert cky(g_cnf, list("c"),   inicial) is True   #  n=0, B=vacío
        assert cky(g_cnf, list("ac"),  inicial) is True   #  n=1, B=a
        assert cky(g_cnf, list("aac"), inicial) is True   #  n=2, B=aa
        assert cky(g_cnf, list("aaac"),inicial) is False  #  no pertenece

    def test_paso5_unitarias_con_ciclo_no_lanza_error(self):
        """
        GN5 tiene el ciclo unitario A->B->C->A. El conversor debe resolverlo
        correctamente sin RecursionError ni bucle infinito.
        El lenguaje resultante es {a, b}.
        """
        gramatica, _ = leer_gramatica(CFG5)
        g_cnf, inicial = convertir_a_cnf(gramatica, "S")
        assert cky(g_cnf, list("a"),  inicial) is True
        assert cky(g_cnf, list("b"),  inicial) is True
        assert cky(g_cnf, list("aa"), inicial) is False
        assert cky(g_cnf, list("ab"), inicial) is False

    def test_paso5_no_quedan_reglas_unitarias_nt_nt(self):
        """
        Tras la conversión de GN5, ninguna producción debe ser de la forma
        NT -> NT (regla unitaria no terminal).
        """
        gramatica, _ = leer_gramatica(CFG5)
        g_cnf, _ = convertir_a_cnf(gramatica, "S")
        for producciones in g_cnf.values():
            for der, _ in producciones:
                if len(der) == 1:
                    #  La única producción de longitud 1 permitida es NT -> terminal
                    assert der[0].islower(), (
                        f"Regla unitaria NT->NT encontrada: {der}"
                    )

    def test_paso6_elimina_simbolos_inalcanzables(self):
        """
        G5 tiene el símbolo Z que no es alcanzable desde S.
        Aunque es_cnf devuelve True (Z no viola la forma), convertir_a_cnf
        debe eliminarlo porque el paso 6 (DFS) lo poda.
        """
        gramatica, _ = leer_gramatica(CNF5)
        g_cnf, _ = convertir_a_cnf(gramatica, "S")
        assert "Z" not in g_cnf

    def test_output_es_cnf_valido(self):
        """
        Tras aplicar convertir_a_cnf() a cualquier CFG No-CNF,
        la gramática resultante debe pasar es_cnf().
        """
        for ruta in [CFG1, CFG2, CFG3,
                     CFG4, CFG5, CFG6]:
            gramatica, _ = leer_gramatica(ruta)
            g_cnf, _ = convertir_a_cnf(gramatica, "S")
            assert es_cnf(g_cnf) is True, f"Fallo en {ruta}: resultado no es CNF"



# ____________________________ MÓDULO 3: Algoritmo CKY determinista _______________________________________________

#   (ruta_gramatica, palabra_como_lista, resultado_esperado)
CASOS_CKY = [
    #   G1: strings de longitud [1, 4]
    (CNF1, list("a"),    True),  
    (CNF1, list("b"),    True),  
    (CNF1, list("aa"),   False),
    (CNF1, list("ab"),   False), 
    (CNF1, list("aba"),  False), 
    (CNF1, list("aaaa"), True),   
    (CNF1, list("aaab"), True),   
    (CNF1, list("aaba"), True),   
    (CNF1, list("aabb"), True),   
    (CNF1, list("abaa"), True),   
    (CNF1, list("abba"), True), 
    (CNF1, list("bbbb"), False), 
    (CNF1, list("babb"), False),  

    #   G2: gramática ambigua (S -> SS), varios caminos para la misma cadena 
    (CNF2, list("ab"),   True),
    (CNF2, list("bb"),   True),
    (CNF2, list("bba"),  True),
    (CNF2, list("bbb"),  True),
    (CNF2, list("aabb"), True),
    (CNF2, list("abab"), True),
    (CNF2, list("a"),    False),  
    (CNF2, list("b"),    False), 
    (CNF2, list("aa"),   False),
    (CNF2, list("ba"),   False),

    #   G3: lenguaje a^n b^n (n >= 1), caso borde longitud par/impar 
    (CNF3, list("ab"),       True),
    (CNF3, list("aabb"),     True),
    (CNF3, list("aaabbb"),   True),
    (CNF3, list("aaaabbbb"), True),
    (CNF3, list("aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbb"), True),
    (CNF3, list("a"),        False),
    (CNF3, list("b"),        False), 
    (CNF3, list("ba"),       False), 
    (CNF3, list("aab"),      False),
    (CNF3, list("abb"),      False),
    (CNF3, list("abab"),     False),

    #   G4: palíndromos de longitud par 
    (CNF4, list("aa"),     True),
    (CNF4, list("bb"),     True),
    (CNF4, list("abba"),   True),
    (CNF4, list("baab"),   True),
    (CNF4, list("aaaa"),   True),
    (CNF4, list("bbbb"),   True),
    (CNF4, list("ababbaababbabaabbabaababbaababbabaabbabaababbaababbabaabbaba"), True),
    (CNF4, list("a"),      False),  
    (CNF4, list("ab"),     False),  
    (CNF4, list("ba"),     False), 
    (CNF4, list("aba"),    False),   

    #   G5: a's de longitud impar y simbolos inalcanzables
    (CNF5, list("a"),     True),
    (CNF5, list("aaa"),   True),
    (CNF5, list("aaaaa"), True),
    (CNF5, list("aa"),    False), 
    (CNF5, list("aaaaaaaaaaaaa"),    True),
    (CNF5, list("aaaa"),  False),
    (CNF5, list("b"),     False), 
    (CNF5, list("bb"),    False),
]

@pytest.mark.parametrize("ruta, palabra, esperado", CASOS_CKY)
def test_cky_algoritmo(ruta, palabra, esperado):
    """
    Test parametrizado del algoritmo CKY determinista.
    Cubre: positivos, negativos, longitud 1, gramáticas ambiguas,
    lenguajes (a^n b^n), palíndromos, y gramáticas con símbolos inalcanzables.
    """
    gramatica, _ = leer_gramatica(ruta)
    resultado = cky(gramatica, palabra)
    assert resultado == esperado


class TestCKYCasosBorde:
    """Tests de casos borde que merecen una aserción explícita y comentada."""

    def test_cky_cadena_vacia_devuelve_false(self):
        """
        El algoritmo CKY debe devolver False para la cadena vacía.
        """
        gramatica, _ = leer_gramatica(CNF1)
        assert cky(gramatica, [], "S") is False

    def test_cky_simbolo_inicial_correcto(self):
        """
        Si se pasa un símbolo inicial que no existe en la gramática,
        el resultado debe ser False.
        """
        gramatica, _ = leer_gramatica(CNF1)
        assert cky(gramatica, list("a"), "Z") is False

    def test_cky_gramatica_ambigua_resultado_correcto(self):
        """
        CKY debe igualmente devolver True si al menos uno existe.
        """
        gramatica, _ = leer_gramatica(CNF2)
        #  'aabb' tiene múltiples derivaciones en G2
        assert cky(gramatica, list("aabb"), "S") is True


# ____________________________ MÓDULO 4: Algoritmo PCKY _______________________________________________

#  (ruta_gramática, palabra, esperado, tolerancia)
TOL = 1e-9 #  se usa esto en vez de 0 porque las operaciones sobre floats no siempre son exactas
CASOS_PCKY = [
    #   GP1: dos derivaciones para 'ab'
    (PCNF1, list("ab"), 0.80, TOL),   #  max(0.80, 0.20) = 0.80
    (PCNF1, list("ba"), 0.0,  TOL),   #  no pertenece
    (PCNF1, list("a"),  0.0,  TOL),   #  no pertenece

    #   GP2: única derivación posible por cadena
    (PCNF2, list("ab"), 0.35, TOL),   #  0.5 * 0.7 * 1.0
    (PCNF2, list("bb"), 0.15, TOL),   #  0.5 * 0.3 * 1.0
    (PCNF2, list("aa"), 0.0,  TOL),   #  no pertenece
    (PCNF2, list("a"),  0.0,  TOL),   #  no pertenece

    #   GP3: cadena más larga
    (PCNF3, list("aab"), 0.9,  TOL),  #  0.9 * 1.0 * 1.0 * 1.0 * 1.0
    (PCNF3, list("ab"),  0.1,  TOL),  #  0.1 * 1.0 * 1.0
    (PCNF3, list("abb"), 0.0,  TOL),  #  no pertenece
]

@pytest.mark.parametrize("ruta, palabra, esperado, tol", CASOS_PCKY)
def test_pcky_algoritmo(ruta, palabra, esperado, tol):
    """
    Test parametrizado del algoritmo PCKY probabilístico.
    Cubre: selección del máximo entre varias derivaciones y cálculo exacto de productos de probabilidades.
    """
    gramatica, _ = leer_gramatica(ruta)
    resultado, _ = pcky(gramatica, palabra)
    assert abs(resultado - esperado) < tol, (
        f"pcky({ruta!r}, {palabra}) = {resultado}, esperado ≈ {esperado}"
    )


class TestPCKYCasosBorde:
    """ Tests de casos borde para PCKY."""

    def test_pcky_cadena_vacia_devuelve_0(self):
        """
        Para cadena vacía, PCKY debe devolver 0.0.
        """
        gramatica, _ = leer_gramatica(PCNF1)
        assert pcky(gramatica, []) == 0.0

    def test_pcky_coherencia_con_cky(self):
        """
        Para cualquier cadena: si pcky > 0.0 entonces cky debe ser True,
        y si cky es False entonces pcky debe ser 0.0.
        Verificamos esto sobre un conjunto representativo de cadenas con GP2.
        """
        gramatica_p, _ = leer_gramatica(PCNF2)
        gramatica_d, _ = leer_gramatica(PCNF2)

        candidatos = [list(w) for w in ["ab", "bb", "aa", "a", "b", "aba", "bbb"]]
        for palabra in candidatos:
            prob, _ = pcky(gramatica_p, palabra)
            booleano = cky(gramatica_d, palabra)
            assert (prob > 0.0) == booleano, (
                f"Incoherencia en {''.join(palabra)!r}: "
                f"pcky={prob}, cky={booleano}"
            )


#  MÓDULO 5: Tests de integración, Conversor + CKY

class TestIntegracion:
    """
    Verifica que convertir_a_cnf() preserva el lenguaje:
    las cadenas aceptadas/rechazadas antes de convertir deben seguir
    siéndolo después (comprobado vía CKY sobre la gramática convertida).

    CKY no puede ejecutarse directamente sobre gramáticas No-CNF,
    por lo que las aceptaciones 'antes' se han verificado manualmente.
    """

    #  (ruta_gramática, simbolo_inicial, cadena, esperado_tras_conversion)
    CASOS_PRESERVACION = [
        #  GN1: lenguaje = {abc}
        (CFG1, "S", list("abc"),  True),
        (CFG1, "S", list("ab"),   False),
        (CFG1, "S", list("abcd"), False),
        (CFG1, "S", list("bc"),   False),

        #  GN2: lenguaje = {ab}
        (CFG2, "S", list("ab"),   True),
        (CFG2, "S", list("a"),    False),
        (CFG2, "S", list("b"),    False),
        (CFG2, "S", list("ba"),   False),

        #  GN3: lenguaje = {b, ab}  (A puede ser símbolo vacio)
        (CFG3, "S", list("b"),    True),
        (CFG3, "S", list("ab"),   True),
        (CFG3, "S", list("a"),    False),
        (CFG3, "S", list("ba"),   False),
        (CFG3, "S", list("bb"),   False),

        #  GN4: lenguaje = {c, ac, aac}  (B->AA, A anulable => cascada)
        (CFG4, "S", list("c"),    True),
        (CFG4, "S", list("ac"),   True),
        (CFG4, "S", list("aac"),  True),
        (CFG4, "S", list("aaac"), False),
        (CFG4, "S", list("a"),    False),

        #  GN5: lenguaje = {a, b}  (ciclos unitarios A->B->C->A)
        (CFG5, "S", list("a"),    True),
        (CFG5, "S", list("b"),    True),
        (CFG5, "S", list("aa"),   False),
        (CFG5, "S", list("ab"),   False),

        #  GN6: lenguaje = {a^n b^n c | n >= 0}
        (CFG6, "S", list("c"),        True),
        (CFG6, "S", list("abc"),       True),
        (CFG6, "S", list("aabbc"),     True),
        (CFG6, "S", list("aaabbbc"),   True),
        (CFG6, "S", list("ab"),        False),
        (CFG6, "S", list("aabc"),      False),
        (CFG6, "S", list("abbc"),      False),
        (CFG6, "S", list("cc"),        False),
    ]

    @pytest.mark.parametrize("ruta, inicial, palabra, esperado", CASOS_PRESERVACION)
    def test_conversion_preserva_lenguaje(self, ruta, inicial, palabra, esperado):
        """
        Convierte la CFG a CNF y ejecuta CKY sobre la gramática resultante.
        """
        gramatica, _ = leer_gramatica(ruta)
        g_cnf, nuevo_inicial = convertir_a_cnf(gramatica, inicial)
        resultado = cky(g_cnf, palabra, nuevo_inicial)
        assert resultado == esperado, (
            f"Fallo en {ruta!r}, cadena {''.join(palabra)!r}: "
            f"obtenido={resultado}, esperado={esperado}"
        )

    def test_conversor_idempotente(self):
        """
        Aplicar convertir_a_cnf() dos veces debe producir una gramática
        que sigue pasando es_cnf() y reconoce el mismo lenguaje.
        """
        gramatica, _ = leer_gramatica(CFG6)
        g_cnf1, inicial1 = convertir_a_cnf(gramatica, "S")
        g_cnf2, inicial2 = convertir_a_cnf(g_cnf1, inicial1)
        assert es_cnf(g_cnf2) is True

        #  el lenguaje debe seguir siendo el mismo
        for cadena, esperado in [(list("c"), True), (list("abc"), True),
                                  (list("ab"), False), (list("cc"), False)]:
            assert cky(g_cnf2, cadena, inicial2) == esperado