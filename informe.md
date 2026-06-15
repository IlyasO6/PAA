# Practica de Programación y Algoritmia Avanzada – GIA
**Implementación del Algoritmo CKY**

## 1. Integrantes del Grupo
* **Ilyas Ouacham Rhailane**
* **Laia Beyloc Guzman**
* **Grupo:** 12


## 2. Enumeración y Arquitectura de Ficheros
[TO DO]

* `main.py`: archivo principal que gestiona la interfaz y el input, y utiliza el resto de archivos para dar el resultado.
* `cky.py`: módulo que implementa el algoritmo determinista CKY.
* `pcky.py`: módulo de extensión que contiene la variante probabilítica del algoritmo CKY.
* `utils/`
  * `cli.py`: define y configura la interfaz de línea de comandos y la gestión de argumentos.
  * `grammar_parser.py`: lee, limpia y transforma el archivo `.txt` dado en un diccionario que representa la gramática.
  * `cnf_converter.py`: módulo de extension que detecta y transforma cualquier Gramatica Libre de Contexto (CFG) a Forma Normal de Chomsky (CNF).
* `datos/`: directorio que almacena las gramáticas de prueba y los archivos de palabras para la ejecución en lote. 
* `tests/`: directorio que contiene los tests en `test_cky.py` para validar el código mediante la librería `pytest`.


## 3. Explicación de Códigos Desarrollados

### Pipeline principal

El flujo de trabajo se encuentra en el archivo *main.py*, que hace uso de otros archivos, manteniendo la estructura modular. La ejecución se inicia mediante el siguiente comando en la línea de comandos:

  main.py [--pcky] [--cnf] [--batch <archivo>] [--help] gramatica [palabra]

Así pues, el programa sigue el siguiente orden secuencial:

- Validación de argumentos: comprueba que hayan suficientes datos para trabajar. 
- Lectura de la gramática: lee el archivo de gramática dado y devuelve un diccionario para representarla.
- Comprovación de CNF y potencial transformación: comprueba si la gramática está en CNF; y en caso de ser necesario transforma la gramática a CNF. 
- Validación de coherencia: comprueba que los argumentos dados sean coherentes con la naturaleza de la gramática. 
- Obtención de la entrada: lee la palabra dada de entrada, o el archivo con palabras (si se indica con la "flag" *--batch*)
- Ejecución del algoritmo: una vez leídos los datos, ejecuta el algoritmo respectivo de entre CKY y PCKY. 
- Muestra de resultados: imprime los resultados obtenidos por el algoritmo de manera estructurada en la terminal. 

### Lectura de datos

La lectura de la gramática se hace con la función *leer_gramática* de grammar_parser.py. Esta función ignora lineas vacias y espacios de más, así como comentarios denotados con el marcador "#" (como en python). Obtiene secuencialmente la gramática (fila a fila), donde en cada regla comprueba si hay alguna probabilidad (implementado meramente para el PCKY, pero el lector de gramática es general) y guarda la regla en un diccionario donde la llave es el símbolo no terminal generador, y el valor es una tupla con una tupla con la producción (cada elemento de la tupla es un símbolo) y la probabilidad de la regla. 
Finalmente devuelve la gramática y una variable booleana que indica si la gramática es probabilística o no, para hacer la comprobación de coherencia más adelante.

Un ejemplo de la representación con el diccionario, para la gramática G dada, sería:

G =
  S -> AB
  A -> a
  B -> b

gramatica = {
  'S': [(('A', 'B'), 1.0)],
  'A': [(('a',), 1.0)],
  'B': [(('b',), 1.0)]
}

### CKY

El módulo principal implementa el análisis sintáctico mediante programación dinámica *bottom-up*. El flujo de ejecución se divide en cuatro fases principales: 

- Preprocesamiento de la gramática: para optimizar la búsqueda, se invierte el diccionario de la gramática dado. Esto se hace porque, al ser la tabla implementada *bottom-up*, se busca encontrar los No Terminales que generan la producción actual. Es por eso que el formato original del diccionario, donde las llaves eran los símbolos generadores, es sub-óptimo, y recurrimos a la inversión para hacer de la búsqueda un acceso directo *O(1)*. Adicionalmente, se eliminan las probabilidades del diccionario, pues son exlusivas del algoritmo PCKY. 

- Inicialización de la tabla: se define una matriz de dimensiones (N+1)xN, donde N es la longitud de la palabra. Las filas representan la longitud de la subpalabra (L) y las columnas el índice de inicio (i). Se inicializa la base (L = 1) evaluando cada caracter individualmente para extraer los No Terminales que lo derivan (mirando reglas del tipo "A -> a").

- Iteración principal: se rellena el resto de la matriz nivel a nivel mediante tres bucles anidados. Una ventana de longitud L se desliza sobre la palabra (la ventana empieza en el índice *i*, y el indice aumenta de uno en uno). Para cada subpalabra restante se evaluan todas sus particiones binarias (el índice *k* representa donde empieza la partición, evaluando particiones desde k=1 hasta k=L-1). El contenido de la celda actual se calcula realizando el producto cartesiano de los No Terminales encontrados en las celdas particionadas, y verificando si cada combinación resultante existe en la gramática. 

- Resultado: al terminar el llenado de la tabla, la celda superior corresponde a L = N. Sabemos que la subpalabra con longitud N es la palabra en sí, y es por ello que comprobamos esta celda para ver el resultado. Si el símbolo inicial de la gramática está contenido en esta celda, la función devuelve *True*; y *False* en caso contrario. Esta lógica se debe al hecho de que si está el símbolo inicial al final de la ejecución, significa que se ha podido "escalar" desde la palabra hasta este mediante reglas de la gramática, lo cual es el proceso inverso de generación, demostrando así que la palabra sí pertenece. 

Para ilustrar el proceso de iteración principal, veáse el siguiente ejemplo: 

Dada la palabra "aaabbb", al evaluar la longitud L=4 en la posición i=1, analizamos la subpalabra "aabb". El algoritmo itera sobre sus tres particiones posibles (k=1,2,3): "a" y "abb", "aa" y "bb" o "aab" y "b". Se consultan las celdas previamente calculadas para estas particiones y evalua el producto cartesiano (por ejemplo, entre la celda correspondiente a "a" en i=1 y L=1, y la correspondiente a "abb" en i=2 y L=3) de todas las parejas y rellena la celda actual con los No Terminales que pueden generar alguna de las combinaciones. 


## 4. Formato Elegido para Describir Gramáticas [TO DO]
El formato elegido para describir las gramáticas es un derivado de la **Forma de Backus-Naur**, pero más facil de leer. Las reglas sintácticas se rigen por las siguientes convenciones (asumiendo siempre la separación por, al menos, un espacio en blanco):

- Operador de derivación: la regla se divide en dos partes separadas por una flecha, denotada como "->".
- La parte izquierda contiene exclusivamente un símbolo No Terminal (el generador). 
- La parte derecha contiene una o múltiples producciones separadas por el operador "|".
- Los símbolos dentro de una producción se delimitan entre ellos mediante espacios. Esto permite trabajar tanto con símbolos de un caracter (p.ej. "a"), como con palabras (p.ej. "pelicano"). Una producción consiste en una combinación libre de símbolos; aunque en el caso de las gramáticas CNF, una producción solo puede componerse de dos No Terminales, o de un Terminal. 
- El símbolo vacío se representa con una 'e' mínuscula.
- Se puede definir una CFG probabílistica (PCFG) añadiendo una probabilidad a cada producción. Se escribe al final de la producción, encerrada entre corchetes [<prob>] (p.ej. "A B [0.8]").

A continuación, se muestra un ejemplo de una gramática probabilística siguiendo este formato:

S -> A B [0.5]
A -> a [0.7] | b [0.3]
B -> b [1.0]

## 5. Descripción de las Extensiones Realizadas

### Conversor a Forma Normal de Chomsky

Este módulo contiene dos funciones principales: la encargada de detectar si una gramática está en CNF *es_cnf* y la que transforma la gramática *convertir_a_cnf* (y esta tiene una función auxiliar por cada paso).

La primera función es muy básica: lo único que hay que comprobar es que las reglas sean o del tipo "A -> B C" o "A -> a"; si hay alguna que incumple esta premisa, entonces no es CNF. Cabe destacar que se puede eliminar la llamada de esta función para usar en su lugar el "flag" *--cnf* (en el código se especifica la línea a cambiar), que se puede añadir para indicar al código que hace falta transformar la gramática. 
La segunda no es tan trivial, y sigue los siguientes pasos para transformar cualquier gramática libre de contexto a CNF:

- Crear nuevo símbolo inicial (suele ser redundante): crea un nuevo símbolo (p.ej. "S0") y crea una regla que produce el símbolo inicial antiguo a partir del nuevo (p.ej. "S0 -> S"). Sirve en casos muy concretos, como cuando el símbolo inicial se encontraba en alguna producción. 
- Aislar terminales: en el caso de una regla "S -> a B", se crea un símbolo No terminal X1 y se modifica "S -> X1 B" y se añade "X1 -> a".
- Binarizar reglas n-arias: misma lógica que en el anterior, dada la regla "S -> A B C", se modifica "S -> A D" y se añade "D -> B C".
- Eliminar carácteres vacios: eliminamos todos los símbolos vacios y las reglas "vacias" (p.ej. "A -> e").
- Eliminar reglas unitarias: aplicando la propiedad transitiva, si "A -> B" y "B -> c", entonces se convierte en "A -> c". 
- Eliminar reglas inalcanzables: paso añadido a posteriori porque, tras algunas pruebas, se descubrió que algunas reglas quedaban inalcanzables, y se eliminan para dejar limpia la gramática final. 

Finalmente cabe recalcar que la mayoria de estos pasos fueron extraídos del capítulo 18 del libro *Speech and Language Processing*, a excepción de las siguientes: crear nuevo símbolo inicial, eliminar carácteres vacios y eliminar reglas inalcanzables. Estas las añadimos porque en el libro no se tenian en cuenta ni el símbolo vacio ni que un símbolo inicial puede aparecer en una producción (y la última ya se ha explicado su razonamiento). 

### CKY probabilístico (PCKY)

Este módulo contiene toda la lógica del algoritmo CKY probabílistico (PCKY). Comparte el mismo código, a diferencia de estos pequeños cambios: 

- Al invertir la gramática, obviamente no se elimina la probabilidad. 
- En cada celda se añade, además de los símbolos, la probabilidad y un *backpointer* (se explica más adelante todo este proceso extra).
- En cada paso, si se añade un símbolo se: multiplican las probabilidades de las 2 celdas anteriores y la probabilidad de emisión del símbolo a añadir; en caso de ambiguedad, se escoge la regla con mayor probabilidad. 
- Al final, en vez de devolver un booleano para dictaminar si una palabra pertenece o no, se devuelve una probabilidad de formar esa palabra. 

## 6. Valoración del Aprendizaje Obtenido
A lo largo del trabajo dedicado a esta práctica hemos aprendido enormemente. No solo hemos mejorado nuestras habilidades programando dinámicamente, así como programando en general, sinó que hemos aprendido mucho de análisis sintáctico que hemos podido compaginar muy bien con nuestra asignatura de Procesamiento del Lenguaje Humano, donde una parte del temario fue dedicada a análisis sintáctico con CKY y PCKY. De hecho, algunas de las adiciones (como el árbol sintáctico) han sido inspiradas por la combinación de las dos asignaturas. 

Así pues, también hemos aprendido cosas nuevas menos relacionadas con la práctica, como a diseñar interfaces de línea de comandos con argumentos y "flags", así como a hacer tests automatizados. 

En conclusión, ha sido una práctica que nos ha parecido muy acertada, pues su impacto y ayuda en este cuadrimestre del grado ha sido substancial, ya que ha ayudado a reforzar y consolidar una parte de uno de los focos de este punto de la carrera: el procesamiento de lenguaje natural (NLP).


## 7. Otras Consideraciones Pertinentes
Además de los requisitos del enunciado, hemos implementado las siguientes funciones:

- Una forma de procesar palabras en lote: al usar el "flag" *--batch* se puede especificar un archivo del que extraer palabras para ejecutar el algoritmo con multiples palabras en una sola ejecución.
- Un analizador sintáctico: en el algoritmo de PCKY no nos hemos limitado a simplemente calcular probabilidades, sinó que hemos tomado el conocimiento de PLH para crear árboles sintácticos mediante el uso de *backpointers*. Así pues, también hemos preparado una gramática (gp4.txt) en la que definimos reglas sintácticas del castellano arbitrarias para probar el análisis sintáctico de frases, para probar todo el potencial del árbol sintáctico. No obstante, para poder procesar frases, hace falta usar el "flag" *--frase* (o *-f*), así como envolver la frase en comillas (p.ej: python main.py -p -f datos/gp4.txt "kenny duerme en el sofa"). 
- Un módulo de testing automatizando con la libreria pytest, con un total de 123 tests (combinando tests con múltiples ejecuciones por test). Este conjunto de tests es suficiente para demostrar que el algoritmo funciona sin fallos ni errores de ejecución, pese a su simplicidad. 

## Bibliografía

Jurafsky, D., & Martin, J. H. Speech and Language Processing. Capítulo 18: Context-Free Grammars and Constituency.

Wikipedia https://en.wikipedia.org/wiki/CYK_algorithm