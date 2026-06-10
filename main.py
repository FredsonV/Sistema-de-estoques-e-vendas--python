import os
import sys

import arquivos
from estoque import Estoque
from produto import Produto, ler_float, ler_int, ler_string

LIMITE_ESTOQUE_BAIXO = 5   # pode ser alterado pelo usuário em runtime
PAGINA_TAMANHO = 10        # itens por página na listagem

# Interação terminal de terminal

def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\n  Pressione ENTER para continuar...")


def cabecalho(titulo: str) -> None:
    print("\n" + "═" * 55)
    print(f"  {titulo}")
    print("═" * 55)


def paginar(itens: list, titulo: str = "Resultados") -> None:
    if not itens:
        print("  (nenhum item encontrado)")
        return
    total = len(itens)
    pagina = 0
    total_paginas = (total + PAGINA_TAMANHO - 1) // PAGINA_TAMANHO
    while True:
        inicio = pagina * PAGINA_TAMANHO
        fim = min(inicio + PAGINA_TAMANHO, total)
        print(f"\n  {titulo}  [página {pagina + 1}/{total_paginas}]")
        print("  " + "-" * 53)
        for p in itens[inicio:fim]:
            print(f"  {p}")
        print("  " + "-" * 53)
        print(f"  Mostrando {inicio + 1}–{fim} de {total}")
        if total_paginas == 1:
            break
        nav = input("\n  [P]róxima  [A]nterior  [S]air → ").strip().upper()
        if nav == "P" and pagina < total_paginas - 1:
            pagina += 1
        elif nav == "A" and pagina > 0:
            pagina -= 1
        elif nav == "S":
            break

# Ações do menu

def cadastrar_produto(est: Estoque) -> None:
    cabecalho("Cadastrar Produto")
    codigo = ler_string("  Código   : ").upper()
    nome = ler_string("  Nome     : ")
    categoria = ler_string("  Categoria: ")
    preco = ler_float("  Preço    : R$ ")
    quantidade = ler_int("  Qtd      : ")
    try:
        p = Produto(codigo, nome, categoria, preco, quantidade)
        est.cadastrar(p)
        arquivos.salvar(est)
        print(f"\n  ✔  Produto '{nome}' cadastrado com sucesso!")
    except ValueError as e:
        print(f"\n  ✖  Erro: {e}")


def editar_produto(est: Estoque) -> None:
    cabecalho("Editar Produto")
    codigo = ler_string("  Código do produto: ").upper()
    produto = est.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto atual: {produto}")
    print("  (deixe em branco para não alterar o campo)\n")
    novo_nome = input(f"  Novo nome [{produto.nome}]: ").strip() or None
    nova_cat = input(f"  Nova categoria [{produto.categoria}]: ").strip() or None
    preco_str = input(f"  Novo preço [{produto.preco:.2f}]: ").strip().replace(",", ".")
    novo_preco = float(preco_str) if preco_str else None
    qtd_str = input(f"  Nova quantidade [{produto.quantidade}]: ").strip()
    nova_qtd = int(qtd_str) if qtd_str else None
    try:
        est.editar(codigo, novo_nome, novo_preco, nova_qtd, nova_cat)
        arquivos.salvar(est)
        print("\n  ✔  Produto atualizado com sucesso!")
    except ValueError as e:
        print(f"\n  ✖  Erro: {e}")


def remover_produto(est: Estoque) -> None:
    cabecalho("Remover Produto")
    codigo = ler_string("  Código do produto: ").upper()
    produto = est.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto: {produto}")
    confirmacao = input("  Confirmar remoção? (s/N): ").strip().lower()
    if confirmacao == "s":
        est.remover(codigo)
        arquivos.salvar(est)
        print("\n  ✔  Produto removido com sucesso!")
    else:
        print("\n  Operação cancelada.")


def buscar_por_codigo(est: Estoque) -> None:
    cabecalho("Buscar por Código  [Busca Binária O(log n)]")
    codigo = ler_string("  Código: ").upper()
    produto = est.buscar_por_codigo(codigo)
    if produto:
        print(f"\n  ✔  Encontrado:\n  {produto}")
    else:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")


def buscar_por_nome(est: Estoque) -> None:
    cabecalho("Buscar por Nome  [Busca Linear O(n)]")
    nome = ler_string("  Nome (parcial): ")
    resultados = est.buscar_por_nome(nome)
    paginar(resultados, f"Resultados para '{nome}'")


def registrar_venda(est: Estoque) -> None:
    cabecalho("Registrar Venda")
    codigo = ler_string("  Código do produto: ").upper()
    produto = est.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto: {produto}")
    quantidade = ler_int("  Quantidade vendida: ", minimo=1)
    try:
        est.registrar_venda(codigo, quantidade)
        arquivos.salvar(est)
        total = quantidade * produto.preco
        print(f"\n  ✔  Venda registrada! Total: R$ {total:.2f}")
        print(f"  Estoque restante: {produto.quantidade} un.")
    except ValueError as e:
        print(f"\n  ✖  Erro: {e}")


def listar_por_codigo(est: Estoque) -> None:
    cabecalho("Produtos Ordenados por Código")
    paginar(est.produtos_ordenados, "Todos os produtos")


def listar_por_categoria(est: Estoque) -> None:
    cabecalho("Listar por Categoria")
    cats = est.categorias()
    if not cats:
        print("  Nenhuma categoria cadastrada.")
        return
    print("  Categorias disponíveis:")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")
    escolha = ler_string("\n  Digite o número ou o nome da categoria: ")
    if escolha.isdigit():
        idx = int(escolha) - 1
        if idx < 0 or idx >= len(cats):
            print("\n  ✖  Número inválido.")
            return
        categoria = cats[idx]
    else:
        categoria = escolha
    resultados = est.listar_por_categoria(categoria)
    paginar(resultados, f"Categoria: {categoria}")


def relatorio_estoque_baixo(est: Estoque) -> None:
    global LIMITE_ESTOQUE_BAIXO
    cabecalho("Relatório de Estoque Baixo")
    print(f"  Limite atual: {LIMITE_ESTOQUE_BAIXO} un.")
    alt = input("  Alterar limite? (s/N): ").strip().lower()
    if alt == "s":
        LIMITE_ESTOQUE_BAIXO = ler_int("  Novo limite: ", minimo=1)
    resultados = est.estoque_baixo(LIMITE_ESTOQUE_BAIXO)
    paginar(resultados, f"Produtos com estoque < {LIMITE_ESTOQUE_BAIXO}")


def relatorio_precos(est: Estoque) -> None:
    cabecalho("Relatório: Menor e Maior Preço")
    menor = est.menor_preco()
    maior = est.maior_preco()
    if menor:
        print(f"\n  💲 Menor preço:\n  {menor}")
    if maior:
        print(f"\n  💲 Maior preço:\n  {maior}")
    if not menor and not maior:
        print("  Nenhum produto cadastrado.")


def menu_relatorios(est: Estoque) -> None:
    while True:
        cabecalho("Relatórios")
        print("  1. Estoque baixo")
        print("  2. Menor e maior preço")
        print("  3. Listar por categoria")
        print("  0. Voltar")
        op = input("\n  Opção: ").strip()
        if op == "1":
            relatorio_estoque_baixo(est)
            pausar()
        elif op == "2":
            relatorio_precos(est)
            pausar()
        elif op == "3":
            listar_por_categoria(est)
            pausar()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

# Menu principal

MENU_PRINCIPAL = """
  1. Cadastrar produto
  2. Editar produto
  3. Remover produto
  4. Buscar por código   [Busca Binária O(log n)]
  5. Buscar por nome     [Busca Linear  O(n)    ]
  6. Registrar venda
  7. Listar todos (ordenado por código)
  8. Relatórios
  0. Sair
"""


def executar() -> None:
    est = Estoque()
    n = arquivos.carregar(est)
    limpar_tela()
    print("\n  ╔══════════════════════════════════╗")
    print("  ║   Sistema de Estoque e Vendas    ║")
    print("  ╚═══════════════════════════════════╝")
    if n:
        print(f"\n  ✔  {n} produto(s) carregado(s) do arquivo.")
    else:
        print("\n  ℹ  Nenhum dado salvo encontrado. Iniciando vazio.")

    acoes = {
        "1": cadastrar_produto,
        "2": editar_produto,
        "3": remover_produto,
        "4": buscar_por_codigo,
        "5": buscar_por_nome,
        "6": registrar_venda,
        "7": listar_por_codigo,
    }

    while True:
        print(MENU_PRINCIPAL)
        print(f"  Produtos cadastrados: {est.total_produtos}")
        op = input("  Opção: ").strip()
        limpar_tela()

        if op in acoes:
            acoes[op](est)
            pausar()
        elif op == "8":
            menu_relatorios(est)
        elif op == "0":
            print("\n  Salvando dados...")
            arquivos.salvar(est)
            print("  Até logo! 👋\n")
            sys.exit(0)
        else:
            print("  ⚠  Opção inválida. Tente novamente.")
            pausar()


if __name__ == "__main__":
    executar()