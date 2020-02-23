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

    @_(r'PRINT "(" STRING ")"')
    def statement(self, p):
        """Print a string."""
        return ('print_str', p.STRING)

    @_(r'PRINT "(" expr ")"')
    def statement(self, p):
        """Print an expression."""
        return ('print_expr', p.expr)

    @_(r'expr')
    def statement(self, p):
        """If no calculation is needed. FX: BASIC> 6"""
        return (p.expr)

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

    @_(r'"-" expr %prec UMINUS')
    def expr(self, p):
        """When using the unary minus expression in expression."""
        return p.expr

    @_(r'NAME')
    def expr(self, p):
        """Variable in expression."""
        return ('var', p.NAME)

    @_(r'NUMBER')
    def expr(self, p):
        """NUMBER in expression."""
        return ('num', p.NUMBER)
