import tkinter as tk
from sympy import symbols, integrate, diff, solve, Eq, lambdify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CalcApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculation Tool")
        self.geometry("677x400") 
        self.configure(background='white')

        self.equation_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.equation_var.set("sin(x)")  

        self.create_widgets()

    def create_widgets(self):
        equation_entry = tk.Entry(self, textvariable=self.equation_var)
        equation_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        calc_buttons_frame = tk.Frame(self)
        calc_buttons_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        calc_buttons = [
            'sin', 'cos', 'tan', 'log',
            'sqrt', 'exp', '(', ')',
            '1', '2', '3', '+',
            '4', '5', '6', '-',
            '7', '8', '9', '*',
            '0', '.', '**', '/',
        ]

        for btn_text in calc_buttons:
            btn = tk.Button(calc_buttons_frame, text=btn_text, width=5, height=2, command=lambda text=btn_text: self.add_to_equation(text))
            btn.grid(row=calc_buttons.index(btn_text)//4, column=calc_buttons.index(btn_text)%4)

        integrate_button = tk.Button(self, text="Integrate", command=self.perform_integration)
        integrate_button.grid(row=2, column=0, padx=5, pady=5)

        derivative_button = tk.Button(self, text="Differentiate", command=self.perform_differentiation)
        derivative_button.grid(row=2, column=1, padx=5, pady=5)

        solve_button = tk.Button(self, text="Solve Equation", command=self.solve_equation)
        solve_button.grid(row=2, column=2, padx=5, pady=5)

        result_label = tk.Label(self, text="Result:")
        result_label.grid(row=3, column=0, padx=5, pady=5)
        result_entry = tk.Entry(self, textvariable=self.result_var, state='readonly')
        result_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=4, rowspan=4, padx=10, pady=10)

    def add_to_equation(self, text):
        self.equation_var.set(self.equation_var.get() + text)

    def perform_integration(self):
        try:
            x = symbols('x')
            equation = self.equation_var.get()

            integrated_equation = integrate(equation, x)

            self.result_var.set(str(integrated_equation))

            self.plot_graph(equation, integrated_equation)

        except Exception as e:
            self.result_var.set("Error: " + str(e))

    def perform_differentiation(self):
        try:
            x = symbols('x')
            equation = self.equation_var.get()

            differentiated_equation = diff(equation, x)

            self.result_var.set(str(differentiated_equation))

            self.plot_graph(equation, differentiated_equation)

        except Exception as e:
            self.result_var.set("Error: " + str(e))

    def solve_equation(self):
        try:
            x = symbols('x')
            equation = self.equation_var.get()

            solution = solve(Eq(equation, 0), x)

            self.result_var.set(str(solution))


            self.plot_graph(equation)

        except Exception as e:
            self.result_var.set("Error: " + str(e))

    def plot_graph(self, equation, integrated_equation=None):
        x = symbols('x')
        x_vals = np.linspace(-10, 10, 1000)
        func = lambdify(x, equation, 'numpy')
        y_vals = func(x_vals)

        self.ax.clear()
        self.ax.plot(x_vals, y_vals, label='Equation')

        if integrated_equation:
            integrated_func = lambdify(x, integrated_equation, 'numpy')
            integrated_y_vals = integrated_func(x_vals)
            self.ax.plot(x_vals, integrated_y_vals, label='Integrated Equation')

        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = CalcApp()
    app.mainloop()
