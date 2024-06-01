import tkinter as tk
from tkinter import filedialog, Text, ttk, scrolledtext
from Interpreter import Interpreter
import pdb

class MyIDE(tk.Tk):
    def __init__(self):
        super().__init__()

        self.interpreter = Interpreter()

        menubar = tk.Menu(self)
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=menubar)

        self.text_area = Text(self)
        self.tab_control = ttk.Notebook(self)
        self.text_tab = ttk.Frame(self.tab_control)
        self.run_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.text_tab, text="Untitled")

        self.text_area.pack(expand=1, fill="both")

        self.run_button = ttk.Button(self.run_tab, text="Run", command=self.run_code)
        self.run_button.pack()

        self.tab_control.add(self.run_tab, text="Run")

        self.tab_control.pack(expand=1, fill="both")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("GRAH files", "*.GRAH")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.insert("1.0", file.read())
            self.tab_control.tab(self.text_tab, text=file_path.split("/")[-1])

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".GRAH", filetypes=[("GRAH files", "*.GRAH")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get("1.0", "end-1c"))
            self.tab_control.tab(self.text_tab, text=file_path.split("/")[-1])

    def run_code(self):
        code = self.text_area.get("1.0", "end-1c")
        print("Running code...")

        try:
            output = self.interpreter.interpret(code)
            if output is not None:
                print(output)
            else:
                print()
        except Exception as e:
            print("Error: ", str(e))

def main():
    app = MyIDE()
    app.mainloop()

if __name__ == "__main__":
    main()