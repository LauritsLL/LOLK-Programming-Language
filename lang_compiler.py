import os

from lolkCore.lang_lexer import LangLexer
from lolkCore.lang_parser import LangParser
from lolkCore.lang_settings import LangSettings
from lolkCore.lang_execute import Execute
from lolkCore.lang_formatter import LangFormatter


def check_for_keywords(formatted_code_line):
    """Check for keywords."""
    settings = LangSettings()
    # Ignore code lines that has <INFUNC> in it.
    if formatted_code_line.find(settings.in_function) != -1:
        return (True, 'ignore')


# Run compiler on a file.
if __name__ == '__main__':
    lexer = LangLexer()
    parser = LangParser()

    # For formatting the code so that the Execute class can understand it.
    formatter = LangFormatter()

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

            # Count lines.
            curr_lineno = 1

            # Go through every line of code and execute it.
            for code in code_lines:
                # If we get <EOF> break loop.
                if code == "<EOF>":
                    break
                
                formatted_code = formatter.format_code(code)
                # Check for keywords.
                k = check_for_keywords(formatted_code)
                if k == (True, 'ignore'):
                    # If the current line of code is in a function don't run.
                    continue
                
                tree = parser.parse(lexer.tokenize(formatted_code))

                # Run parsed tree and generate output.
                Execute(tree, env, code_lines, curr_lineno)
                curr_lineno += 1

            
            # Break out of loop after execution.
            break
        else:
            # File doesn't exist - Inform user.
            print("File specified in directory " + program + " does not exist!")
