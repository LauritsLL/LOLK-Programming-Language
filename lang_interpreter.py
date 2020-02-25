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
            data = input('LOLK> ')
        except EOFError:
            break

        # If we got data successfully - generate tokens for parser.
        if data:
            # Parse and generate tree.
            tree = parser.parse(lexer.tokenize(data))

            # Run parsed tree and generate output.
            Execute(tree, env)


# Run compiler on a file.
if run_file_compiler:
    lexer = LangLexer()
    parser = LangParser()

    # Keep track of variables when compiler is running.
    env = {}

    while(True):
        prompt = "What file do you want to use (Starting in root directory "
        prompt += os.getcwd() + ") "
        file_to_use = input(prompt)
        program = os.path.join(os.getcwd(), file_to_use)
        if os.path.exists(program) and os.path.isfile(program):
            # The file exists; compile and run.
            print("Running specified file with compiler...\n\n")
            print("\tSTART OF PROGRAM")
            print("----------------------------------------\n\n")
            
            # Split code up into seperate lines and add End Of File to end of list,
            # to know when we are done executing the file.
            code_lines = open(program, 'r').read().split("\n")
            code_lines.append("<EOF>")

            # Go through every line of code and execute it.
            for code in code_lines:
                # If we get <EOF> break loop.
                if code == "<EOF>":
                    break
                tree = parser.parse(lexer.tokenize(code))

                # Run parsed tree and generate output.
                Execute(tree, env)
            
            
            # Break out of loop after execution.
            break
        else:
            # File doesn't exist - Inform user.
            print("File specified in directory " + program + " does not exist!")
