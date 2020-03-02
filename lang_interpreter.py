import os

from lolkCore.lang_lexer import LangLexer
from lolkCore.lang_parser import LangParser
from lolkCore.lang_execute import Execute


# Start interpreter.
if __name__ == '__main__':
    lexer = LangLexer()
    parser = LangParser()

    # Keep track of variables when interpreter is running.
    env = {}

    # Count lines and store all code.
    curr_lineno = 1
    all_code = ['<EOF>']

    # Infinite loop that accepts code.
    while True:
        try:
            data = input('LOLK> ')
        except EOFError:
            break
        
        # Add code to all code list if it is not empty.
        if data != '':
            all_code.insert(len(all_code)-1, data)
        
        # If we got data successfully - generate tokens for parser.
        if data:
            # Parse and generate tree.
            tree = parser.parse(lexer.tokenize(data))

            # Run parsed tree and generate output.
            Execute(tree, env, all_code, curr_lineno)
            curr_lineno += 1
