"""
Tradução direta do pseudocódigo da atividade para execução local em memória.
Demonstra a complexidade linear O(N) de testar combinações numéricas simples (000 a 999)
e por que senhas curtas/previsíveis são inseguras.
"""

def executar_algoritmo_pseudocodigo():
    senha_correta = 583
    tentativa = 0
    encontrada = False

    print("=== Iniciando simulação local do pseudocódigo ===")
    while tentativa <= 999 and not encontrada:
        print(f"Testando senha: {tentativa:03d}")

        if tentativa == senha_correta:
            encontrada = True
            print(f"\n[!] Senha encontrada na tentativa {tentativa:03d}!")
        else:
            tentativa += 1

    if not encontrada:
        print("\nSenha não encontrada.")

if __name__ == "__main__":
    executar_algoritmo_pseudocodigo()
