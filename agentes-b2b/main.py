from crewai import Agent, Task, Crew, Process

# recebendo dados do ESP tool ou evento?


analista = Agent(
    role="Analista de dados de luminosidade",
    goal=(
        "Analisar os dados de luminosidade recebidos do sensor, "
        "identificar se estão dentro ou fora da especificação e "
        "gerar um relatório direcionado ao setor responsável."
    ),
    backstory=(
        "Você é um analista especializado no monitoramento de sensores "
        "de luminosidade em ambientes industriais. Sua função é analisar "
        "as leituras recebidas, compará-las com a especificação definida "
        "e identificar possíveis situações que necessitem de atenção. "
        "Valores entre 100 e 1000 lux estão dentro da especificação. "
        "Valores abaixo de 100 lux ou acima de 1000 lux estão fora da "
        "especificação."
    ),
    verbose=True
)


analisar_luminosidade = Task(
    description=(
        '''
        Analise o dado de luminosidade recebido do sensor:

        {luminosidade}

        A especificação do sensor é:
        - Entre 100 e 1000 lux: DENTRO DA ESPECIFICAÇÃO;
        - Abaixo de 100 lux ou acima de 1000 lux: FORA DA ESPECIFICAÇÃO.

        Com base no dado recebido:

        1. Identifique o valor de luminosidade;
        2. Determine se o valor está dentro ou fora da especificação;
        3. Caso esteja FORA da especificação, gere um relatório
           direcionado à equipe de sustentação, descrevendo a situação
           identificada e a necessidade de atenção;
        4. Caso esteja DENTRO da especificação, gere um relatório
           direcionado à direção, apresentando os impactos positivos
           das condições adequadas de luminosidade.
        '''
    ),
    expected_output=(
        "Um relatório em Markdown contendo o valor de luminosidade, "
        "a classificação (dentro ou fora da especificação), o setor "
        "destinatário e a análise correspondente à situação identificada."
    ),
    agent=analista
)


equipe = Crew(
    agents=[analista],
    tasks=[analisar_luminosidade],
    process=Process.sequential,
    verbose=True
)


resultado = equipe.kickoff(
    inputs={
        "luminosidade": (
            "450 lux"
        )
    }
)

print(resultado.raw)