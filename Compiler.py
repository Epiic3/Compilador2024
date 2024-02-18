
'''
Rust compiler developed and implemented on python by:

1- Manuel Corona Perez.
2- Guillermo Bertrand Hernandez.
3- Erick Perez Coronado.
'''

class LexicalAnalyzer:
    
    ERROR = -1
    ACP = 999
    BOOLEAN_VALUES = ['true', 'false']
    RESERVED_WORDS = [
        'function', 'main', 'println', 'println!', 'int', 'const', 
        'float', 'bool', 'string', 'let', 'if', 'else if', 'for', 
        'in', 'while', 'loop', 'return', 'read', 'break', 'continue'
    ]
    ARITHMETIC_OPERATORS = ['+', '-', '*', '%']
    RELATIONAL_OPERATORS = ['<', '>']
    INVISIBLE_CHARACTERS = [' ', '\t', '\n']
    DELIMITERS = ['{', '}', '[', ']', '(', ')', ';', ',', ':', '.']
    SPECIAL_CHARACTERS = ['#', '$', '¿', '?', '^', '¡']
    TRANSITION_MATRIX = [
        [    1,     1,    21,     2,     7,     8,    10,    12,    16,    20,    18,    14,  21,   5], #0
        [    1,     1,   ACP,     1,   ACP,   ACP,     1,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #1
        [  ACP,   ACP,     3,     2,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #2
        [ERROR, ERROR, ERROR,     4, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ACP, ACP], #3
        [  ACP,   ACP,   ACP,     4,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #4
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP,   6], #5  
        [    6,     6,     6,     6,     6,     6,     6,     6,     6,     6,     6,     6,   6,   6], #6
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #7
        [ERROR, ERROR, ERROR, ERROR, ERROR,     9, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], #8
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #9
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,    11,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #10
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #11
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,    13,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #12
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #13
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,    15, ACP, ACP], #14
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #15
        [   16,    16,    16,    16,    16,    16,    16,    16,    17,    16,    16,    16,  16,  16], #16
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #17
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,    19,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #18
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #19
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #20
        [  ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP,   ACP, ACP, ACP], #21
    ]

    #Constructor: Initialize every var.
    def __init__(self):
        pass

    def logError(self, type, message):
        print(type, message)

    def getColumn(self, c):
        if c.isalpha():                      return 0
        elif c == '_':                       return 1
        elif c == '.':                       return 2
        elif c.isdigit():                    return 3
        elif c in self.ARITHMETIC_OPERATORS: return 4
        elif c == '&':                       return 5
        elif c == '!':                       return 6
        elif c == '=':                       return 7
        elif c == '"':                       return 8
        elif c in self.DELIMITERS:           return 9
        elif c in self.RELATIONAL_OPERATORS: return 10
        elif c == '|':                       return 11
        elif c in self.SPECIAL_CHARACTERS:   return 12
        elif c in '/':                       return 13
        elif c in self.INVISIBLE_CHARACTERS: return 0
        else: self.logError(c, " No es válido en el alfabeto del lenguaje")
        return self.ERROR
    
    def analyze(self, input):
       
        currentIndex = 0
        
        while input != '.' and currentIndex < len(input):

            #Declare vars to analyze input
            currentState = 0
            previousState = 0
            lexeme = ''
            token = ''

            #Check every character as long as there are still chars and current state isn't acp or error.
            while currentIndex < len(input) and currentState != self.ACP and currentState != self.ERROR:
                #In case of invisible characters at the beggining of the input, ignore them.
                while(input[currentIndex] in self.INVISIBLE_CHARACTERS and currentState == 0): 
                    currentIndex += 1
                #Get current char and move 1 position.
                currentChar = input[currentIndex]
                currentIndex += 1
            
                #If currently iterating a comment, get to the end 'till scape.
                while currentState == 6 and currentChar != '\n' and currentIndex < len(input):
                    currentChar = input[currentIndex]
                    currentIndex += 1
            
                #If just passed a comment, get back to initial state and continue iterating input.
                if currentState == 6 and currentIndex < len(input):
                    currentChar = input[currentIndex]
                    lexeme = ''
                    currentState = 0
                #If there is a blank, then break, next char could be a different token.
                if currentState != 6 and currentState != 16 and currentChar in self.INVISIBLE_CHARACTERS:
                    break
            
                #Get column of current char.
                column = self.getColumn(currentChar)

                if column >= 0 and column <= 13 and currentState != self.ERROR:
                    #Store previous state and go to next state
                    previousState = currentState
                    currentState = self.TRANSITION_MATRIX[currentState][column]
                    #And if is not equals to acp or error, concatenate char.
                    if currentState != self.ACP and currentState != self.ERROR: 
                        lexeme += currentChar

                if currentState == self.ACP or currentState == self.ERROR:
                    #If currently in acp state, do an unget.
                    if currentState == self.ACP:
                        currentIndex -= 1
                    break

            #if current state isn't acp o error, set previous state.
            if currentState != self.ACP and currentState != self.ERROR: 
                previousState = currentState
            
            if previousState == 1:
                token = 'Identifier:'
                if lexeme in self.RESERVED_WORDS: token = 'Reserved:'
                elif lexeme in self.BOOLEAN_VALUES: token = 'Boolean:'
            elif previousState == 2:
                token = 'Integer:'
            elif currentState == 3 or currentState == 4:
                token = 'Float:'
                if currentState == 3: self.logError('Error léxico ', lexeme + ' decimal incompleto')
            elif previousState == 5 or previousState == 7:
                token = 'Arithmetic-operator:'
            elif previousState == 6:
                token = 'Comment:'
                lexeme = ''
            elif previousState == 9 or previousState == 10 or previousState == 15:
                token = 'Logical-operator:'
            elif previousState == 11 or previousState == 13 or previousState == 18 or previousState == 19:
                token = 'Relational-operator:'
            elif previousState == 12:
                token = 'Assignment operator:'
            elif previousState == 17:
                token = 'String:'
            elif previousState == 20:
                token = 'Delimiter:'
            elif previousState == 21:
                token = 'Special-character:'
            else: 
                token = 'ERROR:'
            
            print(token, lexeme)

if __name__ == "__main__":

    #Get input from user.
    input = input("Dame una entrada (. = salir): ")
    #Instantiate lexical analyzer
    lexicalAnalyzer = LexicalAnalyzer()
    #And analyze input.
    lexicalAnalyzer.analyze(input)

    