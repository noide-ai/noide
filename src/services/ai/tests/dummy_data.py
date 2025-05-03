"""
Dummy data to test issue solver
"""
from src.models import File, Issue

test_file1 = File(
    path='calculator.py',
    content="""
             class Calculator:
                def add(self, a, b):
                    return a + b
            
                def subtract(self, a, b):
                    return a - b
            
                def multiply(self, a, b):
                    return a * b
            
                def divide(self, a, b):
                    return a / b
            
                def power(self, a, b):
                    return a ** b
            
                def square_root(self, a):
                    return a ** 0.5
             """
)

test_file2 = File(
    path='app.py',
    content="""
            from calculator import Calculator
            from flask import Flask, request, render_template, jsonify
            
            app = Flask(__name__)
            calc = Calculator()
            
            @app.route('/')
            def index():
                return render_template('index.html')
            
            @app.route('/calculate', methods=['POST'])
            def calculate():
                data = request.get_json()
                operation = data.get('operation')
                a = float(data.get('a', 0))
                b = float(data.get('b', 0))
            
                result = None
            
                if operation == 'add':
                    result = calc.add(a, b)
                elif operation == 'subtract':
                    result = calc.subtract(a, b)
                elif operation == 'multiply':
                    result = calc.multiply(a, b)
                elif operation == 'divide':
                    # BUG: No handling of potential ZeroDivisionError from the calculator
                    result = calc.divide(a, b)
                elif operation == 'power':
                    result = calc.power(a, b)
                elif operation == 'square_root':
                    # BUG: No handling of potential ValueError for negative numbers
                    result = calc.square_root(a)
            
                return jsonify({'result': result})
            
            if __name__ == '__main__':
                app.run(debug=True)
             """
)

test_issue = Issue(
    title="Division by Zero",
    body="The calculator application crashes when a user attempts to divide by zero or calculate the square root of a negative number."
)

test_file_list = [test_file1, test_file2]





