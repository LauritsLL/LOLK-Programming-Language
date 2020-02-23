from sly import Lexer


class LangLexer(Lexer):
    """Lexer class for generating tokens. - LANG"""
    tokens = {NAME, NUMBER, STRING, PRINT}

    # Ignore spaces and tabs.
    ignore = "\t "

    # One-character literals.
    literals = {'=', '+', '-', '*', '/', '(', ')', ',', ';'}

    # Define tokens (regular expressions REGEXES).
    PRINT = r'show'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'\".*?\"'

    @_(r'\d+')
    def NUMBER(self, t):
        """Convert NUMBER to python number."""
        t.value = int(t.value)
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

# ZOMBIE CODE: TEST LEXING TOKENS (DON'T USE)
# if __name__ == '__main__':
#    lexer = LangLexer()

#    # Infinite loop that accepts code.
#    while True:
#        try:
#            data = input('LANG> ')
#        except EOFError:
#            break

#        # If we got the code successfully - generate tokens for parser.
#        if data:
#            # Print tokens for now.
#            tokens = lexer.tokenize(data)
#            for token in tokens:
#                print(token)
