"""
Hierarquia de imoveis da imobiliaria R.M.

Este arquivo concentra os quatro conceitos de orientacao a objetos usados no
trabalho:

ABSTRACAO    A classe Imovel define o que todo imovel tem em comum, mas nao
             pode ser instanciada sozinha. Ela e um contrato: quem herdar dela
             precisa dizer como calcula o proprio aluguel.

HERANCA      Apartamento, Casa e Estudio herdam de Imovel e reaproveitam tudo
             que ja esta pronto na classe mae.

POLIMORFISMO O metodo calcular_adicionais() existe nas tres subclasses com o
             mesmo nome, mas com regras diferentes. Quem chama nao precisa
             saber qual tipo de imovel esta na mao.

ENCAPSULAMENTO Os atributos comecam com underline e sao lidos por propriedades.
             As validacoes ficam dentro da classe, entao nao existe imovel em
             estado invalido.
"""

from abc import ABC, abstractmethod

# Valor unico do contrato imobiliario, igual para qualquer tipo de imovel.
VALOR_CONTRATO = 2000.00
MAXIMO_PARCELAS_CONTRATO = 5


class Imovel(ABC):
    """
    Classe abstrata. Representa qualquer imovel alugado pela R.M.

    ABC vem de Abstract Base Class. Uma classe que herda de ABC e tem pelo
    menos um metodo marcado com @abstractmethod nao pode ser instanciada:
    tentar criar Imovel() diretamente levanta um erro. Isso e proposital,
    porque "imovel" sozinho nao existe no mundo real da imobiliaria. O que
    existe e apartamento, casa ou estudio.
    """

    def __init__(self, valor_base, tem_garagem=False):
        self._valor_base = valor_base
        self._tem_garagem = bool(tem_garagem)

    # ---------------- encapsulamento ----------------

    @property
    def valor_base(self):
        """Valor de tabela do imovel, antes de qualquer adicional."""
        return self._valor_base

    @property
    def tem_garagem(self):
        return self._tem_garagem

    # ---------------- metodos abstratos ----------------

    @abstractmethod
    def calcular_adicionais(self):
        """
        Soma tudo que e cobrado alem do valor de tabela.

        Cada subclasse implementa do seu jeito, porque as regras da R.M. sao
        diferentes para apartamento, casa e estudio.
        """

    @abstractmethod
    def descrever(self):
        """Devolve a lista de itens do orcamento, para exibir na tela."""

    @property
    @abstractmethod
    def tipo(self):
        """Nome do tipo de imovel, usado nos textos e no arquivo CSV."""

    # ---------------- metodos concretos ----------------

    def calcular_desconto(self, cliente):
        """
        Desconto aplicado ao aluguel.

        Na classe mae o desconto e sempre zero. Somente Apartamento
        sobrescreve este metodo, porque a regra de 5% para quem nao tem
        criancas vale so para apartamentos.
        """
        return 0.0

    def calcular_aluguel(self, cliente):
        """
        Calcula o aluguel mensal final.

        Este metodo e o coracao do polimorfismo: ele vale para os tres tipos
        de imovel sem nenhum "se for apartamento faca isso". Quem responde
        pelas diferencas sao os metodos que cada subclasse implementou.
        """
        subtotal = self.valor_base + self.calcular_adicionais()
        return round(subtotal - self.calcular_desconto(cliente), 2)

    def __str__(self):
        """Texto amigavel do objeto, util para depuracao."""
        return f"{self.tipo} (base R$ {self.valor_base:.2f})"


class Apartamento(Imovel):
    """
    Apartamento.

    Regras da R.M.:
      valor base R$ 700,00 para 1 quarto
      2 quartos acrescentam R$ 200,00
      garagem acrescenta R$ 300,00
      desconto de 5% no aluguel para cliente sem criancas
    """

    VALOR_BASE = 700.00
    ADICIONAL_SEGUNDO_QUARTO = 200.00
    ADICIONAL_GARAGEM = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = 0.05

    def __init__(self, quartos=1, tem_garagem=False):
        # super() chama o construtor da classe mae, reaproveitando o que ja
        # esta escrito la em vez de repetir codigo aqui.
        super().__init__(self.VALOR_BASE, tem_garagem)
        self._quartos = self._validar_quartos(quartos)

    @staticmethod
    def _validar_quartos(quartos):
        """Apartamentos da R.M. tem 1 ou 2 quartos."""
        if int(quartos) not in (1, 2):
            raise ValueError("Apartamento aceita apenas 1 ou 2 quartos.")
        return int(quartos)

    @property
    def quartos(self):
        return self._quartos

    @property
    def tipo(self):
        return "Apartamento"

    def calcular_adicionais(self):
        total = 0.0
        if self._quartos == 2:
            total += self.ADICIONAL_SEGUNDO_QUARTO
        if self.tem_garagem:
            total += self.ADICIONAL_GARAGEM
        return total

    def calcular_desconto(self, cliente):
        """
        Sobrescreve o metodo da classe mae.

        Este e o unico tipo de imovel com desconto. O percentual incide sobre
        o valor ja somado com os adicionais, que e o valor do aluguel.
        """
        if cliente.possui_criancas:
            return 0.0
        base_do_desconto = self.valor_base + self.calcular_adicionais()
        return round(base_do_desconto * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS, 2)

    def descrever(self):
        itens = [(f"Apartamento com {self._quartos} quarto"
                  f"{'s' if self._quartos > 1 else ''}", self.VALOR_BASE)]
        if self._quartos == 2:
            itens.append(("Adicional pelo segundo quarto",
                          self.ADICIONAL_SEGUNDO_QUARTO))
        if self.tem_garagem:
            itens.append(("Vaga de garagem", self.ADICIONAL_GARAGEM))
        return itens


class Casa(Imovel):
    """
    Casa.

    Regras da R.M.:
      valor base R$ 900,00 para 1 quarto
      2 quartos acrescentam R$ 250,00
      garagem acrescenta R$ 300,00
      casa nao tem desconto
    """

    VALOR_BASE = 900.00
    ADICIONAL_SEGUNDO_QUARTO = 250.00
    ADICIONAL_GARAGEM = 300.00

    def __init__(self, quartos=1, tem_garagem=False):
        super().__init__(self.VALOR_BASE, tem_garagem)
        self._quartos = self._validar_quartos(quartos)

    @staticmethod
    def _validar_quartos(quartos):
        if int(quartos) not in (1, 2):
            raise ValueError("Casa aceita apenas 1 ou 2 quartos.")
        return int(quartos)

    @property
    def quartos(self):
        return self._quartos

    @property
    def tipo(self):
        return "Casa"

    def calcular_adicionais(self):
        total = 0.0
        if self._quartos == 2:
            total += self.ADICIONAL_SEGUNDO_QUARTO
        if self.tem_garagem:
            total += self.ADICIONAL_GARAGEM
        return total

    # Casa nao sobrescreve calcular_desconto: herda o zero da classe mae.

    def descrever(self):
        itens = [(f"Casa com {self._quartos} quarto"
                  f"{'s' if self._quartos > 1 else ''}", self.VALOR_BASE)]
        if self._quartos == 2:
            itens.append(("Adicional pelo segundo quarto",
                          self.ADICIONAL_SEGUNDO_QUARTO))
        if self.tem_garagem:
            itens.append(("Vaga de garagem", self.ADICIONAL_GARAGEM))
        return itens


class Estudio(Imovel):
    """
    Estudio.

    Regras da R.M.:
      valor base R$ 1.200,00, sem divisao por quartos
      estacionamento custa R$ 250,00 e ja da direito a 2 vagas
      cada vaga alem da segunda custa R$ 60,00
      estudio nao tem desconto
    """

    VALOR_BASE = 1200.00
    VALOR_ESTACIONAMENTO = 250.00
    VAGAS_INCLUSAS = 2
    VALOR_VAGA_EXTRA = 60.00

    def __init__(self, vagas=0):
        # Estudio nao usa o conceito de garagem de casa e apartamento, entao
        # passa tem_garagem como False e trata as vagas na propria classe.
        super().__init__(self.VALOR_BASE, tem_garagem=False)
        self._vagas = self._validar_vagas(vagas)

    @staticmethod
    def _validar_vagas(vagas):
        vagas = int(vagas)
        if vagas < 0:
            raise ValueError("O numero de vagas nao pode ser negativo.")
        return vagas

    @property
    def vagas(self):
        return self._vagas

    @property
    def vagas_extras(self):
        """Quantas vagas passam das duas que ja vem inclusas."""
        return max(0, self._vagas - self.VAGAS_INCLUSAS)

    @property
    def tipo(self):
        return "Estudio"

    def calcular_adicionais(self):
        if self._vagas == 0:
            return 0.0
        total = self.VALOR_ESTACIONAMENTO
        total += self.vagas_extras * self.VALOR_VAGA_EXTRA
        return total

    def descrever(self):
        itens = [("Estudio", self.VALOR_BASE)]
        if self._vagas > 0:
            inclusas = min(self._vagas, self.VAGAS_INCLUSAS)
            itens.append((f"Estacionamento com {inclusas} vaga"
                          f"{'s' if inclusas > 1 else ''}",
                          self.VALOR_ESTACIONAMENTO))
        if self.vagas_extras > 0:
            itens.append((f"{self.vagas_extras} vaga"
                          f"{'s' if self.vagas_extras > 1 else ''} adiciona"
                          f"{'is' if self.vagas_extras > 1 else 'l'}",
                          self.vagas_extras * self.VALOR_VAGA_EXTRA))
        return itens
