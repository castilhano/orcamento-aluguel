"""
Fabrica de imoveis.

Este arquivo resolve um problema pratico: o formulario devolve texto, e o
programa precisa de objetos. A fabrica e o unico lugar do projeto que decide
qual classe instanciar. Toda a aplicacao depois disso trabalha apenas com a
classe abstrata Imovel, sem saber com qual tipo esta lidando.

Se um dia a R.M. passar a alugar salas comerciais, basta criar a classe Sala e
registrar ela aqui. Nenhum outro arquivo precisa mudar.
"""

from modelos.imovel import Apartamento, Casa, Estudio

# Liga o texto que vem do formulario a classe correspondente.
TIPOS_DISPONIVEIS = {
    "apartamento": Apartamento,
    "casa": Casa,
    "estudio": Estudio,
}


def converter_inteiro(valor, nome_campo, minimo=0):
    """
    Converte o texto do formulario em numero inteiro.

    Atende ao requisito de nao aceitar texto onde se espera numero. Se o
    usuario digitar "dois" ou "3a", o int() falha e devolvemos uma mensagem
    explicando qual campo esta errado.
    """
    texto = str(valor if valor is not None else "").strip()

    if texto == "":
        return None, f"O campo {nome_campo} e obrigatorio."

    try:
        numero = int(texto)
    except ValueError:
        return None, f"O campo {nome_campo} aceita apenas numeros inteiros."

    if numero < minimo:
        return None, f"O campo {nome_campo} nao pode ser menor que {minimo}."

    return numero, None


def criar_imovel(tipo, quartos=1, tem_garagem=False, vagas=0):
    """
    Cria o objeto de imovel do tipo pedido.

    Devolve (imovel, None) quando da certo e (None, mensagem) quando algum
    dado esta invalido.
    """
    tipo = str(tipo or "").strip().lower()

    if tipo not in TIPOS_DISPONIVEIS:
        return None, "Escolha um tipo de imovel valido."

    try:
        if tipo == "estudio":
            return Estudio(vagas=vagas), None

        classe = TIPOS_DISPONIVEIS[tipo]
        return classe(quartos=quartos, tem_garagem=tem_garagem), None

    except ValueError as erro:
        # As proprias classes levantam ValueError quando recebem dado ruim.
        # A fabrica so traduz isso em mensagem para a tela.
        return None, str(erro)
