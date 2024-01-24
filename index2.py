from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def pagina():
    return render_template('index.html', bandera='')

class Tokenizer:
    def __init__(self):
        self.keywords = {'var', 'func', 'void', 'main', 'if', 'else', 'while', 'true', 'false'}

    def tokenize(self, input_string):
        tokens = []
        current_token = ''

        for char in input_string:
            if char.isalnum() or char == '_':
                current_token += char
            else:
                if current_token:
                    token_type, token_value = self.classify_token(current_token)
                    tokens.append({'type': token_type, 'value': token_value})
                current_token = ''
                if char.isspace():
                    continue
                token_type, token_value = self.classify_token(char)
                tokens.append({'type': token_type, 'value': token_value})

        if current_token:
            token_type, token_value = self.classify_token(current_token)
            tokens.append({'type': token_type, 'value': token_value})

        return tokens



    def classify_token(self, token):
        token_mappings = {
            **{kw.upper(): kw.upper() for kw in self.keywords},
            **{'=': 'EQUALS', 'var': 'VAR', 'func': 'FUNC', '(': 'OPEN_PAREN', ')': 'CLOSE_PAREN', '{': 'OPEN_BRACE',
                '}': 'CLOSE_BRACE', 'void': 'VOID', 'main': 'MAIN', 'if': 'IF', 'else': 'ELSE', '==': 'EQUALS_EQUALS',
                '!=': 'DIFERENT', '<=': 'LESS_THAN', '>=': 'MORE_THAN', 'while': 'WHILE', 'true': 'TRUE', 'false': 'FALSE'
                },
            **{str(i): 'INT' for i in range(10)}
        }

        token_type = token_mappings.get(token, f'Error en el caracter {token}' if not (token.isidentifier() or token.isdigit()) else 'NUMBER' if token.isdigit() else 'VARNAME')

        return token_type, token

    
@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    texto = request.form.get('texto')

    tokenizer = Tokenizer()
    token = tokenizer.tokenize(texto)

    return render_template('index.html', bandera=True, tokens=token, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)