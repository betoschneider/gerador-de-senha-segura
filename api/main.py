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

# Baixar recursos do NLTK (executado apenas uma vez)
nltk.download('stopwords')
nltk.download('punkt_tab')

app = Flask(__name__)

@app.route('/password', methods=['GET'])
def gerar_senha():
    try:
        tipo = request.args.get('type', 'senha')  # 'senha' ou 'frase'
        tamanho = int(request.args.get('len', 12))
        lang = request.args.get('lang', 'pt_BR')

        # Flags REST-friendly
        upper = request.args.get('upper', 'true').lower() == 'true'
        lower = request.args.get('lower', 'true').lower() == 'true'
        num = request.args.get('num', 'true').lower() == 'true'
        special = request.args.get('special', 'false').lower() == 'true'

        # ==============================
        # GERAÇÃO DE SENHA
        # ==============================
        if tipo == 'senha':
            # Definição dos grupos de caracteres
            grupos = []
            if upper:
                grupos.append(string.ascii_uppercase)
            if lower:
                grupos.append(string.ascii_lowercase)
            if num:
                grupos.append(string.digits)
            if special:
                grupos.append("#!@.$%&*")  # conjunto restrito

            if not grupos:
                return jsonify({'error': 'Nenhum conjunto de caracteres selecionado.'}), 400

            tamanho = max(min(tamanho, 25), 4)

            # Garante pelo menos 1 caractere de cada grupo escolhido
            senha_chars = [choice(grupo) for grupo in grupos]

            # Preenche o restante com caracteres de todos os grupos combinados
            todos_caracteres = ''.join(grupos)
            restantes = tamanho - len(senha_chars)

            senha_chars += [choice(todos_caracteres) for _ in range(restantes)]

            # Embaralha para não ficar previsível
            random.shuffle(senha_chars)

            senha = ''.join(senha_chars)

        # ==============================
        # GERAÇÃO DE FRASE SECRETA
        # ==============================
        elif tipo == 'frase':
            lang_map = {
                'pt_BR': 'portuguese',
                'es_CL': 'spanish',
                'en_US': 'english',
                'fr_FR': 'french'
            }
            fake = Faker(locale=lang)
            texto = " ".join(
                " ".join([
                    fake.catch_phrase(),
                    fake.catch_phrase_attribute() if lang not in ['en_US', 'es_CL'] else '',
                    fake.catch_phrase_verb() if lang not in ['en_US', 'es_CL'] else '',
                    # fake.first_name(),
                    fake.color_name(),
                    fake.job(),
                    fake.month_name(),
                    fake.street_prefix() if lang not in ['en_US', 'es_CL'] else '',
                    fake.day_of_week()
                ])
                for _ in range(80)
            )

            # Remove caracteres especiais e acentuação
            texto = re.sub(r'[^\w\s]', ' ', texto)
            texto = "".join(
                c for c in unicodedata.normalize('NFKD', texto)
                if not unicodedata.combining(c)
            )

            # Tokenização e filtragem
            palavras = word_tokenize(texto, language=lang_map.get(lang, 'portuguese'))
            stop_words = set(stopwords.words(lang_map.get(lang, 'portuguese')))
            palavras_filtradas = [p.lower() for p in palavras if p.lower() not in stop_words]
            palavras_filtradas = list(dict.fromkeys(palavras_filtradas))

            if not palavras_filtradas:
                return jsonify({'error': 'Falha ao gerar palavras para a frase.'}), 500

            # Gera a frase secreta
            qtd_palavras = max(min(tamanho, 15), 2)
            frase_secreta = random.sample(palavras_filtradas, qtd_palavras)

            # Aplicar opções
            if upper:
                frase_secreta = [p.capitalize() for p in frase_secreta]
            if num:
                idx = random.randint(0, len(frase_secreta) - 1)
                frase_secreta[idx] += str(random.randint(0, 9))

            # 🔒 Sempre usar separador aleatório de #!@.$%&*
            separador = random.choice("#!@.$%&*")
            senha = separador.join(frase_secreta)

        else:
            return jsonify({'error': 'Tipo inválido. Use "senha" ou "frase".'}), 400

        return jsonify({'password': senha}), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao gerar senha.', 'detalhe': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
