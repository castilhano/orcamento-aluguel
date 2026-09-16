# Orçamento de Aluguel — Imobiliária R.M.

Aplicação que gera o orçamento mensal de aluguel de casas, apartamentos e
estúdios, com o contrato parcelado e exportação das 12 parcelas em CSV.

**Aluno:** Nicolas Machado Castilhano
**Curso:** Análise e Desenvolvimento de Sistemas
**Disciplina:** Algorithmic Thinking and Introduction to Object-Oriented Programming
**Instituição:** Centro Universitário UniFECAF

---

## Como rodar

**Modo rápido:** dê dois cliques no arquivo `INICIAR.bat`.
Ele instala o que falta, abre o navegador e sobe a aplicação.

**Modo manual:** abra o terminal nesta pasta e rode:

```
pip install -r requirements.txt
python app.py
```

Depois acesse `http://localhost:5000` no navegador.

Para encerrar, aperte `Ctrl + C` na janela do terminal.

---

## Estrutura do projeto

```
orcamento_aluguel/
├── app.py                  interface web (Flask), sem regras de negócio
├── INICIAR.bat             atalho que instala e executa tudo
├── requirements.txt        bibliotecas necessárias
├── modelos/                as classes do sistema
│   ├── imovel.py           classe abstrata Imovel + Apartamento, Casa, Estudio
│   ├── cliente.py          dados do cliente
│   ├── contrato.py         contrato de R$ 2.000 e suas parcelas
│   ├── orcamento.py        junta tudo, projeta 12 meses e gera o CSV
│   └── fabrica.py          cria o objeto de imóvel certo e valida números
├── templates/              telas em HTML
├── static/css/             folha de estilo
└── docs/                   documentação, fluxograma e diagrama de classes
```

---

## Regras de cálculo

| Item | Valor | Condição |
|------|-------|----------|
| Apartamento | R$ 700,00 | valor base, 1 quarto |
| Casa | R$ 900,00 | valor base, 1 quarto |
| Estúdio | R$ 1.200,00 | valor base |
| Segundo quarto | R$ 200,00 | apartamento |
| Segundo quarto | R$ 250,00 | casa |
| Garagem | R$ 300,00 | casa e apartamento |
| Estacionamento | R$ 250,00 | estúdio, já inclui 2 vagas |
| Vaga adicional | R$ 60,00 | estúdio, da terceira vaga em diante |
| Desconto | 5% do aluguel | apartamento, cliente sem crianças |
| Contrato | R$ 2.000,00 | divisível em até 5 vezes |

---

## Orientação a objetos

| Conceito | Onde aparece |
|----------|--------------|
| Abstração | `Imovel` herda de `ABC` e tem métodos `@abstractmethod`. Não pode ser instanciada. |
| Herança | `Apartamento`, `Casa` e `Estudio` herdam de `Imovel`. |
| Polimorfismo | `calcular_adicionais()` existe nas três com regras diferentes. |
| Encapsulamento | Atributos com underline, lidos por `@property`, com validação interna. |
| Composição | `Orcamento` é formado por um `Cliente`, um `Imovel` e um `Contrato`. |

O arquivo `orcamento.py` não contém nenhum `if` para diferenciar tipo de imóvel.
Essa ausência é proposital e é o principal resultado da modelagem adotada.

---

## Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3 | linguagem da aplicação |
| Flask | rotas e servidor web |
| Jinja2 | templates HTML |
| csv e io | geração do arquivo das 12 parcelas |

Nenhuma biblioteca externa além do Flask. As classes da pasta `modelos`
funcionam em Python puro e não dependem da interface.
