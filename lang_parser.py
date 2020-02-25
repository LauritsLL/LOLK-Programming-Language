from sly import Parser

from lang_lexer import LangLexer


class LangParser(Parser):
    tokens = LangLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = {}

    @_(r'')
    def statement(self, p):
        pass
    
    ##### VARIABLE DECLARATION #####

    @_(r'NAME "=" expr')
    def var_assign(self, p):
        """Assign an "expression" variable. (Numbers, calculations, etc.)"""
        return ('var_assign', p.NAME, p.expr)

    @_(r'NAME "=" STRING')
    def var_assign(self, p):
        """Assign a string variable."""
        return ('var_assign', p.NAME, p.STRING)

    @_(r'var_assign')
    def statement(self, p):
        """Request for variable assignation. Assign it."""
        return p.var_assign
    
    ##### END #####
    ##### PRINT STATEMENTS #####

    @_(r'PRINT "(" STRING ")"')
    def statement(self, p):
        """Print a string."""
        return ('print_str', p.STRING)

    @_(r'PRINT "(" expr ")"')
    def statement(self, p):
        """Print an expression."""
        return ('print_expr', p.expr)

    ##### END #####
    ##### IF STATEMENTS AND CONDITIONS #####

    @_(r'IF condition THEN statement ELSE statement')
    def statement(self, p):
        """If statement WITH ELSE."""
        return ('if_stmt_with_else', p.condition, ('branch', p.statement0, p.statement1))
    
    @_(r'IF condition THEN statement')
    def statement(self, p):
        """If statement WITHOUT ELSE."""
        return ('if_stmt_no_else', p.condition, p.statement)
    
    ### Conditions here. ###
    @_(r'expr EQEQ expr')
    def condition(self, p):
        """Condition for EQEQ (==)."""
        return ('condition_eqeq', p.expr0, p.expr1)
    
    @_(r'expr GREATER expr')
    def condition(self, p):
        """Condition for GREATER (>)."""
        return ('condition_greater', p.expr0, p.expr1)
    
    @_(r'expr LESSER expr')
    def condition(self, p):
        """Condition for LESSER (<)."""
        return ('condition_lesser', p.expr0, p.expr1)

    @_(r'expr GE expr')
    def condition(self, p):
        """Condition for greater than or equal. (>=)."""
        return ('condition_ge', p.expr0, p.expr1)

    @_(r'expr LE expr')
    def condition(self, p):
        """Condition for lesser than or equal. (<=)."""
        return ('condition_le', p.expr0, p.expr1)
    
    ##### END #####
    ##### STRING CONCATENATION AND CONVERSION OF DATATYPES #####

    @_(r'expr')
    def statement(self, p):
        """If no calculation is needed. FX: BASIC> 6"""
        return (p.expr)
    
    @_(r'STRING "+" STRING')
    def expr(self, p):
        """Concatenate STRING with STRING."""
        return ('concatenate', p.STRING0, p.STRING1)
    
    @_(r'STRING "+" expr')
    def expr(self, p):
        """Concatenate STRING with expression."""
        return ('concatenate', p.STRING, p.expr)
    
    @_(r'expr "+" STRING')
    def expr(self, p):
        """Concatenate expression with STRING."""
        return ('concatenate', p.expr, p.STRING)
    
    @_(r'CONV_STR "(" expr ")"')
    def expr(self, p):
        """Convert {} to string."""
        return ('convert_str', p.expr)

    ##### END #####
    ##### ADD, SUBTRACT, MULTIPLY AND DIVIDE NO PARENTHESES #####

    @_(r'expr "+" expr')
    def expr(self, p):
        """Add expressions."""
        return ("add", p.expr0, p.expr1)

    @_(r'expr "-" expr')
    def expr(self, p):
        """Subtract expressions."""
        return ("sub", p.expr0, p.expr1)

    @_(r'expr "*" expr')
    def expr(self, p):
        """Multiply expressions."""
        return ("mul", p.expr0, p.expr1)

    @_(r'expr "/" expr')
    def expr(self, p):
        """Divide expressions."""
        return ("div", p.expr0, p.expr1)
    
    ##### END #####
    ##### ADD, SUBTRACT, MULTIPLY AND DIVIDE WITH PARENTHESES #####

    @_(r'"(" expr ")" "+" expr')
    def expr(self, p):
        """Add expressions."""
        return ("add", p.expr0, p.expr1)

    @_(r'"(" expr ")" "-" expr')
    def expr(self, p):
        """Subtract expressions."""
        return ("sub", p.expr0, p.expr1)

    @_(r'"(" expr ")" "*" expr')
    def expr(self, p):
        """Multiply expressions."""
        return ("mul", p.expr0, p.expr1)

    @_(r'"(" expr ")" "/" expr')
    def expr(self, p):
        """Divide expressions."""
        return ("div", p.expr0, p.expr1)
    
    @_(r'expr "+" "(" expr ")"')
    def expr(self, p):
        """Add expressions."""
        return ("add", p.expr0, p.expr1)

    @_(r'expr "-" "(" expr ")"')
    def expr(self, p):
        """Subtract expressions."""
        return ("sub", p.expr0, p.expr1)

    @_(r'expr "*" "(" expr ")"')
    def expr(self, p):
        """Multiply expressions."""
        return ("mul", p.expr0, p.expr1)

    @_(r'expr "/" "(" expr ")"')
    def expr(self, p):
        """Divide expressions."""
        return ("div", p.expr0, p.expr1)

    @_(r'"(" expr ")" "+" "(" expr ")"')
    def expr(self, p):
        """Add expressions."""
        return ("add", p.expr0, p.expr1)

    @_(r'"(" expr ")" "-" "(" expr ")"')
    def expr(self, p):
        """Subtract expressions."""
        return ("sub", p.expr0, p.expr1)
    
    @_(r'"(" expr ")" "*" "(" expr ")"')
    def expr(self, p):
        """Multiply expressions."""
        return ("mul", p.expr0, p.expr1)

    @_(r'"(" expr ")" "/" "(" expr ")"')
    def expr(self, p):
        """Divide expressions."""
        return ("div", p.expr0, p.expr1)
    
    ##### END #####
    ##### EXPRESSION VARIABLES #####

    @_(r'"-" expr %prec UMINUS')
    def expr(self, p):
        """When using the unary minus expression in expression."""
        # Turn number into a negative.
        p.expr = (p.expr[0], -p.expr[1])

        return p.expr

    @_(r'NAME')
    def expr(self, p):
        """Variable in expression."""
        return ('var', p.NAME)

    @_(r'NUMBER')
    def expr(self, p):
        """NUMBER in expression."""
        return ('num', p.NUMBER)
    
    @_(r'STRING')
    def expr(self, p):
        """STRING in expression."""
        return ('str', p.STRING)
    
    ##### END #####
    ##### EXIT PROGRAM #####

    @_(r'EXIT "(" ")"')
    def statement(self, p):
        """Exit the program/interpreter."""
        return ('sys_exit')
