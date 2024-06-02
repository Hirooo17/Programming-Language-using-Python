import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

class Lexer:
    def __init__(self, syntax_rules):
        self.token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
            ('ASSIGN',   r'='),             # Assignment operator
            ('END',      r'\.'),            # End of statement
            ('ID',       r'[A-Za-z_]\w*'),  # Identifiers
            ('OP',       r'[+\-*/]'),       # Arithmetic operators
            ('STRING',   r'"[^"]*"'),       # String literals
            ('SKIP',     r'[ \t]+'),        # Skip spaces and tabs
            ('MISMATCH', r'.'),             # Any other character
        ]
        # Add the rules from syntax_bank.txt
        self.token_specification.extend(syntax_rules)
        self.token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_specification))

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
