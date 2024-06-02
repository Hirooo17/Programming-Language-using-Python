import tkinter as tk
from tkinter import scrolledtext
from tokenizer import Tokenizer
from interpreter import Interpreter

class IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Programming Language IDE")
        self.create_widgets()
        
    def create_widgets(self):
        self.editor = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.editor.pack(pady=10)
        
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(pady=10)
        
        self.output = scrolledtext.ScrolledText(self.root, width=80, height=10, state='disabled')
        self.output.pack(pady=10)
        
    def run_code(self):
        code = self.editor.get("1.0", tk.END)
        tokenizer = Tokenizer('syntax.txt')
        tokens = tokenizer.tokenize(code)
        
        interpreter = Interpreter(tokens, 'syntax.txt')
        
        # Redirect print to output console
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.stdout = self.output
        self.run_interpreter(interpreter)
        self.output.config(state='disabled')
        
    def run_interpreter(self, interpreter):
        import sys
        from io import StringIO
        
        # Redirect stdout
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            interpreter.parse()
            output = mystdout.getvalue()
            self.stdout.insert(tk.END, output)
        except Exception as e:
            self.stdout.insert(tk.END, f"Error: {e}")
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    root = tk.Tk()
    ide = IDE(root)
    root.mainloop()
