class Interpreter:
    def __init__(self, tokens, syntax_rules):
        self.tokens = tokens
        self.syntax_rules = syntax_rules
        self.position = 0
    
    def parse(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token[0] == 'KEYWORD':
                if token[1] == 'print':
                    self.position += 1
                    self.handle_print()
                elif token[1] == 'if':
                    self.position += 1
                    self.handle_if()
                elif token[1] == 'while':
                    self.position += 1
                    self.handle_while()
                elif token[1] == 'end':
                    self.position += 1
                    break
            else:
                self.position += 1
    
    def handle_print(self):
        expr = []
        while self.position < len(self.tokens) and self.tokens[self.position][1] != 'end':
            expr.append(self.tokens[self.position][1])
            self.position += 1
        print(eval(' '.join(expr)))
    
    def handle_if(self):
        condition = []
        while self.position < len(self.tokens) and self.tokens[self.position][1] != ':':
            condition.append(self.tokens[self.position][1])
            self.position += 1
        self.position += 1  # Skip ':'
        if eval(' '.join(condition)):
            self.parse()
        else:
            while self.position < len(self.tokens) and self.tokens[self.position][1] != 'else':
                self.position += 1
            if self.tokens[self.position][1] == 'else':
                self.position += 1  # Skip 'else'
                self.position += 1  # Skip ':'
                self.parse()
    
    def handle_while(self):
        condition = []
        while self.position < len(self.tokens) and self.tokens[self.position][1] != ':':
            condition.append(self.tokens[self.position][1])
            self.position += 1
        self.position += 1  # Skip ':'
        start_position = self.position
        while eval(' '.join(condition)):
            self.position = start_position
            self.parse()
