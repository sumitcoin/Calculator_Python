from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple Calculator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .calculator {
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                width: 320px;
            }

            .calculator h1 {
                text-align: center;
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
            }

            .display {
                background: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: right;
                font-size: 32px;
                color: #333;
                word-wrap: break-word;
                word-break: break-all;
                min-height: 60px;
                display: flex;
                align-items: center;
                justify-content: flex-end;
            }

            .buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
            }

            button {
                padding: 20px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.2s ease;
            }

            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }

            button:active {
                transform: translateY(0);
            }

            .number, .operator {
                background: #f0f0f0;
                color: #333;
                border: 2px solid #ddd;
            }

            .number:hover {
                background: #e0e0e0;
            }

            .operator {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }

            .operator:hover {
                background: #5568d3;
            }

            .equals {
                background: #48bb78;
                color: white;
                border: 2px solid #48bb78;
                grid-column: span 2;
            }

            .equals:hover {
                background: #38a169;
            }

            .clear {
                background: #f56565;
                color: white;
                border: 2px solid #f56565;
                grid-column: span 2;
            }

            .clear:hover {
                background: #e53e3e;
            }

            .delete {
                background: #ed8936;
                color: white;
                border: 2px solid #ed8936;
            }

            .delete:hover {
                background: #dd6b20;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <h1>Calculator</h1>
            <div class="display" id="display">0</div>
            <div class="buttons">
                <button class="clear" onclick="clearDisplay()">C</button>
                <button class="delete" onclick="deleteLastChar()">&larr;</button>
                <button class="operator" onclick="appendOperator('/')">÷</button>
                <button class="number" onclick="appendNumber('7')">7</button>
                <button class="number" onclick="appendNumber('8')">8</button>
                <button class="number" onclick="appendNumber('9')">9</button>
                <button class="operator" onclick="appendOperator('*')">×</button>
                <button class="number" onclick="appendNumber('4')">4</button>
                <button class="number" onclick="appendNumber('5')">5</button>
                <button class="number" onclick="appendNumber('6')">6</button>
                <button class="operator" onclick="appendOperator('-')">−</button>
                <button class="number" onclick="appendNumber('1')">1</button>
                <button class="number" onclick="appendNumber('2')">2</button>
                <button class="number" onclick="appendNumber('3')">3</button>
                <button class="operator" onclick="appendOperator('+')">+</button>
                <button class="number" onclick="appendNumber('0')" style="grid-column: span 2;">0</button>
                <button class="number" onclick="appendNumber('.')">.</button>
                <button class="equals" onclick="calculate()">=</button>
            </div>
        </div>

        <script>
            let display = document.getElementById('display');
            let currentInput = '0';

            function updateDisplay() {
                display.textContent = currentInput;
            }

            function appendNumber(num) {
                if (currentInput === '0' && num !== '.') {
                    currentInput = num;
                } else if (num === '.' && currentInput.includes('.')) {
                    return;
                } else {
                    currentInput += num;
                }
                updateDisplay();
            }

            function appendOperator(op) {
                if (currentInput === '') return;
                currentInput += ' ' + op + ' ';
                updateDisplay();
            }

            function clearDisplay() {
                currentInput = '0';
                updateDisplay();
            }

            function deleteLastChar() {
                currentInput = currentInput.slice(0, -1) || '0';
                updateDisplay();
            }

            function calculate() {
                if (currentInput === '' || currentInput === '0') return;
                
                try {
                    let result = eval(currentInput);
                    currentInput = result.toString();
                    updateDisplay();
                } catch (error) {
                    currentInput = 'Error';
                    updateDisplay();
                    setTimeout(() => {
                        currentInput = '0';
                        updateDisplay();
                    }, 1000);
                }
            }

            // Keyboard support
            document.addEventListener('keydown', (e) => {
                if (/[0-9.]/.test(e.key)) appendNumber(e.key);
                if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
                    e.preventDefault();
                    appendOperator(e.key);
                }
                if (e.key === 'Enter' || e.key === '=') {
                    e.preventDefault();
                    calculate();
                }
                if (e.key === 'Backspace') deleteLastChar();
                if (e.key === 'Escape') clearDisplay();
            });
        </script>
    </body>
    </html>
    '''

@app.route('/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        result = eval(expression)
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)