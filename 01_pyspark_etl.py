import os
import sys


os.environ['_JAVA_OPTIONS'] = (
    '--add-opens=java.base/javax.security.auth=ALL-UNNAMED '
    '--add-opens=java.base/java.lang=ALL-UNNAMED '
    '--add-opens=java.base/java.util=ALL-UNNAMED'
)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round

def main():
    print("\n=== [STEP 1] Inicializando Sessão Spark (Simulando o Databricks) ===")
    
    
    spark = SparkSession.builder \
        .appName("YipitDataSignalsKagglePipeline") \
        .master("local[*]") \
        .getOrCreate()

    print("=== [STEP 2] Carregando o Dataset baixado do Kaggle ===")
    
    df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv("company_data.csv")
    
    print("=== [STEP 3] Selecionando e Renomeando as colunas críticas ===")
    
    df_cleaned = df_raw.select(
        col("Bankrupt?").alias("is_bankrupt"),
        col(" ROA(C) before interest and depreciation before interest").alias("roa_before_interest"),
        col(" Net Value Growth Rate").alias("net_value_growth_rate"),
        col(" Net Income to Total Assets").alias("net_income_to_total_assets")
    )

    
    df_cleaned.createOrReplaceTempView("investment_signals")

    print("=== [STEP 4] Executando Queries Spark SQL Avançadas ===")
    
    market_intelligence_query = """
        SELECT 
            is_bankrupt,
            COUNT(*) as total_companies,
            ROUND(AVG(roa_before_interest), 4) as avg_roa,
            ROUND(AVG(net_value_growth_rate), 4) as avg_net_value_growth,
            ROUND(AVG(net_income_to_total_assets), 4) as avg_net_income_ratio
        FROM investment_signals
        GROUP BY is_bankrupt
    """
    
    
    result_df = spark.sql(market_intelligence_query)
    result_df.show(truncate=False)

    print("=== [STEP 5] Exportando os dados limpos para consumo do Agente de IA ===")
    
    result_df.toPandas().to_csv("market_intelligence_summary.csv", index=False)
    
    
    spark.stop()
    print("=== [SUCCESS] Pipeline de Dados concluída com sucesso! ===\n")

if __name__ == "__main__":
    main()