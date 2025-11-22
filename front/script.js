document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('form');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(tab.dataset.target).classList.add('active');

            // Hide result when switching tabs
            document.getElementById('result-container').style.display = 'none';
        });
    });

    // Range Sliders
    const pwdLength = document.getElementById('pwd-length');
    const pwdLengthVal = document.getElementById('pwd-length-val');
    pwdLength.addEventListener('input', (e) => pwdLengthVal.textContent = e.target.value);

    const phraseLength = document.getElementById('phrase-length');
    const phraseLengthVal = document.getElementById('phrase-length-val');
    phraseLength.addEventListener('input', (e) => phraseLengthVal.textContent = e.target.value);

    // API Call
    async function generate(type, params) {
        const btn = document.querySelector(`form.active .generate-btn`);
        const originalText = btn.textContent;
        btn.textContent = 'Gerando...';
        btn.disabled = true;

        try {
            const query = new URLSearchParams(params).toString();
            // Using relative URL, proxied by Nginx to the API container
            // No leading slash to support subpath deployments (e.g. /senha)
            const apiUrl = `api/password?type=${type}&${query}`;

            const response = await fetch(apiUrl);
            const data = await response.json();

            if (response.ok) {
                showResult(data.password);
            } else {
                alert('Erro: ' + (data.error || 'Falha desconhecida'));
            }
        } catch (error) {
            console.error(error);
            alert('Erro ao conectar com a API. Verifique se ela está rodando.');
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    }

    // Password Submit
    document.getElementById('password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const params = {
            len: document.getElementById('pwd-length').value,
            upper: document.getElementById('pwd-upper').checked,
            lower: document.getElementById('pwd-lower').checked,
            num: document.getElementById('pwd-num').checked,
            special: document.getElementById('pwd-special').checked
        };

        if (!params.upper && !params.lower && !params.num && !params.special) {
            alert('Selecione pelo menos uma opção!');
            return;
        }

        generate('senha', params);
    });

    // Passphrase Submit
    document.getElementById('passphrase-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const params = {
            len: document.getElementById('phrase-length').value,
            lang: document.getElementById('phrase-lang').value,
            upper: document.getElementById('phrase-upper').checked,
            num: document.getElementById('phrase-num').checked
        };
        generate('frase', params);
    });

    // Show Result
    function showResult(text) {
        const container = document.getElementById('result-container');
        const input = document.getElementById('result-output');

        container.style.display = 'block';
        input.value = text;

        // Scroll to result on mobile
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Copy to Clipboard
    document.getElementById('copy-btn').addEventListener('click', () => {
        const input = document.getElementById('result-output');
        input.select();
        input.setSelectionRange(0, 99999); // Mobile

        navigator.clipboard.writeText(input.value).then(() => {
            const feedback = document.getElementById('copy-feedback');
            feedback.classList.add('show');
            setTimeout(() => feedback.classList.remove('show'), 2000);
        });
    });

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Check local storage
    if (localStorage.getItem('theme') === 'light') {
        body.classList.add('light-mode');
    }

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        if (body.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light');
        } else {
            localStorage.setItem('theme', 'dark');
        }
    });
});
