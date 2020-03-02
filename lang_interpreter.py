from lolkCore.lang_lexer import LangLexer
from lolkCore.lang_parser import LangParser
from lolkCore.lang_formatter import LangFormatter
from lolkCore.lang_settings import LangSettings
from lolkCore.lang_execute import Execute


# Start interpreter.
if __name__ == '__main__':
    lexer = LangLexer()
    parser = LangParser()

    # For formatting the code so that the Execute class can understand it.
    formatter = LangFormatter()
    settings = LangSettings()

    # Keep track of variables when interpreter is running.
    env = {}

    # Count lines and store all code.
    curr_lineno = 1
    all_code = ['<EOF>']

    in_func_state = False
    func_stmts = []
    func_name = ''
    # Infinite loop that accepts code.
    while True:
        code_already_inserted = False
        try:
            if not in_func_state:
                data = input('LOLK> ')
                formatted_code = formatter.format_code(data)
                parsed = parser.parse(lexer.tokenize(data))
                if parsed is None:
                    continue
                if parsed[0] == 'fun_def':
                    func_name = parsed[1]
                    in_func_state = True
                    continue
            else:
                # We are currently defining function code,
                # create a temporary input field for code for the function.
                all_code.insert(len(all_code)-1, data)
                code_already_inserted = True
                while in_func_state:
                    func_code = input("...\t  ")
                    if func_code == '':
                        # Quit defining code.
                        in_func_state = False
                    
                    # Add parsed tree to func_stmts.
                    parsed = parser.parse(lexer.tokenize(func_code))
                    if not parsed is None:
                        func_stmts.append(parsed)
                        all_code.insert(len(all_code)-1, func_code)
                
                # Finally, add the function to the environment.
                env[func_name] = func_stmts
                # Reset func statements for new use.
                func_stmts = []
        except EOFError:
            break
        
        print(env)
        # Add code to all code list if it is not empty.
        if data != '' and not code_already_inserted:
            all_code.insert(len(all_code)-1, data)
        
        # If we got data successfully - generate tokens for parser.
        if data:
            # Parse and generate tree.
            tree = parser.parse(lexer.tokenize(data))

            # Run parsed tree and generate output.
            Execute(tree, env, all_code, curr_lineno, is_compiling=False)
            curr_lineno += 1
