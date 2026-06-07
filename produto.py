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