from flask import Flask, request, jsonify
from random import choice
import string
from faker import Faker
import random
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Baixar as stopwords do NLTK (apenas uma vez)
nltk.download('stopwords')
nltk.download('punkt_tab')

app = Flask(__name__)

@app.route('/senha', methods=['GET'])
def gerar_senha():
    try:
        # define as variáveis com os argumentos da url
        tipo = request.args.get('type')
        tamanho = int(request.args.get('len'))
        opcoes = request.args.get('options').replace('[', '').replace(']', '').replace("'", '').replace(' ', '')

        # Para geração de senha
        if tipo == 'senha':
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
        elif tipo == 'frase':
            # Geração dos textos
            # fake = Faker(locale='pt_BR')
            lang = request.args.get('lang')
            lang_map = {
                'pt_BR': 'portuguese',
                'es_ES': 'spanish',
                'en_US': 'english',
                'fr_FR': 'french'
            }
            fake = Faker(locale=lang)
            texto = ''
            for i in range(40):
                texto += " ".join([
                    fake.catch_phrase(),
                    fake.catch_phrase_attribute() if lang not in ['en_US', 'es_ES'] else '',
                    fake.catch_phrase_verb() if lang not in ['en_US', 'es_ES'] else '',
                    fake.first_name(),
                    fake.color_name(),
                    fake.job(),
                    fake.month_name(),
                    fake.street_prefix() if lang != 'en_US' else '',
                    fake.day_of_week()
                ]) + " "
            
            # Remove caracteres especiais do texto
            texto = re.sub(r'[^\w\s]', ' ', texto)

            # Função para remover acentos e cedilha
            def remover_acentos(texto):
                nfkd = unicodedata.normalize('NFKD', texto)
                return "".join([char for char in nfkd if not unicodedata.combining(char)])
            
            # Remove acentos e cedilha
            texto = remover_acentos(texto)

            # Tokeniza o texto (divide o texto em palavras)
            palavras = word_tokenize(texto, language=lang_map[lang])

            # Obtém a lista de stopwords em português
            stop_words = set(stopwords.words(lang_map[lang]))

            # Filtra as palavras, removendo as stopwords
            palavras_filtradas = [palavra.lower() for palavra in palavras if palavra.lower() not in stop_words]

            # Removendo palavras duplicadas
            palavras_filtradas = list(dict.fromkeys(palavras_filtradas))
            qtd_filtradas = len(palavras_filtradas) # total de palavras filtradas

            # Faz a seleção para gerar a frase secreta
            qtd_palavras = tamanho # quantidade de palavras na frase secreta
            if "º" not in opcoes:
                separador = opcoes[-1] # separador das palavras
            else:
                separador = ""

            frase_secreta = []
            for i in range(qtd_palavras):
                # seleciona a palavra
                palavra = palavras_filtradas[random.randint(0, qtd_filtradas - 1)]
                
                # seleciona outra palavra caso já esteja na frase secreta
                while palavra in frase_secreta:
                    palavra = palavras_filtradas[random.randint(0, qtd_filtradas - 1)]
                
                # adiciona a palavra selecionada na frase secreta
                frase_secreta.append(palavra)

            # Transforma primeira letra em maiúscula
            if 'uppercase' in opcoes:
                frase_secreta = [palavra.capitalize() for palavra in frase_secreta]

            # Adiciona um número
            if 'number' in opcoes:
                id_palavra = random.randint(0, qtd_palavras - 1)
                frase_secreta[id_palavra] = frase_secreta[id_palavra] + str(random.randint(0, 9))

            # Concatena a frase com o sparador
            senha = separador.join(frase_secreta)
        
        return {'senha': senha}, 200
    except:
        return {'message': 'Um erro ocorreu ao tentar gerar a senha.'}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
