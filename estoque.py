from __future__ import annotations

from typing import Optional

from produto import Produto
from logger import registrar_log


class Estoque:

    LIMITE_ESTOQUE_BAIXO_PADRAO = 5

    def __init__(self):
        self._vetor_ordenado: list[Produto] = []
        self._vetor_nao_ord: list[Produto] = []

    @property
    def produtos_ordenados(self) -> list[Produto]:
        return list(self._vetor_ordenado)

    @property
    def total_produtos(self) -> int:
        return len(self._vetor_ordenado)

    def cadastrar(self, produto: Produto) -> None:
        for p in self._vetor_ordenado:
            if p.codigo == produto.codigo:
                raise ValueError(f"Código '{produto.codigo}' já cadastrado.")
        self._vetor_ordenado.append(produto)
        self._vetor_nao_ord.append(produto)
        registrar_log(f"CADASTRO: {produto.codigo} - {produto.nome}")

    def carregar_produtos(self, produtos: list[Produto]) -> None:
        self._vetor_ordenado.clear()
        self._vetor_nao_ord.clear()
        for p in produtos:
            self._vetor_ordenado.append(p)
            self._vetor_nao_ord.append(p)