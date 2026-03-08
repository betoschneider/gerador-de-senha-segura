# 🔒 Gerador de Senha Segura

Aplicação web moderna desenvolvida com **FastAPI** (backend) e **HTML/CSS/JS** (frontend) para gerar **senhas seguras** e **frases secretas** de forma personalizável.

Acesse o [Gerador de Senha Segura](https://betoschneider.com/senha/).

---

## 🚀 Principais Atualizações

### 🔒 **Segurança e Análise de Força**
- **Integração com zxcvbn**: Análise profunda da complexidade da senha/frase.
- **Tempo de Quebra**: Estimativa realista do tempo necessário para um ataque offline.
- **Feedback Visual**: Destaque automático (cor vermelha) para senhas consideradas fracas.

### 🔗 **API REST-friendly**
- Backend em **FastAPI** padronizado na porta **5000**.
- Suporte a **CORS** para comunicação segura.
- Endpoints que retornam não só a senha, mas também o `score` (0-4) e o `time` estimado.

---

## 🧠 Tecnologias Utilizadas

| Camada | Tecnologia |
|---------|-------------|
| Backend | FastAPI, Faker, NLTK, **zxcvbn** |
| Frontend | HTML5, CSS3, JavaScript |
| Servidor Web | Nginx (Alpine) |
| Containerização | Docker & Docker Compose |
| Linguagem | Python 3.12+ |

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seuusuario/gerador-de-senha-segura.git
cd gerador-de-senha-segura
```

### 2. Suba os containers
```bash
docker-compose up --build
```

### 3. Acesse a aplicação
- **Frontend**: http://localhost:8502
- **API**: http://localhost:5000/password

---

## 🧪 Exemplos de Uso da API

### 🔐 Senha
```bash
GET /password?type=senha&len=10&upper=true&lower=true&num=true&special=false
→ {
    "password": "Ac3pLnVgWh",
    "score": 3,
    "time": "8 days"
  }
```

### 💬 Frase Secreta
```bash
GET /password?type=frase&len=4&lang=pt_BR&upper=true&num=true&special=true
→ {
    "password": "Dados.Azul3.Luz",
    "score": 4,
    "time": "centuries"
  }
```

---

## 👨‍💻 Autor
**Roberto Schneider**  
Desenvolvedor e entusiasta de automação, segurança e aplicações web modernas.  
🌐 [betoschneider.com](https://betoschneider.com)