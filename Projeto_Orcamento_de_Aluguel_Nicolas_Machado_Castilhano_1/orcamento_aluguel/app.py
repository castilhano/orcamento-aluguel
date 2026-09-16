"""
Orcamento de Aluguel - Imobiliaria R.M.
Disciplina: Algorithmic Thinking and Introduction to Object-Oriented Programming

Este arquivo e apenas a interface. Ele recebe o que o usuario digitou, monta os
objetos e mostra o resultado na tela.

Repare que nenhuma regra de negocio mora aqui. Nenhum valor de aluguel, nenhum
percentual de desconto, nenhuma conta. Tudo isso esta nas classes da pasta
modelos. Se a R.M. mudar o preco do apartamento amanha, este arquivo nao muda
nem uma linha.

Para rodar:
    python app.py
Depois abra http://localhost:5000 no navegador.
"""

from flask import Flask, Response, render_template, request

from modelos.cliente import Cliente
from modelos.contrato import Contrato
from modelos.fabrica import converter_inteiro, criar_imovel
from modelos.orcamento import Orcamento

app = Flask(__name__)


@app.template_filter("moeda")
def formatar_moeda(valor):
    """
    Formata um numero no padrao brasileiro: 1234.5 vira 1.234,50.

    O Python formata no padrao americano por padrao, com virgula separando
    milhar e ponto no decimal. Aqui trocamos os dois de lugar.
    """
    texto = f"{abs(float(valor)):,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return texto


def montar_orcamento(formulario):
    """
    Transforma os dados do formulario em um objeto Orcamento.

    Devolve (orcamento, None) quando da tudo certo e (None, mensagem) no
    primeiro erro encontrado. A ordem das validacoes segue a ordem dos campos
    na tela, para que a mensagem faca sentido para quem esta preenchendo.
    """
    tipo = formulario.get("tipo", "")

    # --- cliente ---
    try:
        cliente = Cliente(
            nome=formulario.get("nome", ""),
            possui_criancas=(formulario.get("criancas") == "sim"),
        )
    except ValueError as erro:
        return None, str(erro)

    # --- campos numericos, validados antes de chegar nas classes ---
    quartos, vagas = 1, 0

    if tipo in ("apartamento", "casa"):
        quartos, erro = converter_inteiro(
            formulario.get("quartos"), "quartos", minimo=1
        )
        if erro:
            return None, erro

    if tipo == "estudio":
        vagas, erro = converter_inteiro(
            formulario.get("vagas"), "vagas de estacionamento", minimo=0
        )
        if erro:
            return None, erro

    # --- imovel, criado pela fabrica ---
    imovel, erro = criar_imovel(
        tipo=tipo,
        quartos=quartos,
        tem_garagem=(formulario.get("garagem") == "sim"),
        vagas=vagas,
    )
    if erro:
        return None, erro

    # --- contrato ---
    parcelas, erro = converter_inteiro(
        formulario.get("parcelas"), "parcelas do contrato", minimo=1
    )
    if erro:
        return None, erro

    try:
        contrato = Contrato(parcelas=parcelas)
    except ValueError as erro:
        return None, str(erro)

    return Orcamento(cliente, imovel, contrato), None


@app.route("/", methods=["GET", "POST"])
def inicio():
    """Mostra o formulario e, quando enviado, o orcamento calculado."""
    if request.method == "POST":
        orcamento, erro = montar_orcamento(request.form)

        if erro:
            # Devolve o formulario com a mensagem e o que ja foi digitado.
            return render_template("formulario.html", erro=erro, dados=request.form)

        return render_template("resultado.html", orcamento=orcamento,
                               dados=request.form)

    return render_template("formulario.html", erro=None, dados=None)


@app.route("/baixar-csv", methods=["POST"])
def baixar_csv():
    """Gera o arquivo CSV com as 12 parcelas e envia para download."""
    orcamento, erro = montar_orcamento(request.form)

    if erro:
        return render_template("formulario.html", erro=erro, dados=request.form)

    nome_arquivo = (
        f"orcamento_{orcamento.cliente.nome.split()[0].lower()}_"
        f"{orcamento.imovel.tipo.lower()}.csv"
    )

    # utf-8-sig coloca a marca que o Excel usa para abrir acentos corretamente.
    return Response(
        orcamento.gerar_csv().encode("utf-8-sig"),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )


if __name__ == "__main__":
    print("Orcamento de Aluguel - Imobiliaria R.M.")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, port=5000)
