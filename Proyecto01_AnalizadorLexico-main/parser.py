import ply.yacc as yacc 
from adaptadorLexer import adaptadorL

#Las funciones deben estar fuera para que funcione el PLY
tokens = (
            # Literales
            'ID', 'NUM', 'DECIMAL', 'TXT',
            # Palabras clave
            'FLOAT', 'INT', 'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'AND', 'OR', 'NOT',
            'SWITCH', 'DO', 'DEFAULT', 'CASE', 'BOOLEAN', 'TRY', 'CATCH',
            'MAIN', 'ELIF', 'PRINT', 'INPUT', 'READ', 'DEF', 'MUL',
            # Operadores aritméticos
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
            # Operadores de comparación
            'EQ', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT', 'MOD',
            'INC', 'DEC', 'PLUSEQ', 'MINUSEQ',
            # Especiales
            'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
            'ASSIGN', 'NEG', 'AMP', 'TILDE', 'DEG',
            # Puntuación
            'COMMA', 'COLON', 'SEMI',
            # Especial
            'NEWLINE'
        )

#Todas las producciones escritas en funciones para que PLY las identifique
#Producciones para contener los saltos de línea
def p_nl_single(p):
    "nl : NEWLINE"
    p[0] = None
 
def p_nl_multi(p):
    "nl : NEWLINE nl"
    p[0] = None

#S' -> S S' | eps
def p_sprime_recurse(p):
    "sprime : s sprime"
    p[0] = ('sprime', p[1], p[2])
 
def p_sprime_empty(p):
    "sprime : empty"
    p[0] = None

def p_sprime_nuevaLinea(p):
    "sprime : nl sprime"
    p[0] = p[2]

#Comienzo de las producciones de S
def p_s_if(p):
    "s : IF LPAREN a RPAREN c b"
    # Sin 'nl': el '}' de 'c' cierra la sentencia.
    p[0] = ('if', p[3], p[5], p[6])
 
def p_s_while(p):
    "s : WHILE LPAREN a RPAREN c"
    # Igual que if: el bloque 'c' ya delimita el while.
    p[0] = ('while', p[3], p[5])
 
def p_s_for(p):
    "s : FOR LPAREN k SEMI a SEMI i RPAREN c"
    p[0] = ('for', p[3], p[5], p[7], p[9])
 
def p_s_print(p):
    "s : PRINT LPAREN e RPAREN nl"
    # Sentencia simple → necesita terminador de línea.
    p[0] = ('print', p[3])

def p_s_print_linea(p):
    "s : PRINT LPAREN e RPAREN"
    p[0] = ('print', p[3])
 
def p_s_return(p):
    "s : RETURN e nl"
    p[0] = ('return', p[2])

def p_s_return_inline(p):
    "s : RETURN e"
    p[0] = ('return', p[2])
 
def p_s_k(p):
    "s : k nl"
    p[0] = p[1]

def p_s_k_inline(p):
    "s : k"
    p[0] = p[1]
 
def p_s_l(p):
    # def es una estructura de bloque → sin 'nl' al final.
    "s : l"
    p[0] = p[1]

def p_s_call(p):
    "s : ID LPAREN o RPAREN nl"
    p[0] = ('call', p[1], p[3])

def p_s_call_inline(p):
    "s : ID LPAREN o RPAREN"
    p[0] = ('call', p[1], p[3])

#Producciones de C
def p_c_inline(p):
    "c : LBRACE sprime RBRACE"
    # Bloque en una sola línea: { print(x) }
    p[0] = ('block', p[2])
 
def p_c_open(p):
    "c : LBRACE nl sprime RBRACE"
    # '{' con salto, pero '}' pegado al último token.
    p[0] = ('block', p[3])
 
def p_c_full(p):
    "c : LBRACE nl sprime nl RBRACE"
    # Forma estándar multilínea con saltos en ambos extremos.
    p[0] = ('block', p[3])

#A -> E F E D
def p_a(p):
    "a : e f e d"
    p[0] = ('condition', p[1], p[2], p[3], p[4])

#B -> elif (A) C B | else C | eps
def p_b_elif(p):
    "b : ELIF LPAREN a RPAREN c b"
    p[0] = ('elif', p[3], p[5], p[6])
 
def p_b_else(p):
    "b : ELSE c"
    p[0] = ('else', p[2])

def p_b_else_nl(p):
    "b : nl ELSE c"          # ← absorbe el NEWLINE antes del else
    p[0] = ('else', p[3])

def p_b_elif_nl(p):
    "b : nl ELIF LPAREN a RPAREN c b"   # ← absorbe el NEWLINE antes del elif
    p[0] = ('elif', p[3], p[5], p[6])
 
def p_b_empty(p):
    "b : empty"
    p[0] = None

#D -> and E F E D | or E F E D | eps
def p_d_and(p):
    "d : AND e f e d"
    p[0] = ('and', p[2], p[3], p[4], p[5])
 
def p_d_or(p):
    "d : OR e f e d"
    p[0] = ('or', p[2], p[3], p[4], p[5])
 
def p_d_empty(p):
    "d : empty"
    p[0] = None

#E -> G E'
def p_e(p):
    "e : g eprime"
    p[0] = ('expr', p[1], p[2])
 
def p_eprime_plus(p):
    "eprime : PLUS g eprime"
    p[0] = ('+', p[2], p[3])
 
def p_eprime_minus(p):
    "eprime : MINUS g eprime"
    p[0] = ('-', p[2], p[3])
 
def p_eprime_empty(p):
    "eprime : empty"
    p[0] = None

#F -> comparadores
def p_f_geq(p):
    "f : GEQ"
    p[0] = '>='
 
def p_f_eq(p):
    "f : EQ"
    p[0] = '=='
 
def p_f_neq(p):
    "f : NEQ"
    p[0] = '!='
 
def p_f_leq(p):
    "f : LEQ"
    p[0] = '<='
 
def p_f_lt(p):
    "f : LT"
    p[0] = '<'
 
def p_f_gt(p):
    "f : GT"
    p[0] = '>'

#G -> H G'
def p_g(p):
    "g : h gprime"
    p[0] = ('term', p[1], p[2])
 
def p_gprime_times(p):
    "gprime : TIMES h gprime"
    p[0] = ('*', p[2], p[3])
 
def p_gprime_divide(p):
    "gprime : DIVIDE h gprime"
    p[0] = ('/', p[2], p[3])
 
def p_gprime_mod(p):
    "gprime : MOD h gprime"
    p[0] = ('%', p[2], p[3])
 
def p_gprime_empty(p):
    "gprime : empty"
    p[0] = None

#H
def p_h_paren(p):
    "h : LPAREN e RPAREN"
    p[0] = p[2]
 
def p_h_call(p):
    "h : ID LPAREN o RPAREN"
    p[0] = ('call', p[1], p[3])
 
def p_h_id(p):
    "h : ID"
    p[0] = ('id', p[1])
 
def p_h_num(p):
    "h : NUM"
    p[0] = ('int', p[1])
 
def p_h_float(p):
    "h : DECIMAL"
    p[0] = ('float', p[1])
 
def p_h_txt(p):
    "h : TXT"
    p[0] = ('txt', p[1])
 
def p_h_bool(p):
    "h : BOOLEAN"
    p[0] = ('boolean', p[1])
 
def p_h_input(p):
    "h : INPUT LPAREN TXT RPAREN"
    p[0] = ('input', p[3])

#I
def p_i_assign(p):
    "i : ID ASSIGN e"
    p[0] = ('assign', p[1], p[3])
 
def p_i_inc(p):
    "i : ID INC"
    p[0] = ('inc', p[1])
 
def p_i_dec(p):
    "i : ID DEC"
    p[0] = ('dec', p[1])
 
def p_i_pluseq(p):
    "i : ID PLUSEQ e"
    p[0] = ('pluseq', p[1], p[3])
 
def p_i_minuseq(p):
    "i : ID MINUSEQ e"
    p[0] = ('minuseq', p[1], p[3])

#J - Los datos
 
def p_j_int(p):
    "j : INT"
    p[0] = 'int'
 
def p_j_float(p):
    "j : FLOAT"
    p[0] = 'float'
 
def p_j_bool(p):
    "j : BOOLEAN"
    p[0] = 'boolean'

#K - Asignación / Declaración
def p_k_assign(p):
    "k : ID ASSIGN e"
    p[0] = ('assign', p[1], p[3])
 
def p_k_decl(p):
    "k : j ID ASSIGN e"
    p[0] = ('decl', p[1], p[2], p[4])

def p_k_inc(p):
    "k : ID INC"
    p[0] = ('inc', p[1])

def p_k_dec(p):
    "k : ID DEC"
    p[0] = ('dec', p[1])

#L - Definición de función
def p_l(p):
    "l : DEF ID LPAREN m RPAREN c"
    p[0] = ('def', p[2], p[4], p[6])

#M, N - Parámetros formales
def p_m_id(p):
    "m : ID n"
    p[0] = ('param', p[1], p[2])
 
def p_m_empty(p):
    "m : empty"
    p[0] = None
 
def p_n_comma(p):
    "n : COMMA ID n"
    p[0] = ('param', p[2], p[3])
 
def p_n_empty(p):
    "n : empty"
    p[0] = None

#O, P - argumentos en llamada a función
def p_o_expr(p):
    "o : e p"
    p[0] = ('arg', p[1], p[2])
 
def p_o_empty(p):
    "o : empty"
    p[0] = None
 
def p_p_comma(p):
    "p : COMMA e p"
    p[0] = ('arg', p[2], p[3])
 
def p_p_empty(p):
    "p : empty"
    p[0] = None

#empty
def p_empty(p):
    "empty :"
    p[0] = None

#Errorsito
def p_s_error_nl(p):
    "s : error nl"
    print(f"  Recuperado: se descartó la sentencia errónea.")
    p[0] = None
    p.parser.errok()

def p_error(token):
    if token is None:
        print("Error sintáctico: fin de archivo inesperado.")
        return
    print(f"Error sintáctico en la línea {token.lineno}: token inesperado '{token.value}' ({token.type})")
    
    # Descartar tokens hasta encontrar un NEWLINE o RBRACE como punto seguro
    while True:
        tok = token.parser.token()
        if tok is None:
            break
        if tok.type in ('NEWLINE', 'RBRACE'):
            token.parser.restart()
            token.lexer.reinsert(tok)  #devuelve el token a la cola
            break


pi = yacc.yacc(start="sprime")

#Instancia del parser

class parserin:
    def __init__(self):
        self.parser = pi

    def analizar(self, lista_tokens):
        adaptador = adaptadorL(lista_tokens)
        adaptador.parser = self.parser
        return self.parser.parse(input=None, lexer=adaptador)
