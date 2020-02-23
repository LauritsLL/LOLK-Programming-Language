import os

from lang_lexer import LangLexer
from lang_parser import LangParser
from lang_execute import Execute


# Use interpreter or run compiler on file?
use_interpreter = False
run_file_compiler = False

inter_or_comp = input("Use 'interpreter' or run 'compiler' on file? ")
if inter_or_comp.lower() == "interpreter":
    use_interpreter = True
elif inter_or_comp.lower() == "compiler":
    run_file_compiler = True


# Only if the user wants to use the interpreter.
if __name__ == '__main__' and use_interpreter:
    lexer = LangLexer()
    parser = LangParser()

    # Keep track of variables when interpreter is running.
    env = {}

    # Infinite loop that accepts code.
    while True:
        try:
            data = input('LANG> ')
        except EOFError:
            break

        # If we got data successfully - generate tokens for parser.
        if data:
            # Parse and generate tree and run code!
            tree = parser.parse(lexer.tokenize(data))

            # Execute code!
            Execute(tree, env)


# Run compiler on a file.
if run_file_compiler:
    prompt = "What file do you want to use (Starting in root directory "
    prompt += os.getcwd() + ") "
    file_to_use = input(prompt)
    print("Running specified file with compiler...\n\n")
    print("\tSTART OF PROGRAM")
    print("----------------------------------------\n\n")

    # CODE FOR COMPILING AND RUNNING A FILE HERE.