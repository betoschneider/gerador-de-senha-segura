# 🔒 Gerador de Senha Segura

Aplicação web moderna desenvolvida com **Flask** (backend) e **HTML/CSS/JS** (frontend) para gerar **senhas seguras** e **frases secretas** de forma personalizável.

Acesse o [Gerador de Senha Segura](https://betoschneider.com/senha/).

---

## 🚀 Principais Atualizações

### ✨ **Nova Interface (Frontend)**
- Interface totalmente refeita utilizando **HTML5, CSS3 e JavaScript Vanilla**.
- **Modo Escuro/Claro**: Alternância de tema com persistência de preferência.
- **Design Responsivo**: Otimizado para desktop e mobile.
- **Cópia Rápida**: Botão integrado para copiar a senha gerada para a área de transferência.
- Servido via **Nginx** em container Docker.

### 🔗 **API REST-friendly**
- Backend em Flask padronizado na porta **5000**.
- Suporte a **CORS** para permitir comunicação segura com o frontend.
- Endpoints otimizados para geração de senhas e frases.

---

## 🧠 Tecnologias Utilizadas

| Camada | Tecnologia |
|---------|-------------|
| Backend | Flask, Faker, NLTK |
| Frontend | HTML5, CSS3, JavaScript |
| Servidor Web | Nginx (Alpine) |
| Containerização | Docker & Docker Compose |
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