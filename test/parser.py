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
