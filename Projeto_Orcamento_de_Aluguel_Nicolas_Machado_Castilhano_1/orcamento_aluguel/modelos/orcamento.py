"""
Classe que monta o orcamento final.

Aqui aparece a COMPOSICAO: o orcamento nao herda de ninguem, ele e formado por
tres objetos que ja sabem cuidar de si mesmos. Um cliente, um imovel e um
contrato. O orcamento so pergunta a cada um o que precisa e junta o resultado.

Repare que nao existe nenhum "se for apartamento" neste arquivo. O orcamento
funciona igual para os tres tipos porque cada imovel sabe calcular o proprio
aluguel. Isso e o polimorfismo funcionando na pratica.
"""

import csv
import io
from datetime import datetime

MESES_DO_CSV = 12


class Orcamento:
    """Orcamento de aluguel gerado para um cliente."""

    def __init__(self, cliente, imovel, contrato):
        self._cliente = cliente
        self._imovel = imovel
        self._contrato = contrato
        self._gerado_em = datetime.now()

    # ---------------- leitura ----------------

    @property
    def cliente(self):
        return self._cliente

    @property
    def imovel(self):
        return self._imovel

    @property
    def contrato(self):
        return self._contrato

    @property
    def gerado_em(self):
        return self._gerado_em.strftime("%d/%m/%Y as %H:%M")

    # ---------------- calculos ----------------

    @property
    def aluguel_mensal(self):
        """Valor do aluguel ja com adicionais e desconto aplicados."""
        return self._imovel.calcular_aluguel(self._cliente)

    @property
    def desconto(self):
        """Quanto o cliente economizou. Zero quando nao ha desconto."""
        return self._imovel.calcular_desconto(self._cliente)

    @property
    def total_primeiro_mes(self):
        """Aluguel somado a primeira parcela do contrato."""
        return round(self.aluguel_mensal + self._contrato.valor_parcela, 2)

    @property
    def total_doze_meses(self):
        """Tudo que o cliente vai desembolsar no primeiro ano."""
        return round(
            self.aluguel_mensal * MESES_DO_CSV + self._contrato.valor_total, 2
        )

    def detalhar_itens(self):
        """
        Lista os itens que compoem o aluguel, para exibir na tela.

        Cada item e uma dupla com descricao e valor. O desconto entra com
        valor negativo, o que deixa a soma da coluna bater com o total.
        """
        itens = list(self._imovel.descrever())
        if self.desconto > 0:
            itens.append(("Desconto de 5% para cliente sem criancas",
                          -self.desconto))
        return itens

    def montar_parcelas(self):
        """
        Monta a tabela dos 12 meses.

        Devolve uma lista de dicionarios, um por mes, com o aluguel, a parcela
        do contrato daquele mes e o total. E essa lista que vira o arquivo CSV
        e tambem a tabela exibida na tela.
        """
        parcelas = []
        for mes in range(1, MESES_DO_CSV + 1):
            valor_contrato = self._contrato.valor_no_mes(mes)
            parcelas.append({
                "mes": mes,
                "aluguel": self.aluguel_mensal,
                "contrato": valor_contrato,
                "total": round(self.aluguel_mensal + valor_contrato, 2),
            })
        return parcelas

    # ---------------- exportacao ----------------

    def gerar_csv(self):
        """
        Gera o conteudo do arquivo CSV com as 12 parcelas.

        Escreve em memoria com io.StringIO em vez de gravar direto no disco.
        Assim o mesmo metodo serve tanto para salvar um arquivo quanto para
        entregar o download pelo navegador.

        O separador e o ponto e virgula e o decimal e a virgula, que e o
        formato que o Excel brasileiro abre sem precisar de configuracao.
        """
        buffer = io.StringIO()
        escritor = csv.writer(buffer, delimiter=";")

        escritor.writerow(["Orcamento de Aluguel - Imobiliaria R.M."])
        escritor.writerow(["Cliente", self._cliente.nome])
        escritor.writerow(["Imovel", self._imovel.tipo])
        escritor.writerow(["Gerado em", self.gerado_em])
        escritor.writerow([])

        escritor.writerow(["Mes", "Aluguel (R$)", "Contrato (R$)", "Total (R$)"])
        for linha in self.montar_parcelas():
            escritor.writerow([
                linha["mes"],
                self._formatar(linha["aluguel"]),
                self._formatar(linha["contrato"]),
                self._formatar(linha["total"]),
            ])

        escritor.writerow([])
        escritor.writerow([
            "TOTAL",
            self._formatar(self.aluguel_mensal * MESES_DO_CSV),
            self._formatar(self._contrato.valor_total),
            self._formatar(self.total_doze_meses),
        ])

        return buffer.getvalue()

    def salvar_csv(self, caminho="orcamento.csv"):
        """Grava o CSV em um arquivo no disco e devolve o caminho usado."""
        with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
            arquivo.write(self.gerar_csv())
        return caminho

    @staticmethod
    def _formatar(valor):
        """Converte 1234.5 em '1234,50', no padrao brasileiro."""
        return f"{valor:.2f}".replace(".", ",")

    def __str__(self):
        return (f"Orcamento de {self._cliente.nome}: {self._imovel.tipo}, "
                f"aluguel de R$ {self.aluguel_mensal:.2f}")
