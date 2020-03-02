from sly import Lexer


class LangLexer(Lexer):
    """Lexer class for generating tokens."""
    tokens = {
        NAME, NUMBER, STRING, PRINT, INPUT, EXIT, 
        CONV_STR, IF, THEN, ELSE,
        EQEQ, GREATER, LESSER, GE, LE, CONCATENATE,
        FUNCTION, ARROW,
        }

    # Ignore spaces.
    ignore = " "

    # One-character literals.
    literals = {'=', '+', '-', '*', '/', '(', ')', ',', ';'}

    # Define tokens (regular expressions REGEXES).
    PRINT = r'show'
    # Keyword to exit program.
    EXIT = r'exit'
    # Convert to string.
    CONV_STR = r'string'
    # Function def.
    FUNCTION = r'fun'
    ARROW = r'-->'

    # Input.
    INPUT = r'get_input'
    
    # Comparison.
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'

    # Comparison signs.
    CONCATENATE = r'\+\+'
    EQEQ = r'=='
    GE = r'>='
    LE = r'<='
    GREATER = r'>'
    LESSER = r'<'

    # Variable name.
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'\".*?\"'

    @_(r'\d+')
    def NUMBER(self, t):
        """Convert NUMBER to python number."""
        t.value = int(t.value)
        return t
    
    @_(r'\".*?\"')
    def STRING(self, t):
        """Format string without quotes."""
        t.value = t.value[1:][:-1]
        return t

    @_(r'!--.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        """Count newlines for better error handling."""
        self.lineno = t.value.count('\n')

    def error(self, t):
        """Handling errors in the code."""
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

#ZOMBIE CODE: TEST LEXING TOKENS (USE WITH CAUTION)
# if __name__ == '__main__':
#     lexer = LangLexer()

#     # Infinite loop that accepts code.
#     while True:
#         try:
#             data = input('LOLK> ')
#         except EOFError:
#             break

#         # If we got the code successfully - generate tokens for parser.
#         if data:
#             # Print tokens for now.
#             tokens = lexer.tokenize(data)
#             for token in tokens:
#                 print(token)
