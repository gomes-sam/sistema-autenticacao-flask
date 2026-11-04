import re
from werkzeug.security import generate_password_hash, check_password_hash

SENHAS_COMUNS = {
    "123456", "12345678", "senha", "password", "qwerty", "111111", "000000", "admin123"
}

def validar_forca_senha(senha: str) -> tuple[bool, list[str]]:
    """
    Verifica se a senha atende aos requisitos de segurança.
    """
    erros = []

    if senha.lower() in SENHAS_COMUNS:
        erros.append("A senha escolhida é muito comum e previsível.")

    if len(senha) < 8:
        erros.append("A senha deve ter no mínimo 8 caracteres.")

    if not re.search(r"[A-Z]", senha):
        erros.append("A senha deve conter pelo menos uma letra maiúscula.")

    if not re.search(r"[a-z]", senha):
        erros.append("A senha deve conter pelo menos uma letra minúscula.")

    if not re.search(r"\d", senha):
        erros.append("A senha deve conter pelo menos um número.")

    # Correção: Uso de aspas simples ( r'...' ) por fora para não dar conflito com a aspa dupla por dentro
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\]', senha):
        erros.append("A senha deve conter pelo menos um caractere especial.")

    return (len(erros) == 0, erros)

def gerar_hash(senha: str) -> str:
    return generate_password_hash(senha)

def verificar_hash(hash_armazenado: str, senha_informada: str) -> bool:
    return check_password_hash(hash_armazenado, senha_informada)