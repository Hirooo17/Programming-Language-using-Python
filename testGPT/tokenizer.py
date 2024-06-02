import re

class Tokenizer:
    def __init__(self, syntax_file):
        self.keywords = []
        self.operators = []
        self.syntax_rules = []
        self.load_syntax(syntax_file)
    
    def load_syntax(self, syntax_file):
        with open(syntax_file, 'r') as file:
            content = file.read()
            keywords_section = re.search(r'KEYWORDS:\n(.*?)(?=\n\n)', content, re.DOTALL)
            operators_section = re.search(r'OPERATORS:\n(.*?)(?=\n\n)', content, re.DOTALL)
            syntax_section = re.search(r'SYNTAX:\n(.*?)(?=\n\n|$)', content, re.DOTALL)

            if keywords_section:
                self.keywords = keywords_section.group(1).split()
            if operators_section:
                self.operators = operators_section.group(1).split()
            if syntax_section:
                self.syntax_rules = syntax_section.group(1).strip().split('\n')
    
    def tokenize(self, code):
        tokens = []
        words = re.findall(r'\w+|[^\s\w]', code)
        for word in words:
            if word in self.keywords:
                tokens.append(('KEYWORD', word))
            elif word in self.operators:
                tokens.append(('OPERATOR', word))
            elif re.match(r'\d+', word):
                tokens.append(('NUMBER', word))
            else:
                tokens.append(('IDENTIFIER', word))
        return tokens
