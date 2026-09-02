from crewai import Agent, Task, Crew, Process

# recebendo dados do esp tool ou evento?



analista = Agent(
    role="Analista de chamados corporativos",
    goal="Analisar chamados e identificar prioridade, impacto e possíveis causas",
    backstory=(
        "Você é um analista de suporte sênior especializado em sistemas "
        "corporativos, infraestrutura e aplicações B2B."
    ),
    verbose=True
)

analisar_chamado = Task(
    description=(
        '''
        Analise o chamado abaixo:
        {chamado}
        Identifique:
        1. Categoria do problema;
        2. Prioridade;
        3. Impacto no negócio;
        4. Possíveis causas;
        5. Informações adicionais necessárias;
        6. Próxima ação recomendada.
        '''

    ),
    expected_output=(
        "Um relatório em Markdown com categoria, prioridade, impacto, possíveis causas, perguntas ao cliente e próximos passos."

    ),
    agent=analista
)

equipe = Crew(
    agents=[analista],
    tasks=[analisar_chamado],
    process=Process.sequential,
    verbose=True

)

resultado = equipe.kickoff(
    inputs={
        "chamado":(
            "O cliente informa que o sistema demora cerca de 25 segundos "
            "para abrir as ordens de manutenção. O problema começou hoje "
            "e está afetando todos os usuários da empresa."

        )
    }
)
print(resultado.raw)

