ERR = -1
ACP = 999
entrada = '' 
idx = 0
bERR = False
ctelog = ['verdadero', 'falso']
palRes = ['fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'const',
          'decimal', 'logico', 'alfabetico', 'sea', 'si', 'sino', 
          'para', 'en', 'mientras', 'ciclo', 'regresa', 'leer', 'interrumpe', 
          'continua']
matran = [
    #let  _    .    dig  +-*% &    !    =    "    /    ><   |
    [1,   1,   ERR, 2,   7,   8,   9,   14,  12,  5,   15,  10 ], #0
    [1,   1,   ACP, 1,   ACP, ACP, 1,   ACP, ACP, ACP, ACP, ACP], #1
    [ACP, ACP, 3,   2,   ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #2
    [ERR, ERR, ERR, 4,   ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #3
    [ACP, ACP, ACP, 4,   ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #4
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, 6,   ACP, ACP], #5  
    [6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6  ], #6
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #7
    [ERR, ERR, ERR, ERR, ERR, 9,   ERR, ERR, ERR, ERR, ERR, ERR], #8
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, 17,  ACP, ACP, ACP, ACP], #9
    [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, 9  ], #10
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #11
    [12,  12,  12,  12,  12,  12,  12,  12,  13,  12,  12,  12 ], #12
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #13
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #14
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, 16,  ACP, ACP, ACP, ACP], #15
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #16
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #17
]
opa = ['+', '-', '*', '%']

def erra(tipo, desc):
    print(tipo, desc)
    bERR = True

def colCar( c ):
    if c.isalpha():     return 0
    if c == '_':        return 1
    if c == '.':        return 2
    if c.isdigit():     return 3
    if c in opa:        return 4
    if c == '&':        return 5
    if c == '!':        return 6
    if c == '=':        return 7
    if c == '"':        return 8
    if c == '/':        return 9
    if c in ['<', '>']: return 10
    if c == '|':        return 11
    if c in [' ', '\t', '\n']: return 0
    print(c ,'NO es valido en el alfabeto del Lenguaje')
    return ERR

def lexico():
    global entrada, ERR, ACP, matran, idx
    estado = 0
    estAnt = 0
    lex = ''
    tok = ''
    while idx < len(entrada) and estado != ERR and estado != ACP:
        while(entrada[idx] in [' ', '\n', '\t'] and estado == 0):
            idx += 1

        x = entrada[idx]
        idx += 1

        while estado == 6 and x != '\n' and idx < len(entrada):
            x = entrada[idx]
            idx += 1

        if estado == 6 and idx < len(entrada):
            x = entrada [idx]
            lex = ''
            estado = 0
        if x in [' ', '\n', '\t'] and estado != 6: 
            break
        col = colCar(x)
        if col>=0 and col <= 11 and estado !=ERR:
            estAnt = estado
            estado = matran[estado][col]
            if estado != ACP and estado != ERR: 
                lex += x

        if estado == ACP or estado == ERR:
            if estado == ACP: idx -= 1
            break

    if estado != ACP and estado != ERR: estAnt = estado
    if estado == 3:
        tok = 'Dec'
        erra('Error Lexico', lex + ' cte decimal incompleta')
    elif estAnt == 1: 
        tok = 'Ide'
        if lex in palRes: tok = 'Res'
        elif lex in ctelog: tok = 'CtL'
    elif estAnt == 2:
        tok = 'Ent'
    elif estAnt == 4:
        tok = 'Dec'
    elif estAnt == 9:
        tok = 'OpL'
    elif estado == 6: 
        tok = 'Com'
        lex = ''
    elif estAnt == 17:
        tok = 'OpR'
    else: tok = 'ERR'

    return tok, lex

if __name__ == '__main__':
    entrada = input('Dame una entrada [.]=Salir: ')
    while entrada != '.' and idx < len(entrada):
        token, lexema = lexico()
        print(token, lexema)