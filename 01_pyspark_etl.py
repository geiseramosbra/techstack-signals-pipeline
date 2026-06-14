import os
import sys

# Injeção de flags necessárias para compatibilidade do Java runtime (Java 16+)
os.environ['_JAVA_OPTIONS'] = (
    '--add-opens=java.base/javax.security.auth=ALL-UNNAMED '
    '--add-opens=java.base/java.lang=ALL-UNNAMED '
    '--add-opens=java.base/java.util=ALL-UNNAMED'
)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, avg, count

def main():
    print("\n=== [STEP 1] Inicializando Sessão Spark (Pronto para Nuvem/Databricks) ===")
    
    spark = SparkSession.builder \
        .appName("YipitDataSignalsKagglePipeline") \
        .master("local[*]") \
        .getOrCreate()

    print("=== [STEP 2] Carregando o Dataset (Bronze Layer) ===")
    df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv("company_data.csv")
    
    print("=== [STEP 3] Selecionando, Renomeando e Higienizando as colunas críticas (Silver Layer) ===")
    df_cleaned = df_raw.select(
        col("Bankrupt?").alias("is_bankrupt"),
        col(" ROA(C) before interest and depreciation before interest").alias("roa_before_interest"),
        col(" Net Value Growth Rate").alias("net_value_growth_rate"),
        col(" Net Income to Total Assets").alias("net_income_to_total_assets")
    )

    print("=== [STEP 4] Executando Agregações via API de DataFrames Nativa ===")
    result_df = df_cleaned.groupBy("is_bankrupt").agg(
        count("*").alias("total_companies"),
        round(avg("roa_before_interest"), 4).alias("avg_roa"),
        round(avg("net_value_growth_rate"), 4).alias("avg_net_value_growth"),
        round(avg("net_income_to_total_assets"), 4).alias("avg_net_income_ratio")
    )
    
    result_df.show(truncate=False)

    print("=== [STEP 5] Exportando os dados limpos para a Camada Gold ===")
    output_path = "gold_market_intelligence_summary"
    
    try:
        # Coleta os resultados agregados e converte para Pandas de forma segura (apenas 2 linhas)
        # Salvamos como Parquet via biblioteca nativa Python, contornando a falha do Hadoop local
        import pandas as pd
        
        print("-> Convertendo resultados e gerando armazenamento analítico otimizado...")
        pdf = result_df.toPandas()
        
        # Garante a criação do diretório se ele não existir
        os.makedirs(output_path, exist_ok=True)
        
        # Salva o resultado final dentro do diretório Gold
        pdf.to_parquet(os.path.join(output_path, "data.parquet"), index=False)
        print(f"-> Sucesso! Dados gravados no diretório analítico local: '{output_path}/'")
        
    except Exception as e:
        print(f"=== [ERROR] Falha ao exportar os dados: {str(e)} ===")
        print("Dica: Certifique-se de instalar o pyarrow executando: pip install pyarrow")
    
    spark.stop()
    print("=== [SUCCESS] Pipeline de Dados concluída com sucesso! ===\n")

if __name__ == "__main__":
    main()