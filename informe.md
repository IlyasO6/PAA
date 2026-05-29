# Practica de Programación y Algoritmia Avanzada – GIA
**Implementación del Algoritmo CKY**

## 1. Integrantes del Grupo
* **Ilyas Ouacham Rhailane**
* **Laia Beyloc Guzman**
* **Grupo:** 12

---

## 2. Enumeración y Arquitectura de Ficheros
[TO DO]

* `main.py`: archivo principal que gestiona la interfaz y el input, y utiliza el resto de archivos para dar un resultado.
* `cky.py`: contiene el algoritmo CKY estándar.
* `pcky.py`: contiene el algoritmo CKY probabilístico.
* `utils/`
  * `cli.py`: donde se configuran los argumentos de terminal.
  * `grammar_parser.py`: lee el archivo `.txt` dado y construye el diccionario con la gramática.
  * `cnf_converter.py`: transforma cualquier CFG (gramatica incontextual) a CNF (Forma Normal de Chomsky).
* `datos/`: directorio que contiene las gramáticas de prueba (`.txt`) y los archivos de palabras (`--batch`).
* `tests/`: directorio que contiene los tests en `test_cky.py` para validar el código mediante la librería `pytest`.

---

## 3. Explicación de Códigos Desarrollados
[TO DO]

**Estructuras de Datos y Optimización:**[TO DO]
Para optimizar el tiempo de ejecución, el parser no pasa la gramática cruda al algoritmo, sino que este último la transforma en un **diccionario invertido** (ej. `{(B, C): [A]}`). Dado que el CKY busca qué no terminales generan una subcadena, esta estructura reduce el coste de búsqueda en el bucle más profundo a $\mathcal{O}(1)$ gracias a las tablas Hash de Python.
La tabla CKY se ha implementado como una matriz bidimensional indexada por longitud ($L$) y posición de inicio ($i$). Las celdas contienen estructuras `set()` para evitar duplicados en tiempo constante.

**Complejidad:**[TO DO]
El algoritmo consta de tres bucles anidados: iteración sobre la longitud de la subcadena ($L$), iteración sobre la posición de inicio ($i$), e iteración sobre el punto de partición ($k$). Esto garantiza que la complejidad temporal teórica se mantenga estrictamente en $\mathcal{O}(N^3 \cdot |G|)$, siendo $N$ la longitud de la palabra y $|G|$ el tamaño de la gramática.

---

## 4. Formato Elegido para Describir Gramáticas
[TO DO]
Se ha optado por una variante de la **Forma de Backus-Naur (BNF)** por ser el estándar académico de la disciplina. 
El formato sigue la estructura: `LHS -> RHS1 [prob] | RHS2 [prob]`.

**Decisiones de diseño para la robustez:**[TO DO]
* **Separación por espacios:** Exigimos que los símbolos de las producciones estén separados por espacios (ej. `X A` en lugar de `XA`). Esto permite que el *parser* soporte No Terminales de múltiples caracteres (como `Sujeto` o `NP`), haciendo la herramienta escalable para Procesamiento de Lenguaje Natural (NLP).
* **Tolerancia:** El *parser* (`grammar_parser.py`) ignora automáticamente líneas vacías y comentarios (iniciados con `#`), y utiliza `.strip()` para ser tolerante a espacios irregulares introducidos por el usuario.
* **Palabra vacía:** Se ha adoptado el carácter `e` minúscula para representar la producción $\epsilon$.

---

## 5. Descripción de las Extensiones Realizadas
[TO DO]

**Extensión 1: Transformación a CNF (`cnf_converter.py`)**[TO DO]
Se ha desarrollado un algoritmo determinista que transforma cualquier CFG a CNF conservando el lenguaje generado. Se ha prestado especial atención al orden de ejecución para evitar incongruencias:
1. *Nuevo Símbolo Inicial:* Protege la raíz de la gramática.
2. *Aislar Terminales y Binarizar:* Al ejecutar estas transformaciones sintácticas primero, garantizamos que las reglas resultantes tengan longitud máxima 2.
3. *Eliminar producciones $\epsilon$ y Unitarias:* La lógica de propagación se simplifica enormemente gracias a la binarización previa.
4. *Eliminación de Inalcanzables (Extra):* Se ha añadido un sexto paso que realiza un recorrido en profundidad (DFS) desde el símbolo inicial para purgar la gramática de símbolos inútiles generados durante la transformación.

**Extensión 2: CKY Probabilístico (`pcky.py`)**[TO DO]
Se ha adaptado la estructura de la tabla CKY. En lugar de conjuntos lógicos, cada celda es un diccionario que mapea cada No Terminal a la **probabilidad máxima** de derivación en ese punto. El algoritmo evalúa todas las ambigüedades estructurales y aplica la ecuación de maximización $P_{nueva} = \max(P_{actual}, P_B \times P_C \times P_{regla})$ en cada iteración.

---

## 6. Valoración del Aprendizaje Obtenido
[TO DO]

---

## 7. Otras Consideraciones Pertinentes
[TO DO]

Además de los requisitos del enunciado, hemos implementado las siguientes mejoras de "Calidad de Vida" (QoL) e Ingeniería de Software en el proyecto:

* **Detección Automática de CNF:** El programa analiza la gramática de entrada en $\mathcal{O}(|G|)$. Si detecta que no está en CNF, invoca automáticamente la Extensión 1 antes de ejecutar el CKY, sin requerir intervención del usuario.
* **Tokenización Dinámica:** El algoritmo detecta el formato de la entrada. Si la entrada contiene espacios (ej. `"el gato come"`), la analiza como una lista de palabras (tokens). Si no los contiene (ej. `"aabb"`), la analiza carácter a carácter. Esto permite procesar tanto lenguajes formales abstractos como frases de lenguaje natural.
* **Testing Automatizado:** Se entrega una suite de pruebas en el directorio `tests/`. Utilizando el framework `pytest` y la parametrización de casos de prueba, hemos validado el código contra casos límite (cadenas vacías, caracteres inexistentes) y verificado la correctitud de ambas extensiones.