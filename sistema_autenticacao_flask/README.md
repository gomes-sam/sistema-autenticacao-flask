# Laboratório de Segurança: Autenticação, Senhas Fracas e Mitigações em Flask

Este projeto contém a estrutura de estudo para a atividade sobre **Autenticação, Senhas Fracas e Mecanismos de Defesa (Rate Limiting, Account Lockout e Hashing)**.

## Estrutura do Projeto

- `algoritmo_local.py`: Tradução direta do pseudocódigo da atividade executando localmente em memória (laço de `000` a `999`).
- `app.py`: Servidor Flask com painel web interativo e endpoints comparativos (`/api/login-sem-protecao` e `/api/login-protegido`).
- `seguranca.py`: Módulo responsável pelo hash seguro de senhas (`Werkzeug`) e validação de política de senhas fortes via Regex.
- `templates/index.html` e `static/style.css`: Interface web para testar os modos de login, observar o bloqueio após 5 falhas consecutivas e validar a força de senhas.

## Como Executar

1. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Para rodar a tradução do pseudocódigo em memória:
   ```bash
   python algoritmo_local.py
   ```

4. Para iniciar o servidor web Flask:
   ```bash
   python app.py
   ```
   Acesse no navegador: `http://127.0.0.1:5000`
