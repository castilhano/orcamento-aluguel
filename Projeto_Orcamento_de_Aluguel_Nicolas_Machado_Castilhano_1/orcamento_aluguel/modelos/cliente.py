"""
Classe que representa o cliente que pede o orcamento.

Parece simples demais para virar uma classe, e essa impressao e justamente o
ponto interessante: o campo "possui criancas" nao e um detalhe do imovel, e uma
caracteristica da pessoa. Colocar essa informacao no lugar certo e o que permite
que o metodo calcular_desconto receba um cliente e decida sozinho.
"""


class Cliente:
    """Cliente interessado em alugar um imovel da R.M."""

    def __init__(self, nome, possui_criancas=False):
        self._nome = self._validar_nome(nome)
        self._possui_criancas = bool(possui_criancas)

    @staticmethod
    def _validar_nome(nome):
        """Nome em branco nao entra: o orcamento precisa sair no nome de alguem."""
        nome = str(nome or "").strip()
        if not nome:
            raise ValueError("Informe o nome do cliente.")
        return nome

    @property
    def nome(self):
        return self._nome

    @property
    def possui_criancas(self):
        return self._possui_criancas

    def __str__(self):
        situacao = "com criancas" if self._possui_criancas else "sem criancas"
        return f"{self._nome} ({situacao})"
