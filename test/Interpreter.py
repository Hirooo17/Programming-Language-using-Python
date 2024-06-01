import re
import ast

class SyntaxRule:
    def __init__(self, pattern, match_group):
        self.pattern = pattern
        self.match_group = match_group

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.syntax_rules = []
        self.read_rules_from_file("syntax_bank.txt")
        self.syntax = re.compile("|".join([rule.pattern for rule in self.syntax_rules]))
        print("Syntax rules loaded:", self.syntax_rules)

    def read_rules_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    pattern, match_group = self.parse_syntax_rule(line)
                    self.syntax_rules.append(SyntaxRule(pattern, match_group))

    def parse_syntax_rule(self, line):
        parts = line.split()
        match_group = parts[0]
        pattern = " ".join(parts[1:])
        pattern = r"\b" + pattern + r"\b"
        return pattern, match_group

    def tokenize(self, code):
        token_pattern = r'\b(?:grah|display|int|string|\d+|[a-zA-Z_]\w*|[+\-*/=]|"[^"]*"|\.)\b'
        tokens = re.findall(token_pattern, code)
        return tokens

    def interpret(self, code, output_func):
        code_lines = code.strip().split("\n")
        print("Interpreting code:")
        for line in code_lines:
            print(f"Processing line: {line}")
            if line:
                tokens = self.tokenize(line)
                print(f"Tokens: {tokens}")
                if tokens and tokens[0] != 'grah' and tokens[0] != 'display':
                    output_func(f"Syntax error: line '{line}' must start with 'grah' or 'display'\n")
                    continue

                if tokens[0] == 'grah':
                    self.handle_assignment(tokens, output_func)
                elif tokens[0] == 'display':
                    self.handle_print(tokens, output_func)
                else:
                    output_func(f"Unknown command: '{line}'\n")

    def handle_assignment(self, tokens, output_func):
        print(f"Handling assignment: {tokens}")
        if len(tokens) < 5 or tokens[2] != '=':
            output_func(f"Syntax error in assignment: {' '.join(tokens)}\n")
            return

        variable_name = tokens[1]
        if tokens[3] == 'int':
            value = int(tokens[4])
        elif tokens[3] == 'String':
            value = tokens[4][1:-1]
        else:
            output_func(f"Invalid data type: {tokens[3]}\n")
            return

        if variable_name in self.variables:
            self.variables[variable_name] = value
        else:
            self.variables[variable_name] = {tokens[3]: value}

        output_func(f"Variable '{variable_name}' = {value}\n")

    def handle_print(self, tokens, output_func):
        print(f"Handling print: {tokens}")
        expression = " ".join(tokens[1:])  # Skip the 'display' token
        value = self.evaluate_expression(expression)
        if value is not None:
            output_func(str(value) + "\n")

    def evaluate_expression(self, expr):
        print(f"Evaluating expression: {expr}")
        try:
            tree = ast.parse(expr, mode='eval')
            value = eval(compile(tree, "<string>", "eval"), {}, self.variables)
        except Exception as e:
            return f"Error: {e}"
        return value