# TechStack Signals Pipeline 

Este projeto demonstra uma arquitetura ponta a ponta de Engenharia de Dados e Inteligência Artificial para análise de risco de crédito e saúde financeira corporativa. 

A solução utiliza **PySpark (Spark SQL)** local para processar grandes volumes de dados financeiros e um **Agente de IA** para executar validações heurísticas automatizadas de qualidade e governança (QA).

## 🛠️ Arquitetura do Projeto

1. **Ingestão (Bronze):** Leitura de dados históricos estruturados de balanços corporativos (`company_data.csv`).
2. **Processamento (Silver/Gold):** Pipeline ETL em PySpark para limpeza, renomeação de colunas críticas e agregação de indicadores financeiros (ROA, Net Income Growth, Net Income Ratio) agrupados por status de falência.
3. **Consumo de Dados:** Exportação dos dados tratados para um sumário executivo em CSV (`market_intelligence_summary.csv`).
4. **Camada de IA (QA Layer):** Um Agente de IA consome o sumário, aplica regras de validação estatística em lote e gera um relatório auditável em formato JSON corporativo.

## Tecnologias Utilizadas

* **Python 3.12+**
* **Apache Spark / PySpark 3.5+**
* **Amazon Corretto OpenJDK 11** (Ambiente de execução Java estável)
* **Pandas & Setuptools** (Conversão de DataFrames e compatibilidade de ambiente)

## Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o **Java 11 (JDK)** instalado e a variável de ambiente `JAVA_HOME` configurada no seu sistema.

### 2. Instalar Dependências
Ative seu ambiente virtual e instale os pacotes necessários:
```bash
.\venv\Scripts\activate
pip install -r requirements.txt