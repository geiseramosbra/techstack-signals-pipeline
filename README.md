# TechStack Signals Pipeline: Spark and AI Risk Framework

Este projeto simula uma esteira de dados corporativa e escalável para análise de risco de crédito empresarial utilizando a Arquitetura Medalhão (Bronze/Silver/Gold). O pipeline realiza a ingestão e higienização de dados brutos de mercado usando Apache Spark (PySpark), otimiza o armazenamento analítico no formato colunar Parquet e utiliza um Agente de IA para executar regras de validação e gerar relatórios executivos estruturados em formato JSON.

---

## Arquitetura do Pipeline de Dados

O desenho deste projeto segue os padrões modernos de engenharia de Big Data para governança, performance e escalabilidade:
1. **Camada Bronze (Dados Brutos):** Ingestão direta do dataset original (`company_data.csv`) contendo sinais macroeconômicos e registros financeiros históricos de empresas.
2. **Camada Silver (Dados Limpos):** Processamento distribuído via PySpark para eliminar espaços vazios nos cabeçalhos das colunas, sanitizar tipos de dados e selecionar KPIs financeiros críticos, como ROA e margens de lucro líquido.
3. **Camada Gold (Dados de Negócio):** Agregação estatística dos dados de mercado agrupados por segmentação de risco. O dataframe final é persistido localmente utilizando o formato colunar Parquet (`gold_market_intelligence_summary`), garantindo alta compressão de dados e velocidade ideal de leitura.
4. **Camada de IA (Insights Analíticos):** Um framework de garantia de qualidade (QA) que consome os metadados em Parquet, avalia as métricas financeiras agregadas contra diretrizes de crédito automatizadas e gera insights formatados como JSON corporativo padrão.

---

## Tecnologias e Ferramentas

* **Linguagem Principal:** Python 3.11+ / 3.14
* **Motor de Processamento de Big Data:** Apache Spark 3.5.1 (PySpark)
* **Armazenamento de Alta Performance:** PyArrow / Parquet
* **Processamento Analítico:** Pandas
* **IA e Engenharia de Prompts:** LangChain / Framework de API da OpenAI (Arquitetura pronta para LLM)

---

## Estrutura de Saída do Agente de IA (Relatório JSON Corporativo)

Após a execução bem-sucedida do Framework de QA, o Agente de IA avalia o dataset e gera a seguinte análise de crédito estruturada:

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