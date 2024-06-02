import re

class Interpreter:
    def __init__(self, tokens, syntax_file):
        self.tokens = tokens
        self.position = 0
        self.keyword_handlers = {}
        self.load_syntax(syntax_file)
    
    def load_syntax(self, syntax_file):
        with open(syntax_file, 'r') as file:
            content = file.read()
            keywords_section = re.search(r'KEYWORDS:\n(.*?)(?=\n\n)', content, re.DOTALL)
            if keywords_section:
                keywords = keywords_section.group(1).split()
                for keyword in keywords:
                    self.keyword_handlers[keyword] = self.create_handler(keyword)
    
    def create_handler(self, keyword):
        def handler():
            if keyword == 'display':
                self.handle_printy()
            elif keyword == 'if':
                self.handle_if()
            elif keyword == 'while':
                self.handle_while()
            elif keyword == 'else':
                pass
            elif keyword == 'end':
                pass
        return handler

    def parse(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token[0] == 'KEYWORD' and token[1] in self.keyword_handlers:
                self.position += 1
                self.keyword_handlers[token[1]]()
            else:
                self.position += 1
    
    def handle_printy(self):
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
