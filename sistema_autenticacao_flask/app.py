import time
from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from seguranca import validar_forca_senha, gerar_hash, verificar_hash

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "60 per hour"]
)

USUARIOS_DB = {
    "admin_fraco": {
        "senha_texto_puro": "583",
        "senha_hash": gerar_hash("583"),
        "descricao": "Conta com PIN numérico curto de 3 dígitos"
    },
    "admin_forte": {
        "senha_hash": gerar_hash("S3nh@F0rt3#2026"),
        "descricao": "Conta protegida com senha forte"
    }
}

CONTROLE_TENTATIVAS = {}
LIMITE_FALHAS = 5
TEMPO_BLOQUEIO_SEGUNDOS = 60

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login-sem-protecao", methods=["POST"])
def login_sem_protecao():
    dados = request.get_json(silent=True) or request.form
    usuario = dados.get("usuario", "admin_fraco")
    senha = str(dados.get("senha", ""))

    registro = USUARIOS_DB.get(usuario)
    if registro and verificar_hash(registro["senha_hash"], senha):
        return jsonify({"status": "sucesso", "mensagem": f"Autenticado com sucesso como '{usuario}'!"}), 200

    return jsonify({"status": "erro", "mensagem": "Credenciais inválidas."}), 401

@app.route("/api/login-protegido", methods=["POST"])
@limiter.limit("5 per minute")
def login_protegido():
    dados = request.get_json(silent=True) or request.form
    usuario = dados.get("usuario", "admin_fraco")
    senha = str(dados.get("senha", ""))

    agora = time.time()
    estado = CONTROLE_TENTATIVAS.get(usuario, {"falhas": 0, "bloqueado_ate": 0})

    if agora < estado["bloqueado_ate"]:
        restante = int(estado["bloqueado_ate"] - agora)
        return jsonify({"status": "bloqueado", "mensagem": f"Conta temporariamente bloqueada. Aguarde {restante}s."}), 429

    registro = USUARIOS_DB.get(usuario)
    if registro and verificar_hash(registro["senha_hash"], senha):
        CONTROLE_TENTATIVAS.pop(usuario, None)
        return jsonify({"status": "sucesso", "mensagem": f"Autenticado com sucesso como '{usuario}'!"}), 200

    estado["falhas"] += 1
    if estado["falhas"] >= LIMITE_FALHAS:
        estado["bloqueado_ate"] = agora + TEMPO_BLOQUEIO_SEGUNDOS
        estado["falhas"] = 0
        CONTROLE_TENTATIVAS[usuario] = estado
        return jsonify({"status": "bloqueado", "mensagem": f"Limite de {LIMITE_FALHAS} falhas atingido! Bloqueado por {TEMPO_BLOQUEIO_SEGUNDOS}s."}), 429

    CONTROLE_TENTATIVAS[usuario] = estado
    return jsonify({"status": "erro", "mensagem": f"Credenciais inválidas."}), 401

@app.route("/api/validar-senha", methods=["POST"])
def api_validar_senha():
    dados = request.get_json(silent=True) or request.form
    senha = str(dados.get("senha", ""))
    valida, erros = validar_forca_senha(senha)

    return jsonify({
        "valida": valida,
        "erros": erros,
        "mensagem": "Senha forte aprovada!" if valida else "A senha não atende aos critérios de segurança."
    }), 200 if valida else 400

@app.route("/api/reset-bloqueios", methods=["POST"])
def reset_bloqueios():
    CONTROLE_TENTATIVAS.clear()
    return jsonify({"status": "ok", "mensagem": "Contadores de bloqueio reiniciados."})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)