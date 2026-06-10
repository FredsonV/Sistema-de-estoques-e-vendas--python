c# 📦 Sistema de Estoque e Vendas

> Sistema de linha de comando para controle de produtos, vendas e relatórios.
> 
> Desenvolvido em Python como **Projeto 1** — Seções 2 a 5.

---

## 👥 Autores

- 🧑‍💻 Arthur Lima
- 🧑‍💻 Bruno Juvenal
- 🧑‍💻 Fredson Vicente
- 🧑‍💻 Gustavo Dias
- 🧑‍💻 Igor Medeiros
- 🧑‍💻 Otávio Cruz

---

## 🚀 Como executar

### 📋 Pré-requisitos

- Python 3.9 ou superior
- Nenhuma biblioteca externa (apenas biblioteca padrão)

### 📝 Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/estoque-vendas.git
cd estoque-vendas

# Execute o sistema
python main.py
```

> 💡 **Dica:** O arquivo de dados (`data/produtos.json`) é criado automaticamente ao salvar.
> Um arquivo de exemplo já está incluso com 8 produtos.

---

## 🗂️ Estrutura do projeto

```
estoque-vendas/
├── main.py              # 🎯 Menu principal e fluxo da aplicação
├── produto.py           # 📦 Classe Produto, validações e leitura de entrada
├── estoque.py           # 🏭 Operações de estoque (busca, cadastro, vendas)
├── arquivos.py          # 💾 Persistência em JSON
├── logger.py            # 📝 Log simples de operações
├── data/
│   └── produtos.json    # 📊 Dados persistidos
├── logs/
│   └── operacoes.log    # 📋 Histórico de operações com data/hora
└── README.md            # 📖 Este arquivo
```

---

## ✨ Funcionalidades

| Opção | Funcionalidade | Complexidade |
|:-----:|---|---|
| 1️⃣ | Cadastrar produto (código único) | O(n) |
| 2️⃣ | Editar produto (nome, preço, quantidade, categoria) | O(log n) |
| 3️⃣ | Remover produto pelo código | O(n) |
| 4️⃣ | Buscar por código — **Busca Binária** | **O(log n)** ⚡ |
| 5️⃣ | Buscar por nome — **Busca Linear** | O(n) |
| 6️⃣ | Registrar venda (valida estoque) | O(log n) |
| 7️⃣ | Listar todos ordenados por código | O(n) |
| 8️⃣ | Relatórios (estoque baixo, preços, categoria) | O(n) |

---

## 💻 Exemplo de uso

```
╔══════════════════════════════════════╗
║   Sistema de Estoque e Vendas  v1.0  ║
╚══════════════════════════════════════╝

  ✔  8 produto(s) carregado(s) do arquivo.

  1. Cadastrar produto
  2. Editar produto
  ...
  Produtos cadastrados: 8

  Opção: 4

══════════════════════════════════════════
  🔍 Buscar por Código [Busca Binária O(log n)]
══════════════════════════════════════════
  Código: BEB001

  ✔  Encontrado:
  [BEB001] Água Mineral 500ml | Categoria: Bebidas | Preço: R$ 2.00 | Estoque: 200 un.
```

---

## 🔧 Relatório de Escolhas Técnicas

### 1️⃣ Estruturas de dados

O sistema mantém **dois vetores paralelos** para os mesmos objetos `Produto`:

- **`_vetor_ordenado`** 📊 — Lista Python mantida sempre ordenada por código.
  
  Garante a aplicabilidade da busca binária.

- **`_vetor_nao_ord`** 📝 — Lista na ordem de inserção.
  
  Representa o cadastro inicial e serve como base para a busca linear por nome.

### 2️⃣ Busca Binária — `buscar_por_codigo()` — **O(log n)** ⚡

**Onde:** `estoque.py → _busca_binaria_indice()`

**Justificativa:** Como o vetor é mantido ordenado por código após cada inserção/remoção, é possível aplicar a divisão binária do espaço de busca. A cada iteração, metade dos elementos é descartada. Para 1.000 produtos, o pior caso é ~10 comparações (log₂ 1000 ≈ 10). Para busca por código único e exato, essa é a escolha ideal.

### 3️⃣ Busca Linear — `buscar_por_nome()` — **O(n)**

**Onde:** `estoque.py → buscar_por_nome()`

**Justificativa:** A busca é por **substring** no nome (ex: "arroz" encontra "Arroz Branco 5kg"). Não existe uma ordenação por nome que permita busca binária eficiente para substrings. É necessário verificar cada elemento. Para esse tipo de consulta, O(n) é o melhor possível sem estruturas auxiliares (como índices invertidos ou tries), que estão fora do escopo das seções 2–5.

### 4️⃣ Inserção ordenada — **O(n)**

**Onde:** `estoque.py → cadastrar()`

A posição de inserção é encontrada em O(log n) (busca binária adaptada), mas o deslocamento de elementos no array para abrir espaço é O(n). Essa é a complexidade de inserção em listas encadeadas vs. arrays — uma compensação consciente pela simplicidade da implementação.

### 5️⃣ Persistência em JSON

✅ Escolhido por ser legível, suportado nativamente pelo Python e facilmente inspecionável.

📌 CSV seria mais simples, mas menos robusto para campos com vírgulas ou quebras de linha.

---

## 📋 Regras de negócio aplicadas

- ✅ Código único por produto (validado na inserção com busca binária)
- ✅ Preço deve ser positivo (`preco > 0`)
- ✅ Quantidade não pode ser negativa (`quantidade >= 0`)
- ✅ Venda exige estoque suficiente (`quantidade_venda <= estoque`)
- ✅ Todos os dados são salvos automaticamente após cada operação

---

## 📐 PEP 8

O código segue rigorosamente as convenções da **PEP 8**:

- 🐍 `snake_case` para variáveis e funções
- 🏛️ `PascalCase` para classes
- 📝 Docstrings em todos os módulos, classes e funções públicas
- 📏 Linhas com no máximo 88 caracteres
- 📦 Importações organizadas por módulo padrão → módulos locais

---

<div align="center">
</div>
