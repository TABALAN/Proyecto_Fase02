Tony Balán - 1202124 Claudia Mejía - 1127224

----- Funcionamiento del proyecto ----- 
En la fase #2 el proyecto implementa:
1. Analizador léxico: lee un archivo de texto, construye lexemas y clasifica por tokens, detecando errores léxicos.
2. Adapatador de tokens: convierte la lista de diccionarios a objetos compatibles con PLY.
3. Analizador sintáctico: valida que los tokens respete la gramática, construyendo un árbol de derivación
----- Análisis de la gramática -----
La gramática tiene como objetivo definir la sintaxis del lenguaje y permitir la construcción del árbol de análisis. Con ella se interpreta de manera más precisa la lectura del código. Para este proyecto se modificó la gramática para un funcionamiento más robusto y exacto:

S’ -> S S’ | eps 
S -> if (A) C B | while (A) C | for (K; A; I) C | print(E) | return E | K | L | id(O)
A -> E F E D
B -> elsif (A) C B | else C | eps
C -> {S’}
D -> and E F E D | or E F E D | eps 
E -> GE’
E’ -> + G E’ | - G E’ | eps
F ->  == | != | <= | >= | < | >
G -> HG’
G’ -> * H G’ | / H G’ | % H G’ | eps
H -> (E) | id(O) | id | num | float | txt | bool | input(txt)
I -> id=E | id++ | id-- | id +=E | id -= E
J -> int | float | bool 
K -> id = E | J id = E
L -> def id(M) C
M -> id N | eps
N -> , id N | eps
O -> E P | eps
P -> , E P | eps

----- Ejecución del programa -----
Requisitos:
1. Python 3.8 o superior
2. Librería PLY (Python Lex-Yacc)
 Cómo instalar --> pip install ply
O si se usa el entorno virtual incluido en el repositorio:
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install ply

Cómo ejecutar: 
1. Editar la variable archivo en main.py con la ruta al archivo fuente que se desea analizar.
2. Ejecutar:
   * python main.py

----- Manejo de errores -----
El parser maneja errores en 2 niveles:
1. Se llama a p_error(token) por PLY cuando el token no coincide con ninguna producción creada.
- Reporta el error con número de lpinea y el token
- Descarta el token inválida y se sincroniza hasta encontrar un punto correcto
2. p_s_error recupera la gramática
- Le indica a PLY después de sincronizarse al final de la línea, puede completar la producción y el árbol sigue construyéndose después de esa sentencia
