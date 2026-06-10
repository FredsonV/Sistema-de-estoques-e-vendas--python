import json
import os
from typing import TYPE_CHECKING

from produto import Produto

if TYPE_CHECKING:
    from estoque import Estoque

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ARQUIVO_DADOS = os.path.join(DATA_DIR, "produtos.json")


def salvar(estoque: "Estoque", caminho: str = ARQUIVO_DADOS) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    dados = [p.to_dict() for p in estoque.produtos_ordenados]
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar(estoque: "Estoque", caminho: str = ARQUIVO_DADOS) -> int:
    if not os.path.exists(caminho):
        return 0
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    produtos = [Produto.from_dict(d) for d in dados]
    estoque.carregar_produtos(produtos)
    return len(produtos)