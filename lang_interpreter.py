import os

from lang_lexer import LangLexer
from lang_parser import LangParser
from lang_execute import Execute


# Start interpreter.
if __name__ == '__main__':
    lexer = LangLexer()
    parser = LangParser()

    # Keep track of variables when interpreter is running.
    env = {}

    # Infinite loop that accepts code.
    while True:
        try:
            data = input('LOLK> ')
        except EOFError:
            break

        # If we got data successfully - generate tokens for parser.
        if data:
            # Parse and generate tree.
            tree = parser.parse(lexer.tokenize(data))

            # Run parsed tree and generate output.
            Execute(tree, env)
