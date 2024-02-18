ERR = -1
ACP = 999
BOOLEANOS = ['true', 'false']
PALABRAS_RESERVADAS = [
    'function', 'main', 'println', 'println!', 'int', 'const', 
    'float', 'bool', 'string', 'let', 'if', 'else if', 'for', 
    'in', 'while', 'loop', 'return', 'read', 'break', 'continue'
]
OPERADORES_ARITMETICOS = ['+', '-', '*', '%', '^']
OPERADORES_RELACIONALES = ['<', '>']
CARACTERES_INVISIBLES = [' ', '\n', '\t']
DELIMITADORES = ['{', '}', '[', ']', '(', ')', ':', ';', ',', '.']
CARACTERES_ESPECIALES = ['#', '$', '¿', '?', '^', '¡']

matran = [
    #a-z    _    .  num +-*/    &    !    =    "   [(   <>    | $#^?    /
    [  1,   1,  21,   2,   7,   8,  10,  12,  16,  20,  18,  14,  21,   5], #0
    [  1,   1, ACP,   1, ACP, ACP,   1, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #1
    [ACP, ACP,   3,   2, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #2
    [ERR, ERR, ERR,   4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #3
    [ACP, ACP, ACP,   4, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #4
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,   6], #5
    [  6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6], #6
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #7
    [ERR, ERR, ERR, ERR, ERR,   9, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #8
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #9
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  11, ACP, ACP, ACP, ACP, ACP, ACP], #10
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #11
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP, ACP, ACP, ACP], #12
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #13
    [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  15, ERR, ERR], #14
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #15
    [ 16,  16,  16,  16,  16,  16,  16,  16,  17,  16,  16,  16,  16,  16], #16
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #17
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  19, ACP, ACP, ACP, ACP, ACP, ACP], #18
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #19
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #20
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #21
]

def getColumn(c) :
    if c.isalpha(): return 0
    elif c == '_': return 1
    elif c == '.': return 2
    elif c.isdigit(): return 3
    elif c in OPERADORES_ARITMETICOS: return 4
    elif c == '&': return 5
    elif c == '!': return 6
    elif c == '=': return 7
    elif c == '"': return 8
    elif c in DELIMITADORES: return 9
    elif c in OPERADORES_RELACIONALES: return 10
    elif c == '|': return 11
    elif c in CARACTERES_ESPECIALES: return 12
    elif c == '/': return 13
    elif c in CARACTERES_INVISIBLES: return 0
    else: print("No es valido en el alfabeto del lenguaje")
    return ERR








