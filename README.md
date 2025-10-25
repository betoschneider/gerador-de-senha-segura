# 🔒 Gerador de Senha Segura

Aplicação web desenvolvida com **Flask** (backend) e **Streamlit** (frontend) para gerar **senhas seguras** e **frases secretas** de forma personalizável, com layout moderno e API REST-friendly.

---

## 🚀 Principais Atualizações

### 🔗 **API REST-friendly**
A API agora segue um padrão mais limpo e consistente, facilitando o uso por outras aplicações.

**Endpoint atualizado:**

---

### 🧩 **Geração de Senhas**
- Agora a senha **garante que todas as opções selecionadas estarão presentes**  
  (ex: se `upper`, `lower` e `num` forem `True`, a senha terá ao menos um caractere de cada tipo).
- O conjunto de caracteres especiais foi **restringido**.

- Tamanho máximo limitado a 25 caracteres para segurança e legibilidade.

---

### ✍️ **Geração de Frases Secretas**
- As frases são geradas a partir de um corpus dinâmico criado com a biblioteca `Faker`, em diferentes idiomas (`pt_BR`, `en_US`, `es_CL`, `fr_FR`).
- Sempre inclui **um separador aleatório** sorteado.
- O separador não é mais configurável no frontend (removido o input manual).
- As opções de **iniciais maiúsculas** e **números aleatórios** continuam disponíveis.

---

### 💅 **Interface Atualizada (Frontend)**
- O seletor principal foi atualizado de `radio` para **pílulas interativas** (`st.pills`), proporcionando uma experiência moderna e fluida.
- Layout simplificado, removendo o campo de escolha do separador para frases secretas.
- Mensagens de erro e validação mais claras, impedindo geração sem opções válidas.

---

## 🧠 Tecnologias Utilizadas

| Camada | Tecnologia |
|---------|-------------|
| Backend | Flask, Faker, NLTK |
| Frontend | Streamlit |
| Containerização | Docker |
| Linguagem | Python 3.10+ |

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seuusuario/gerador-de-senha-segura.git
cd gerador-de-senha-segura
```

### 2. Suba os containers
```bash
docker compose up -d
```

### 3. Acesse a aplicação
- Frontend: http://localhost:8502
- API: http://localhost:5001/password

## 🧪 Exemplos de Uso
### 🔐 Senha
```bash
GET /password?type=senha&len=10&upper=true&lower=true&num=true&special=false
→ "Ac3pLnVgWh"
```

### 💬 Frase Secreta
```bash
GET /password?type=frase&len=4&lang=pt_BR&upper=true&num=true&special=true
→ "Dados.Azul3.Luz"
```

---

## 👨‍💻 Autor
**Roberto Schneider**  
Desenvolvedor e entusiasta de automação, segurança e aplicações web modernas.
🌐 [betoschneider.com](https://betoschneider.com)