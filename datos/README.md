#  ARCHIVOS DE INPUT

Este directorio contiene 2 tipos de archivo de input:

- Archivo de gramática: archivo txt que contiene una gramática CFG.
- Archivo de palabras: archivo txt que contiene palabras para utilizar como input usando la **flag** *--batch*.

## Formato

El formato de cada arxivo de gramática es el siguiente:

S -> <P1> [prob] | <P2> [prob] | ... | <Pi> [prob]
NT1 -> <P1> [prob] | <P2> [prob] | ... | <Pi> [prob]
.
.
.
NTi -> <P1> [prob] | <P2> [prob] | ... | <Pi> [prob]

donde:

- *S* es el No Terminal inicial.
- *NT* es un símbolo No Terminal.
- *P* representa cualquier producción (**Los símbolos en una producción deben estar separados por espacios**). (ejs. *a*, *X A*, *A B C*, etc).
- *[prob]* es opcional (PCKY) y representa la probabilidad de cada producción.