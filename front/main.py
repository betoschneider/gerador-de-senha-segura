import streamlit as st
import requests

# Função para chamar a API e obter a senha
def get_senha_api(tipo, tamanho, opcoes):
    api_url = f'http://api:5001/senha?type={tipo}&len={tamanho}&options={opcoes}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('senha')
        else:
            st.error(f"Erro ao chamar a API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao chamar a API: {e}")
        return None

# Configuração da página e ocultação de elementos padrão do Streamlit
st.set_page_config(page_title="Gerador de Senha Segura")
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.header('Gerador de Senha Segura')

# Seletor para alternar entre formulários
form_choice = st.radio("Escolha o tipo:", ["Senha", "Frase Secreta"], index=1)

if form_choice == "Senha":
    tipo = "senha"
    with st.form('senha_segura'):
        tamanho = st.number_input(
            'Tamanho da senha',
            min_value=4,
            max_value=25,
            value=12
        )
        opcao1 = st.checkbox('Letra maiúscula', value=True)
        opcao2 = st.checkbox('Letra minúscula', value=True)
        opcao3 = st.checkbox('Número', value=True)
        opcao4 = st.checkbox('Símbolo', value=True)
        submit = st.form_submit_button('Gerar senha')

    # Criando a string de opções
    opcoes = ''
    if opcao1:
        opcoes += 'uppercase,'
    if opcao2:
        opcoes += 'lowercase,'
    if opcao3:
        opcoes += 'number,'
    if opcao4:
        opcoes += 'symbol,'

    if len(opcoes) == 0:
        st.error('Ao menos uma opção deve ser selecionada.')

    if submit and len(opcoes) > 0:
        senha_gerada = get_senha_api(tipo, tamanho, opcoes)
        if senha_gerada:
            st.divider()
            col1, col2 = st.columns([1, 2])
            col1.text('Senha:')
            col2.text(senha_gerada)
            st.divider()

elif form_choice == "Frase Secreta":
    tipo = "frase"
    with st.form('frase_secreta'):
        tamanho = st.number_input(
            'Número de palavras na frase',
            min_value=2,
            max_value=10,
            value=3
        )
        iniciais_maiusculas = st.checkbox('Iniciais Em Maiúsculas', value=True)
        incluir_numeros = st.checkbox('Incluir números', value=True)
        separador = st.text_input('Separador', value='-')
        submit_frase = st.form_submit_button('Gerar frase secreta')
    
    # Criando a string de opções
    opcoes = ''
    if iniciais_maiusculas:
        opcoes += 'uppercase,'
    if incluir_numeros:
        opcoes += 'number,'
    
    # Adicionando o separador
    if not separador:
        separador = 'º'
    opcoes += separador[0]

    if submit_frase:
        frase_gerada = get_senha_api(tipo, tamanho, opcoes)
        if frase_gerada:
            st.divider()
            col1, col2 = st.columns([1, 2])
            col1.text('Frase Secreta:')
            col2.text(frase_gerada)
            st.divider()