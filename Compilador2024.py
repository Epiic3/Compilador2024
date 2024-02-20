import pathlib

class AnalizadorLexico:

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

    #Constructor
    def __init__(self):
        pass

    def logError(self, type, message):
        print(type, message)

    def getColumn(self, c) :
        if c.isalpha(): return 0
        elif c == '_': return 1
        elif c == '.': return 2
        elif c.isdigit(): return 3
        elif c in self.OPERADORES_ARITMETICOS: return 4
        elif c == '&': return 5
        elif c == '!': return 6
        elif c == '=': return 7
        elif c == '"': return 8
        elif c in self.DELIMITADORES: return 9
        elif c in self.OPERADORES_RELACIONALES: return 10
        elif c == '|': return 11
        elif c in self.CARACTERES_ESPECIALES: return 12
        elif c == '/': return 13
        elif c in self.CARACTERES_INVISIBLES: return 0
        else: self.logError(c, " No es valido en el alfabeto del lenguaje")
        return self.ERR

    def lexico(self, entrada):

        index = 0

        while entrada != '.' and index < len(entrada):

            estado = 0
            estadoAnterior = 0
            lexico = ''
            token = ''

            while index < len(entrada) and estado != self.ERR and estado != self.ACP:
                while entrada[index] in self.CARACTERES_INVISIBLES and estado == 0:
                    index += 1
                
                currentChar = entrada[index]
                index += 1

                while estado == 6 and currentChar != '\n' and index < len(entrada):
                    currentChar = entrada[index]
                    index += 1

                if estado == 6 and index < len(entrada):
                    currentChar = entrada[index]
                    lexico = ''
                    estado = 0

                if estado != 6 and estado != 16 and currentChar in self.CARACTERES_INVISIBLES:
                    break

                columna = self.getColumn(currentChar)

                if columna >= 0 and columna <= 13 and estado != self.ERR:
                    estadoAnterior = estado
                    estado = self.matran[estado][columna]
                    if estado != self.ACP or estado != self.ERR:
                        lexico += currentChar

                if estado == self.ACP and estado == self.ERR:
                    index -= 1
                    break
            
            if estado != self.ACP and estado != self.ERR:
                estadoAnterior = estado

            if estadoAnterior == 1:
                token = 'Identificador:'
                if lexico in self.PALABRAS_RESERVADAS: token = 'Palabra reservada:'
                elif lexico in self.BOOLEANOS: token = 'Booleando:'
            elif estadoAnterior == 2:
                token = 'Integer:'
            elif estado == 3 or estado == 4:
                token = 'Float:'
                if estado == 3: self.logError('Error lexico', lexico + ' decimal incompleto')
            elif estadoAnterior == 5 or estadoAnterior == 7:
                token = 'Operador aritmetico:'
            elif estadoAnterior == 6:
                token = 'Comment:'
                lexico = ''
            elif estadoAnterior == 9 or estadoAnterior == 10 or estadoAnterior == 15:
                token = 'Operador lógico:'
            elif estadoAnterior == 11 or estadoAnterior == 13 or estadoAnterior == 18 or estadoAnterior == 19:
                token = 'Operador relacional:'
            elif estadoAnterior == 12:
                token = 'Operador de asignación:'
            elif estadoAnterior == 17:
                token = 'String:'
            elif estadoAnterior == 20:
                token = 'Delimitador'
            elif estadoAnterior == 21:
                token = 'Caracter especial'
            else:
                token = 'Error'

            print(token, lexico)

if __name__ == "__main__":
    # #Instantiate lexical analyzer
    analizadorLexico = AnalizadorLexico()

    #Get input from user and analyze it.
    # input = input("Dame una entrada (. = salir): ")
    # lexicalAnalyzer.analyze(input)
    
    #Get file to open.
    fileName = input("Ingresa el nombre del archivo (.icc): ")
    #If file name does not end with the correct extension.
    while not fileName.endswith(".icc"): fileName = input("Ingresa el nombre del archivo (.icc): ")
    #Open file.
    with open(str(pathlib.Path(__file__).parent.resolve()) + "/" + fileName, 'r') as file:
        rows = file.readlines()
        input = ''
        #Store every single line in one input.
        for row in rows: input += row
        print("\n" + input + "\n")
        #And analyze input.
        analizadorLexico.lexico(input)
        #close file
        file.close()  

