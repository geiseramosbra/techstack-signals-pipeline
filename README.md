# TechStack Signals Pipeline: Spark and AI Risk Framework

Criei este projeto para desenvolver uma esteira de dados completa voltada para análise de risco de crédito empresarial. A ideia foi aplicar o conceito prático da Arquitetura Medalhão (Bronze, Silver e Gold) para organizar o fluxo de dados: usei o Apache Spark (PySpark) para limpar e consolidar o volume de dados brutos, salvei o resultado final no formato otimizado Parquet e conectei um Agente de IA para validar os indicadores financeiros automaticamente, gerando um relatório pronto em JSON.

---

## Como o Pipeline Foi Estruturado

Dividi o fluxo de dados em etapas claras para garantir organização e boa performance no processamento:

1. **Camada Bronze:** O ponto de partida do projeto, onde leio o arquivo bruto original (`company_data.csv`) que contém o histórico financeiro e os sinais de mercado das empresas.
2. **Camada Silver:** Aqui utilizei o PySpark para fazer a limpeza pesada. Ajustei os nomes das colunas (que vieram cheias de espaços em branco no arquivo original), tratei os tipos de dados e filtrei apenas as métricas essenciais para a análise, como o ROA e a taxa de lucro líquido.
3. **Camada Gold:** Com os dados limpos, fiz as agregações estatísticas agrupando as empresas pelo status de falência. Em vez de salvar em CSV comum, exportei o resultado na pasta `gold_market_intelligence_summary` usando formato Parquet, que é muito mais rápido para leitura e ocupa menos espaço.
4. **Camada de IA:** Desenvolvi um script de validação que funciona como uma auditoria. Ele lê os arquivos Parquet da camada Gold, aplica regras de negócios financeiras e gera um relatório final consolidado.

---

## Tecnologias que Utilizei

* **Linguagem:** Python (versões 3.11 / 3.14)
* **Processamento de Big Data:** Apache Spark 3.5.1 (PySpark)
* **Armazenamento e Performance:** PyArrow e Parquet
* **Manipulação de Dados:** Pandas
* **Estrutura de IA:** LangChain (Arquitetura integrada e pronta para chamadas de modelos LLM)

---

## Exemplo de Resultado Final (Relatório JSON)

Após rodar este é o formato do relatório estruturado gerado com a análise de saúde financeira das empresas:

```json
[
    {
        "segmento": "Falidas (Bankrupt)",
        "metricas_analisadas": {
            "avg_roa": 0.4185,
            "avg_net_income_ratio": 0.7381
        },
        "insight_ia": "CRÍTICO: Empresas Falidas (Bankrupt) apresentam ROA médio preocupante de 0.4185.",
        "status_qa": "REJEITADO - Risco de Crédito Elevado"
    },
    {
        "segmento": "Saudáveis (Solvent)",
        "metricas_analisadas": {
            "avg_roa": 0.5081,
            "avg_net_income_ratio": 0.8101
        },
        "insight_ia": "NORMAL: Métricas para empresas Saudáveis (Solvent) operando dentro dos limites estatísticos.",
        "status_qa": "APROVADO - Padrão de Estabilidade Mapeado"
    }
]