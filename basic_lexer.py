from sly import Lexer


class BasicLexer(Lexer):
    """BASIC Lexer class for generating tokens."""
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ}

    # Ignore spaces and tabs.
    ignore = "\t "

    # One-character literals.
    literals = {'=', '+', '-', '*', '/', '(', ')', ',', ';'}

    # Define tokens (regular expressions REGEXES).
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        """When we get a number."""
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        """Commenting in BASIC should just be ignored."""
        pass

    @_(r'\n+')
    def newline(self, t):
        """Count newlines for better error handling."""
        self.lineno = t.value.count('\n')

    def error(self, t):
        """Handling errors in the code."""
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == '__main__':
    lexer = BasicLexer()

    # Keep track of variables when interpreter is running.
    env = {}

    # Infinite loop that accepts code.
    while True:
        try:
            data = input('BASIC> ')
        except EOFError:
            break

        # If we got the code successfully - generate tokens for parser.
        if data:
            lex = lexer.tokenize(text)

            # For now, just print the tokens (We haven't implemented parser yet!)
            for token in lex:
                print(token)
