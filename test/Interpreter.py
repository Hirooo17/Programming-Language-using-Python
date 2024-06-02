import re

class SyntaxRule:
    def __init__(self, pattern, match_group):
        self.pattern = pattern
        self.match_group = match_group

class Lexer:
    def __init__(self):
        self.token_specification = []
        self.read_rules_from_file("syntax_bank.txt")
        self.token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_specification))

    def read_rules_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    match_group = parts[0]
                    pattern = " ".join(parts[1:])
                    self.token_specification.append((match_group, pattern))

    def tokenize(self, code):
        tokens = []
        for mo in self.token_re.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in ('grah', 'display', 'int', 'string'):
                kind = value.upper()
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            tokens.append(Token(kind, value))
        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return statements

    def statement(self):
        if self.match('GRAH'):
            return self.assignment()
        elif self.match('DISPLAY'):
            return self.print_statement()
        else:
            raise SyntaxError(f'Unexpected token: {self.peek().value}')

    def assignment(self):
        self.consume('GRAH')
        dtype = self.consume('INT', 'STRING').type.lower()
        var_name = self.consume('ID').value
        self.consume('ASSIGN')
        expr = self.expression()
        self.consume('END')
        return ('assign', dtype, var_name, expr)

    def print_statement(self):
        self.consume('DISPLAY')
        expr = self.expression()
        self.consume('END')
        return ('print', expr)

    def expression(self):
        terms = [self.term()]
        while self.match('OP'):
            op = self.consume('OP').value
            term = self.term()
            terms.append((op, term))
        if len(terms) == 1:
            return terms[0]
        return terms

    def term(self):
        if self.match('NUMBER'):
            return ('number', self.consume('NUMBER').value)
        elif self.match('STRING'):
            return ('string', self.consume('STRING').value.strip('"'))
        elif self.match('ID'):
            return ('variable', self.consume('ID').value)
        else:
            raise SyntaxError(f'Unexpected token: {self.peek().value}')

    def match(self, *token_types):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].type in token_types
        return False

    def consume(self, *token_types):
        if self.match(*token_types):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        raise SyntaxError(f'Expected {token_types}, got {self.peek().type}')

    def peek(self):
        return self.tokens[self.pos]

class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, statements):
        for stmt in statements:
            if stmt[0] == 'assign':
                self.execute_assignment(stmt)
            elif stmt[0] == 'print':
                self.execute_print(stmt)

    def execute_assignment(self, stmt):
        _, dtype, var_name, expr = stmt
        value = self.evaluate(expr)
        self.variables[var_name] = value

    def execute_print(self, stmt):
        _, expr = stmt
        value = self.evaluate(expr)
        print(value)

    def evaluate(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'number':
                return expr[1]
            elif expr[0] == 'string':
                return expr[1]
            elif expr[0] == 'variable':
                var_name = expr[1]
                if var_name in self.variables:
                    return self.variables[var_name]
                raise NameError(f'Undefined variable: {var_name}')
            elif isinstance(expr, list):
                result = self.evaluate(expr[0])
                for op, term in expr[1:]:
                    right = self.evaluate(term)
                    if op == '+':
                        result += right
                    elif op == '-':
                        result -= right
                    elif op == '*':
                        result *= right
                    elif op == '/':
                        result /= right
                return result
        else:
            raise TypeError(f'Invalid expression: {expr}')
