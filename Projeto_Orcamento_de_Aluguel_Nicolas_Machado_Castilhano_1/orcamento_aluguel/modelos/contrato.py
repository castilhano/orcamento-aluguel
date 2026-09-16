"""
Classe que representa o contrato imobiliario.

O contrato e uma cobranca unica de R$ 2.000,00, separada do aluguel e paga em
ate 5 vezes. Como ele tem regra propria, virou uma classe propria em vez de
ficar solto dentro do orcamento.
"""

from modelos.imovel import MAXIMO_PARCELAS_CONTRATO, VALOR_CONTRATO


class Contrato:
    """Contrato imobiliario cobrado na assinatura."""

    def __init__(self, parcelas=1):
        self._valor_total = VALOR_CONTRATO
        self._parcelas = self._validar_parcelas(parcelas)

    @staticmethod
    def _validar_parcelas(parcelas):
        """O contrato pode ser dividido em 1 ate 5 vezes."""
        try:
            parcelas = int(parcelas)
        except (TypeError, ValueError):
            raise ValueError("O numero de parcelas precisa ser um numero inteiro.")

        if parcelas < 1 or parcelas > MAXIMO_PARCELAS_CONTRATO:
            raise ValueError(
                f"O contrato pode ser dividido em 1 ate "
                f"{MAXIMO_PARCELAS_CONTRATO} vezes."
            )
        return parcelas

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def parcelas(self):
        return self._parcelas

    @property
    def valor_parcela(self):
        """Valor de cada parcela do contrato."""
        return round(self._valor_total / self._parcelas, 2)

    def valor_no_mes(self, mes):
        """
        Quanto do contrato cai em um mes especifico.

        O contrato e cobrado nos primeiros meses. Do mes seguinte em diante o
        cliente paga somente o aluguel. Esse metodo e o que monta a coluna de
        contrato no arquivo CSV das 12 parcelas.
        """
        return self.valor_parcela if mes <= self._parcelas else 0.0

    def __str__(self):
        return (f"Contrato de R$ {self._valor_total:.2f} em {self._parcelas}x "
                f"de R$ {self.valor_parcela:.2f}")
