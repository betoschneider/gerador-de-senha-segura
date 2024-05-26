import streamlit as st
import requests


# Função para chamar a API e obter a senha
def get_senha_api(tamanho, opcoes):
    api_url = f'http://api:5000/senha?len={tamanho}&options={opcoes}'
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

st.set_page_config(page_title="Streamlit + Docker" #, layout="wide"
                   )
#ocultar opção deploy na página
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

st.header('Gerador de Senha')


with st.form('senha_segura'):
    tamanho = st.number_input(
            'Tamanho da senha',
             min_value=4,
             max_value=25,
             value=12)
    tipo1 = st.checkbox('Letra maiúscula', value=True)
    tipo2 = st.checkbox('Letra minuscula', value=True)
    tipo3 = st.checkbox('Número', value=True)
    tipo4 = st.checkbox('Símbolo', value=True)
    submit = st.form_submit_button('Gerar senha')

#criando a string de opções
opcoes = ''
if tipo1:
    opcoes += 'uppercase,'
if tipo2:
    opcoes += 'lowercase,'
if tipo3:
    opcoes += 'number,'
if tipo4:
    opcoes += 'symbol,'

if len(opcoes)==0:
    st.error('Ao menos uma opção deve ser selecionada.')

if submit and len(opcoes)>0:
    senha_gerada = get_senha_api(tamanho, opcoes)
    if senha_gerada:
        st.divider()
        col1, col2 = st.columns([1, 2])
        col1.text('Senha:')
        col2.text(senha_gerada)
        st.divider()
        