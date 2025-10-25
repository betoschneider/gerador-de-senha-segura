import streamlit as st
import requests

# Função para chamar a API e obter a senha
def get_senha_api(tipo='senha', len=3, upper=True, lower=True, num=True, special=True, idioma='pt_BR'):
    api_url = f'http://api:5001/password?type={tipo}&len={len}&upper={upper}&lower={lower}&num={num}&special={special}&lang={idioma}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('password')
        else:
            st.error(f"Erro ao chamar a API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao chamar a API: {e}")
        return None

# Configuração da página
st.set_page_config(
    page_title="Gerador de Senha Segura - betoschneider.com",
    page_icon="🔒",
)
st.markdown("""
    <style>
        .reportview-container { margin-top: -2em; }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.header('Gerador de Senha Segura')

# Seletor principal
form_choice = st.pills(
    "Escolha o tipo:",
    options=["Frase Secreta", "Senha"],
    selection_mode="single",
    default="Frase Secreta",
)

# ========================================
# FORMULÁRIO PARA SENHA
# ========================================
if form_choice == "Senha":
    tipo = "senha"

    with st.form('senha_segura'):
        len = st.number_input(
            'Tamanho da senha',
            min_value=4,
            max_value=25,
            value=12
        )
        upper = st.checkbox('Letra maiúscula', value=True)
        lower = st.checkbox('Letra minúscula', value=True)
        num = st.checkbox('Número', value=True)
        special = st.checkbox('Símbolo', value=True)
        submit = st.form_submit_button('Gerar senha')

    selecao = any([upper, lower, num, special])

    if not selecao:
        st.error('Ao menos uma opção deve ser selecionada.')

    if submit and selecao:
        senha_gerada = get_senha_api(tipo, len, upper, lower, num, special)
        if senha_gerada:
            st.divider()
            col1, col2 = st.columns([1, 2])
            col1.text('Senha:')
            col2.text(senha_gerada)
            st.divider()

# ========================================
# FORMULÁRIO PARA FRASE SECRETA
# ========================================
elif form_choice == "Frase Secreta":
    tipo = "frase"
    with st.form('frase_secreta'):
        len = st.number_input(
            'Número de palavras na frase',
            min_value=2,
            max_value=10,
            value=3
        )
        upper = st.checkbox('Iniciais Em Maiúsculas', value=True)
        num = st.checkbox('Incluir números', value=True)
        
        # Mapeamento das linguagens
        linguagens = {
            'Português': 'pt_BR',
            'Espanhol': 'es_CL',
            'Inglês': 'en_US',
            'Francês': 'fr_FR'
        }
        linguagens_ordenada = sorted(list(linguagens.keys()))
        index_padrao = linguagens_ordenada.index('Português')
        linguagem_selecionada = st.selectbox('Idioma', linguagens_ordenada, index=index_padrao)
        idioma = linguagens[linguagem_selecionada]
        
        submit_frase = st.form_submit_button('Gerar frase secreta')
        lower = True  # Não usados na geração de frase
        special = True # Não usados na geração de frase
    
    
    if submit_frase:
        frase_gerada = get_senha_api(tipo, len, upper, lower, num, special, idioma)
        if frase_gerada:
            st.divider()
            col1, col2 = st.columns([1, 2])
            col1.text('Frase Secreta:')
            col2.text(frase_gerada)
            st.divider()
