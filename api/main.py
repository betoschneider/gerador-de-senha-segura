from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(
    title="Gerador de Senha Segura API",
    description="API para geração de senhas fortes e frases secretas.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/password")
def gerar_senha(
    type: str = Query("senha", pattern="^(senha|frase)$"),
    lenght: int = Query(12, alias="len", ge=2, le=50),
    lang: str = Query("pt_BR", pattern="^(pt_BR|es_CL|en_US|fr_FR)$"),
    upper: bool = Query(True),
    lower: bool = Query(True),
    num: bool = Query(True),
    special: bool = Query(False),
):
    try:
        # ==============================
        # GERAÇÃO DE SENHA
        # ==============================
        if type == 'senha':
            # Definição dos grupos de caracteres
            grupos = []
            if upper:
                grupos.append(string.ascii_uppercase)
            if lower:
                grupos.append(string.ascii_lowercase)
            if num:
                grupos.append(string.digits)
            if special:
                grupos.append("#!@.$%&*")

            if not grupos:
                raise HTTPException(status_code=400, detail="Nenhum conjunto de caracteres selecionado.")
            
            lenght = max(min(lenght, 25), 4)

            # Garante pelo menos 1 caractere de cada grupo escolhido
            senha_chars = [choice(grupo) for grupo in grupos]

            # Preenche o restante com caracteres de todos os grupos combinados
            todos_caracteres = ''.join(grupos)
            restantes = lenght - len(senha_chars)
            senha_chars += [choice(todos_caracteres) for _ in range(restantes)]

            random.shuffle(senha_chars)
            senha = ''.join(senha_chars)

        # ==============================
        # GERAÇÃO DE FRASE SECRETA
        # ==============================
        else: # type == 'frase'
            lang_map = {
                'pt_BR': 'portuguese',
                'es_CL': 'spanish',
                'en_US': 'english',
                'fr_FR': 'french'
            }

            # Faker
            fake = Faker(locale=lang)
            texto = " ".join(
                " ".join([
                    fake.catch_phrase(),
                    fake.catch_phrase_attribute() if lang not in ['en_US', 'es_CL'] else '',
                    fake.catch_phrase_verb() if lang not in ['en_US', 'es_CL'] else '',
                    fake.color_name(),
                    fake.job(),
                    fake.month_name(),
                    fake.street_prefix() if lang not in ['en_US', 'es_CL'] else '',
                    fake.day_of_week()
                ])
                for _ in range(80)
            )

            # Limpeza
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
                raise HTTPException(status_code=500, detail="Falha ao gerar palavras para a frase.")

            # Seleção
            qtd_palavras = max(min(lenght, 15), 2)
            frase_secreta = random.sample(palavras_filtradas, qtd_palavras)

            # Aplicar opções
            if upper:
                frase_secreta = [p.capitalize() for p in frase_secreta]
            if num:
                idx = random.randint(0, len(frase_secreta) - 1)
                frase_secreta[idx] += str(random.randint(0, 9))

            # Separação
            separador = random.choice(".") # random.choice("#!@.$%&*")
            senha = separador.join(frase_secreta)

        return {'password': senha}

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e)) 


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
