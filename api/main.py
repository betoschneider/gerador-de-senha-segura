from flask import Flask, request, jsonify
from random import choice
import string

app = Flask(__name__)

@app.route('/senha', methods=['GET'])
def gerar_senha():
    try:
        tamanho = int(request.args.get('len'))
        #len=12&options=['uppercase', 'lowercase', 'number', 'symbol']
        opcoes = request.args.get('options').replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
        caracteres = ''
        for opcao in opcoes.split(','):
            if opcao == 'uppercase':
                caracteres += string.ascii_uppercase
            if opcao == 'lowercase':
                caracteres += string.ascii_lowercase
            if opcao == 'number':
                caracteres += string.digits
            if opcao == 'symbol':
                caracteres += string.punctuation
        
        tamanho = max(min(tamanho, 25), 4)
        senha = ''
        for i in range(tamanho):
            senha += choice(caracteres)
        
        return {'senha': senha}, 200
    except:
        return {'message': 'Um erro ocorreu ao tentar gerar a senha.'}, 500

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)