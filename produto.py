from dataclasses import dataclass

@dataclass
class Produto:
    codigo: str
    nome: str
    categoria: str
    preco: float
    quantidade: int

    def __post_init__(self):
        self.validar()

    def validar(self):
        if not self.codigo or not self.codigo.strip():
            raise ValueError("Código não pode ser vazio.")
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if not self.categoria or not self.categoria.strip():
            raise ValueError("Categoria não pode ser vazia.")
        if self.preco <= 0:
            raise ValueError("Preço deve ser positivo.")
        if self.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        self.codigo = self.codigo.strip().upper()
        self.nome = self.nome.strip()
        self.categoria = self.categoria.strip()

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Produto":
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=float(dados["preco"]),
            quantidade=int(dados["quantidade"]),
        )

    def __str__(self) -> str:
        return (
            f"[{self.codigo}] {self.nome} | "
            f"Categoria: {self.categoria} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"Estoque: {self.quantidade} un."
        )

    def __lt__(self, other: "Produto") -> bool:
        return self.codigo < other.codigo

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Produto):
            return False
        return self.codigo == other.codigo

# Funções de validação de entrada (reutilizáveis em outros módulos)

def ler_string(prompt: str, obrigatorio: bool = True) -> str:
    """Lê uma string do terminal com validação de vazio."""
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        if not obrigatorio:
            return ""
        print("Campo obrigatório. Digite um valor.")


def ler_float(prompt: str, minimo: float = 0.0, exclusivo: bool = True) -> float:
    """Lê um número decimal com validação de intervalo."""
    while True:
        texto = input(prompt).strip().replace(",", ".")
        try:
            valor = float(texto)
            if exclusivo and valor <= minimo:
                print(f"O valor deve ser maior que {minimo}.")
            elif not exclusivo and valor < minimo:
                print(f"O valor deve ser ≥ {minimo}.")
            else:
                return valor
        except ValueError:
            print("Número inválido. Use apenas dígitos e vírgula/ponto decimal.")


def ler_int(prompt: str, minimo: int = 0) -> int:
    """Lê um número inteiro com validação de intervalo."""
    while True:
        texto = input(prompt).strip()
        try:
            valor = int(texto)
            if valor < minimo:
                print(f"O valor deve ser ≥ {minimo}.")
            else:
                return valor
        except ValueError:
            print("Número inteiro inválido.")