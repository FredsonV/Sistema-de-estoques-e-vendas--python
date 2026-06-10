"""
estoque.py - Operações de estoque: cadastro, busca, ordenação e vendas.

Complexidade das operações:
────────────────────────────────────────────────────────────────
Busca por código   → Busca Binária em vetor ordenado → O(log n)
    Justificativa: o vetor é mantido ordenado por código após
    cada inserção/remoção usando inserção ordenada. Com o vetor
    ordenado garantido, a busca binária divide o espaço de busca
    pela metade a cada passo, resultando em O(log n).

Busca por nome     → Busca Linear em vetor não ordenado → O(n)
    Justificativa: nomes não possuem uma ordem natural pré-
    definida e a busca é por substring (parcial). Não há como
    aplicar busca binária; é necessário percorrer todos os
    elementos. Complexidade linear O(n).

Inserção ordenada  → O(n)
    Justificativa: encontrar a posição certa é O(log n) com
    busca binária, mas deslocar os elementos subsequentes é O(n).

Remoção            → O(n)
    Justificativa: após localizar o item (O(log n)), o vetor
    precisa ser compactado, deslocando os elementos → O(n).

Listagem completa  → O(n)
    Justificativa: percorre todos os elementos uma vez.
────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

from typing import Optional

from produto import Produto
from logger import registrar_log


class Estoque:
    
    """
    Gerencia dois vetores paralelos:
    - _vetor_ordenado  : lista mantida ordenada por código (busca binária).
    - _vetor_nao_ord   : lista de inserção na ordem de cadastro (busca linear por nome).

    Ambos contêm os mesmos objetos Produto; a separação deixa explícita
    a diferença de estrutura exigida pelo enunciado.
    """

    LIMITE_ESTOQUE_BAIXO_PADRAO = 5

    def __init__(self):
        self._vetor_ordenado: list[Produto] = []    # ordenado por código
        self._vetor_nao_ord: list[Produto] = []     # ordem de inserção

    # Propriedade pública (leitura)

    @property
    def produtos_ordenados(self) -> list[Produto]:
        return list(self._vetor_ordenado)

    @property
    def total_produtos(self) -> int:
        return len(self._vetor_ordenado)

    # Busca Binária — O(log n)

    def _busca_binaria_indice(self, codigo: str) -> int:
        codigo = codigo.strip().upper()
        esq, dir_ = 0, len(self._vetor_ordenado) - 1
        while esq <= dir_:
            meio = (esq + dir_) // 2
            cod_meio = self._vetor_ordenado[meio].codigo
            if cod_meio == codigo:
                return meio
            if cod_meio < codigo:
                esq = meio + 1
            else:
                dir_ = meio - 1
        return -1

    def _posicao_insercao(self, codigo: str) -> int:
        esq, dir_ = 0, len(self._vetor_ordenado)
        while esq < dir_:
            meio = (esq + dir_) // 2
            if self._vetor_ordenado[meio].codigo < codigo:
                esq = meio + 1
            else:
                dir_ = meio
        return esq

    # Cadastro — O(n) por causa do deslocamento no vetor ordenado

    def cadastrar(self, produto: Produto) -> None:
        if self._busca_binaria_indice(produto.codigo) != -1:
            raise ValueError(f"Código '{produto.codigo}' já cadastrado.")
        pos = self._posicao_insercao(produto.codigo)
        self._vetor_ordenado.insert(pos, produto)
        self._vetor_nao_ord.append(produto)
        registrar_log(f"CADASTRO: {produto.codigo} - {produto.nome}")

    # Busca por código — O(log n)

    def buscar_por_codigo(self, codigo: str) -> Optional[Produto]:
        idx = self._busca_binaria_indice(codigo)
        return self._vetor_ordenado[idx] if idx != -1 else None

    # Busca por nome — O(n)

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        nome_lower = nome.strip().lower()
        return [p for p in self._vetor_nao_ord if nome_lower in p.nome.lower()]

    # Edição — O(log n) busca + O(1) edição

    def editar(
        self,
        codigo: str,
        novo_nome: Optional[str] = None,
        novo_preco: Optional[float] = None,
        nova_quantidade: Optional[int] = None,
        nova_categoria: Optional[str] = None,
    ) -> Produto:
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise ValueError(f"Produto '{codigo}' não encontrado.")
        if novo_nome:
            produto.nome = novo_nome.strip()
        if nova_categoria:
            produto.categoria = nova_categoria.strip()
        if novo_preco is not None:
            if novo_preco <= 0:
                raise ValueError("Preço deve ser positivo.")
            produto.preco = novo_preco
        if nova_quantidade is not None:
            if nova_quantidade < 0:
                raise ValueError("Quantidade não pode ser negativa.")
            produto.quantidade = nova_quantidade
        registrar_log(f"EDICAO: {produto.codigo} - {produto.nome}")
        return produto

    # Remoção — O(n)

    def remover(self, codigo: str) -> Produto:
        idx = self._busca_binaria_indice(codigo)
        if idx == -1:
            raise ValueError(f"Produto '{codigo}' não encontrado.")
        produto = self._vetor_ordenado.pop(idx)
        self._vetor_nao_ord.remove(produto)
        registrar_log(f"REMOCAO: {produto.codigo} - {produto.nome}")
        return produto
    
    # Venda — O(log n)

    def registrar_venda(self, codigo: str, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise ValueError("Quantidade da venda deve ser positiva.")
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise ValueError(f"Produto '{codigo}' não encontrado.")
        if produto.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto.quantidade} un."
            )
        produto.quantidade -= quantidade
        registrar_log(
            f"VENDA: {produto.codigo} - {produto.nome} | Qtd: {quantidade} | "
            f"Estoque restante: {produto.quantidade}"
        )
        return produto

    # Relatórios — O(n)

    def listar_por_categoria(self, categoria: str) -> list[Produto]:
        cat = categoria.strip().lower()
        return [p for p in self._vetor_ordenado if p.categoria.lower() == cat]

    def estoque_baixo(self, limite: int = LIMITE_ESTOQUE_BAIXO_PADRAO) -> list[Produto]:
        return [p for p in self._vetor_ordenado if p.quantidade < limite]

    def menor_preco(self) -> Optional[Produto]:
        if not self._vetor_ordenado:
            return None
        return min(self._vetor_ordenado, key=lambda p: p.preco)

    def maior_preco(self) -> Optional[Produto]:
        if not self._vetor_ordenado:
            return None
        return max(self._vetor_ordenado, key=lambda p: p.preco)

    def categorias(self) -> list[str]:
        return sorted({p.categoria for p in self._vetor_ordenado})
    
    # Carga em massa (usado por arquivos.py)

    def carregar_produtos(self, produtos: list[Produto]) -> None:
        self._vetor_ordenado.clear()
        self._vetor_nao_ord.clear()
        for p in sorted(produtos, key=lambda x: x.codigo):
            pos = self._posicao_insercao(p.codigo)
            self._vetor_ordenado.insert(pos, p)
            self._vetor_nao_ord.append(p)