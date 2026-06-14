import os

# Injeção de flags para o Java runtime (Java 16+)
os.environ['_JAVA_OPTIONS'] = (
    '--add-opens=java.base/javax.security.auth=ALL-UNNAMED '
    '--add-opens=java.base/java.lang=ALL-UNNAMED '
    '--add-opens=java.base/java.util=ALL-UNNAMED'
)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, avg, count

def main():
    print("\n=== [STEP 1] Inicializando Sessão Spark ===")
    spark = SparkSession.builder \
        .appName("YipitDataSignalsKagglePipeline") \
        .master("local[*]") \
        .getOrCreate()

    print("=== [STEP 2] Carregando Dataset (Camada Bronze) ===")
    df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv("company_data.csv")
    
    print("=== [STEP 3] Higienizando Colunas Críticas (Camada Silver) ===")
    df_cleaned = df_raw.select(
        col("Bankrupt?").alias("is_bankrupt"),
        col(" ROA(C) before interest and depreciation before interest").alias("roa_before_interest"),
        col(" Net Value Growth Rate").alias("net_value_growth_rate"),
        col(" Net Income to Total Assets").alias("net_income_to_total_assets")
    )

    print("=== [STEP 4] Agregando Dados via Catalyst Optimizer ===")
    result_df = df_cleaned.groupBy("is_bankrupt").agg(
        count("*").alias("total_companies"),
        round(avg("roa_before_interest"), 4).alias("avg_roa"),
        round(avg("net_value_growth_rate"), 4).alias("avg_net_value_growth"),
        round(avg("net_income_to_total_assets"), 4).alias("avg_net_income_ratio")
    )
    result_df.show(truncate=False)

    print("=== [STEP 5] Exportando para a Camada Gold (Parquet Nativo) ===")
    output_path = "gold_market_intelligence_summary"
    
    # Coleta as 2 linhas resultantes e salva via PyArrow/Pandas de forma segura no Windows
    import pandas as pd
    pdf = result_df.toPandas()
    os.makedirs(output_path, exist_ok=True)
    pdf.to_parquet(os.path.join(output_path, "data.parquet"), index=False)
    
    print(f"-> Sucesso! Dados gravados na pasta Gold: '{output_path}/'")
    spark.stop()

if __name__ == "__main__":
    main()