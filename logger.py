import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "operacoes.log")


def registrar_log(mensagem: str) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{agora}] {mensagem}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linha)
    except OSError:
        pass